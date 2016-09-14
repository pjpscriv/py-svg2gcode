#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *

PRINTS = False

def generate_gcode():
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
    
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    
    width = root.get('width')
    height = root.get('height')
    if width == None or height == None:
        viewbox = root.get('viewBox')
        if viewbox:
            _, _, width, height = viewbox.split()                

    if width == None or height == None:
        print "Unable to get width and height for the svg"
        sys.exit(1)
    
    #print "test:", width, height

    width = float(width)
    height = float(height)

    scale_x = bed_max_x / max(width, height)
    scale_y = bed_max_y / max(width, height)

    print preamble 
    
    #print(root)

    for elem in root.iter():
        #print(elem)
        try:
            tag_suffix = elem.tag
            # print tag_suffix
            # _, tag_suffix = elem.tag.split('}')
        except:
            print "Error reading tag value:", tag_suffix
            continue
        
        #print(tag_suffix)

        if tag_suffix in svg_shapes:
            #print(tag_suffix, "is in the thing")
            if PRINTS: print "thing:", tag_suffix
            shape_class = getattr(shapes_pkg, tag_suffix)
            if PRINTS: print "Shape Class:", shape_class
            shape_obj = shape_class(elem)
            #print "Shape obj:", str(shape_obj)
            d = shape_obj.d_path()
            if PRINTS: print "d:", d
            if PRINTS: print "if d:", bool(d)
            m = shape_obj.transformation_matrix()
            if PRINTS: print "m", m

            if d:
                if PRINTS: print("D IS TRUE")
                print shape_preamble 
                p = point_generator(d, m, smoothness)
                if PRINTS: print "Points:", p
                for x,y in p:
                    if PRINTS: print(x,y)
                    if x > 0 and x < bed_max_x and y > 0 and y < bed_max_y:  
                        print "G1 X%0.1f Y%0.1f" % (scale_x*x, scale_y*y) 
                print shape_postamble

    print postamble 

if __name__ == "__main__":
    generate_gcode()



