#!/bin/bash

# Display all of input+output files or
# just 15 lines of each
verbose=false

if [[ ! $# -eq 1 ]]
  then
  echo -e "\e[95mBruh\e[0m you needa have one argument. C'mon now. \nIt should probably to be an \e[93m.svg file\e[0m because then I can do some magic with it."
else
  infile=$1

  # 1. Print input file name        # Output Styles listed here:
  inlen=$(cat $infile | wc -l)
  echo -en "\e[4m"                  # 1. Underline
  echo -e "Input: \"$infile\" ($inlen lines)"
  
  # 2. Show input file
  echo -en "\e[24;96m"              # 2. Cyan, no Underline
  if [ $verbose = false ] ; then
    if [[ $inlen -gt 15 ]] 
     then
     cat $infile | head -n 10
     echo ...
     cat $infile | tail -n 5
    else
      cat $infile
    fi
  else
    cat $infile
  fi
  
  # 3. Convert to GCode
  buglen=$(python -c "import svg2gcode as s2g; s2g.generate_gcode(\"$infile\")" | wc -l)
  echo -e "\e[0;4m"                  # 4. White, Underlined
  echo "Debugging: ($buglen lines)"
  echo -en "\e[24;33m"               # 5. Orange, no Underline
  python -c "import svg2gcode as s2g; s2g.generate_gcode(\"$infile\")"
  
  # 4. Print output file name

  fname=${infile%.svg}
  name=${fname##*/}
  flocation=${fname%$name}
  outfile=${flocation}gcode_output/$name.gcode
  outlen=$(cat $outfile | wc -l)
  echo -e "\e[0;4m"                  # 4. White, Underlined
  echo -e "Output: \"$outfile\" ($outlen lines)"


  # 5. Print output file
  echo -en "\e[24;32m"               # 5. Green, no Underline
  if [ $verbose = false ] ; then
    if [[ $outlen -gt 15 ]] 
      then
      cat $outfile | head -n 10
      echo ...
      cat $outfile | tail -n 5
    else
       cat $outfile
    fi
  else
    cat $outfile
  fi
  
  echo -ne "\e[0m"                   # Reset to normal
fi
