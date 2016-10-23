for f in $(ls tests)
  do 
  echo 
  read -p "Press Enter to test \""$f"\" ..."
  ./RUNME tests/$f
done
