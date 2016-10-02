# Python SVG to G-Code Converter
A fast svg to gcode compiler forked from github user [vishpat](https://github.com/vishpat)'s [svg2gcode repository](https://github.com/vishpat/svg2gcode).

## Installation
Simply clone this repo.
```
git clone https://github.com/JustaBitDope/py-svg2gcode.git
```

## Usage
Use the `RUNME` script to convert files. ensure you are submitting files the are in the `in` directory as parameters. Their output files will be placed in the `out` directory.
```
./RUNME in/svgfile.svg
```

The file `config.py` contains the configurations for the conversion (printer bed size etc).

## Details
The compiler is based on the eggbot project and it basically converts all of the SVG shapes into bezier curves. The bezier curves are then recursively sub divided until desired smoothness is achieved. The sub curves are then approximated as lines which are then converted into g-code.
