for f in $(ls tests)
  do
  read -p "Press Enter to test \""$f"\" ..."
  ./RUNME tests/$f
done
