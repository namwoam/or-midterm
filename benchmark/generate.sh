echo "Generating testdata"
echo "------------------------"

if [[ -d "testdata" ]]; then
  rm -rf testdata
fi

mkdir testdata
cnt=1
  for i in ./setup-*.py; do
    limit=40
    for ((j = 0 ; j < $limit ; j ++)); do
      python3 $i > ./testdata/instance-$cnt.txt
      ((cnt+= 1))
    done
  done

echo "done."