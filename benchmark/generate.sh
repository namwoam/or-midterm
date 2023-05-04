echo "Generating testdata"
echo "------------------------"

if [[ -d "../kung/testdata" ]]; then
  rm -rf ../kung/testdata
fi

mkdir ../kung/testdata
cnt=1
  for i in ./setup-*.py; do
    limit=40
    for ((j = 0 ; j < $limit ; j ++)); do
      python3 $i > ../kung/testdata/instance$cnt.txt
      ((cnt+= 1))
    done
  done

echo "done."