#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *

PRINTS = False

def generate_gcode():
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
    
    # Get the SVG Input File
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    
    # Get the Height and Width from the parent svg tag
    width = root.get('width')
    height = root.get('height')
    if width == None or height == None:
        viewbox = root.get('viewBox')
        if viewbox:
            _, _, width, height = viewbox.split()                

    if width == None or height == None:
        print "Unable to get width and height for the svg"
        sys.exit(1)
    
    # Scale the file appropriately
    width = float(width)
    height = float(height)
    scale_x = bed_max_x / max(width, height)
    scale_y = bed_max_y / max(width, height)

    # Write Initial GCODES
    print preamble 
    
    # Iterate through svg elements
    for elem in root.iter():
        log("--Found Elem: "+str(elem))
        try:
            tag_suffix = elem.tag.split("}")[-1]
        except:
            print "Error reading tag value:", tag_suffix
            continue
        
        # Checks element is valid SVG shape
        if tag_suffix in svg_shapes:

            log("  --Name: "+str(tag_suffix))

            # Get corresponding class object from 'shapes.py'
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)

            log("\tClass : "+str(shape_class))
            log("\tObject: "+str(shape_obj))
            log("\tAttrs : "+str(elem.items()))
            log("\tTransform: "+str(elem.get('transform')))
            d = shape_obj.d_path()

            log("\td: "+str(d))

            m = shape_obj.transformation_matrix()
            log("\tm: "+str(m))

            if d:
                if PRINTS: print("\td is GOOD!")

                print shape_preamble 
                p = point_generator(d, m, smoothness)

                log("\tPoints: "+str(p))

                for x,y in p:
                    log("\t "+str((x,y)))

                    if x > 0 and x < bed_max_x and y > 0 and y < bed_max_y:  
                        print "G1 X%0.1f Y%0.1f" % (scale_x*x, scale_y*y) 
                print shape_postamble
            else:
              log("\tNO PATH INSTRUCTIONS FOUND!!")
        else:
          log("  --No Name: "+tag_suffix)


    print postamble 

def log(message):
  if (PRINTS):
    print message



if __name__ == "__main__":
    generate_gcode()



