#!/usr/bin/env python

# External Imports
import os
import sys
import xml.etree.ElementTree as ET

# Local Imports
import shapes as shapes_pkg
from shapes import point_generator
from config import *

DEBUGGING = True
SVG = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])

## THIS IS A TEST


def generate_gcode(filename):

    # Define the Output
    debug_log(filename)
    outfile = filename.split(".svg")[0] + ".gcode"
    outfile = "out/" + outfile.split("in/")[-1]
    debug_log(outfile)

    gcode = ""

    # Get the SVG Input File
    file = open(filename, 'r')
    tree = ET.parse(file)
    root = tree.getroot()
    file.close()
    
    # Get the Height and Width from the parent svg tag
    width = root.get('width')
    height = root.get('height')
    if width == None or height == None:
        viewbox = root.get('viewBox')
        if viewbox:
            _, _, width, height = viewbox.split()                

    if width == None or height == None:
        # raise ValueError("Unable to get width or height for the svg")
        print "Unable to get width and height for the svg"
        sys.exit(1)
    
    # Scale the file appropriately
    width = float(width)
    height = float(height)
    scale_x = bed_max_x / max(width, height)
    scale_y = bed_max_y / max(width, height)

    # Write Initial GCODES
    gcode += preamble + "\n"
    
    # Iterate through svg elements
    for elem in root.iter():
        debug_log("--Found Elem: "+str(elem))
        new_shape = True
        try:
            tag_suffix = elem.tag.split("}")[-1]
        except:
            print "Error reading tag value:", tag_suffix
            continue
        
        # Checks element is valid SVG shape
        if tag_suffix in SVG:

            debug_log("  --Name: "+str(tag_suffix))

            # Get corresponding class object from 'shapes.py'
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)

            debug_log("\tClass : "+str(shape_class))
            debug_log("\tObject: "+str(shape_obj))
            debug_log("\tAttrs : "+str(elem.items()))
            debug_log("\tTransform: "+str(elem.get('transform')))


#################### HERE'S THE MEAT!!! ####################
            # Gets the Object path info in one of 2 ways:
            # 1. Reads the <tag>'s 'd' attribute.
            # 2. Reads the SVG and generates the path itself.
            d = shape_obj.d_path()
            debug_log("\td: "+str(d))

            # The *Transformation Matrix*
            # Specifies something about how curves are approximated
            # Non-essential - a default is used if the method below
            #   returns None.
            m = shape_obj.transformation_matrix()
            debug_log("\tm: "+str(m))

            if d:
                debug_log("\td is GOOD!")

                gcode += shape_preamble + "\n"
                points = point_generator(d, m, smoothness)

                debug_log("\tPoints: "+str(points))

                for x,y in points:
                    debug_log("\tpt: "+str((x,y)))

                    if x >= 0 and x < bed_max_x and y >= 0 and y < bed_max_y:
                        if new_shape:
                            gcode += ("G0 X%0.1f Y%0.1f" % (scale_x*x, scale_y*y))
                            new_shape = False
                        else:
                            gcode += ("G1 X%0.1f Y%0.1f" % (scale_x*x, scale_y*y))
                        gcode += "\n"
                        debug_log("\t    --Point printed")
                    else:
                      debug_log("\t    --Point not printed ("+str(bed_max_x)+","+str(bed_max_y)+")")
                gcode += shape_postamble + "\n"
            else:
              debug_log("\tNO PATH INSTRUCTIONS FOUND!!")
        else:
          debug_log("  --No Name: "+tag_suffix)

    gcode += postamble + "\n"

    # Write the Result
    ofile = open(outfile, 'w')
    ofile.write(gcode)
    ofile.close()
    #debug_log("RESULT:\n"+gcode)



def debug_log(message):
  if (DEBUGGING):
    print message



def test(filename):
  circle_gcode = "G28\nG1 Z5.0\nG4 P200\nG1 X10.0 Y100.0\nG1 X10.0 Y101.8\nG1 X10.6 Y107.0\nG1 X11.8 Y112.1\nG1 X13.7 Y117.0\nG1 X16.2 Y121.5\nG1 X19.3 Y125.7\nG1 X22.9 Y129.5\nG1 X27.0 Y132.8\nG1 X31.5 Y135.5\nG1 X36.4 Y137.7\nG1 X41.4 Y139.1\nG1 X46.5 Y139.9\nG1 X51.7 Y140.0\nG1 X56.9 Y139.4\nG1 X62.0 Y138.2\nG1 X66.9 Y136.3\nG1 X71.5 Y133.7\nG1 X75.8 Y130.6\nG1 X79.6 Y127.0\nG1 X82.8 Y122.9\nG1 X85.5 Y118.5\nG1 X87.6 Y113.8\nG1 X89.1 Y108.8\nG1 X89.9 Y103.6\nG1 X90.0 Y98.2\nG1 X89.4 Y93.0\nG1 X88.2 Y87.9\nG1 X86.3 Y83.0\nG1 X83.8 Y78.5\nG1 X80.7 Y74.3\nG1 X77.1 Y70.5\nG1 X73.0 Y67.2\nG1 X68.5 Y64.5\nG1 X63.6 Y62.3\nG1 X58.6 Y60.9\nG1 X53.5 Y60.1\nG1 X48.3 Y60.0\nG1 X43.1 Y60.6\nG1 X38.0 Y61.8\nG1 X33.1 Y63.7\nG1 X28.5 Y66.3\nG1 X24.2 Y69.4\nG1 X20.4 Y73.0\nG1 X17.2 Y77.1\nG1 X14.5 Y81.5\nG1 X12.4 Y86.2\nG1 X10.9 Y91.2\nG1 X10.1 Y96.4\nG1 X10.0 Y100.0\nG4 P200\nG4 P200\nG1 X110.0 Y100.0\nG1 X110.0 Y101.8\nG1 X110.6 Y107.0\nG1 X111.8 Y112.1\nG1 X113.7 Y117.0\nG1 X116.2 Y121.5\nG1 X119.3 Y125.7\nG1 X122.9 Y129.5\nG1 X127.0 Y132.8\nG1 X131.5 Y135.5\nG1 X136.4 Y137.7\nG1 X141.4 Y139.1\nG1 X146.5 Y139.9\nG1 X151.7 Y140.0\nG1 X156.9 Y139.4\nG1 X162.0 Y138.2\nG1 X166.9 Y136.3\nG1 X171.5 Y133.7\nG1 X175.8 Y130.6\nG1 X179.6 Y127.0\nG1 X182.8 Y122.9\nG1 X185.5 Y118.5\nG1 X187.6 Y113.8\nG1 X189.1 Y108.8\nG1 X189.9 Y103.6\nG1 X190.0 Y98.2\nG1 X189.4 Y93.0\nG1 X188.2 Y87.9\nG1 X186.3 Y83.0\nG1 X183.8 Y78.5\nG1 X180.7 Y74.3\nG1 X177.1 Y70.5\nG1 X173.0 Y67.2\nG1 X168.5 Y64.5\nG1 X163.6 Y62.3\nG1 X158.6 Y60.9\nG1 X153.5 Y60.1\nG1 X148.3 Y60.0\nG1 X143.1 Y60.6\nG1 X138.0 Y61.8\nG1 X133.1 Y63.7\nG1 X128.5 Y66.3\nG1 X124.2 Y69.4\nG1 X120.4 Y73.0\nG1 X117.2 Y77.1\nG1 X114.5 Y81.5\nG1 X112.4 Y86.2\nG1 X110.9 Y91.2\nG1 X110.1 Y96.4\nG1 X110.0 Y100.0\nG4 P200\nG28\n"
  print circle_gcode[:90], "..."
  return circle_gcode



if __name__ == "__main__":
  file = raw_input("Please supply a filename: ")
  if os.path.isfile(file):
    print file, "is a file"
    generate_gcode(file)
  else:
    raise ValueError("File \""+file+"\" not found")

