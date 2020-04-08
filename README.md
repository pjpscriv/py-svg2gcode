# Python SVG to G-Code Converter
A fast svg to gcode compiler forked from [vishpat/svg2gcode](https://github.com/vishpat/svg2gcode).

This library takes an svg file `location/my_file.svg` and outputs the gcode conversion to a folder in the same directory `location/gcode_output/my_file.gcode`.

The file `config.py` contains the configurations for the conversion (printer bed size etc).

## Installation
Simply clone this repo.
```
git clone https://github.com/pjpscriv/py-svg2gcode.git
```

## Usage
### As a Python module
To import it into your existing python project:
```python
import py-svg2gcode
```
or
```python
import generate_gcode from py-scvg2gcode
```
### As a Python Command
```
python svg2gcode.py
```

### With Bash Script (Recommended)
You can also use the `RUNME` script to convert files.

This method is useful for debugging as it gives you extra information.
```
./RUNME my_svg_file.svg
```

## Details
The compiler is based on the eggbot project and it basically converts all of the SVG shapes into bezier curves. The bezier curves are then recursively sub divided until desired smoothness is achieved. The sub curves are then approximated as lines which are then converted into g-code.
