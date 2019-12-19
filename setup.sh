#!/bin/bash

if [ -z "$1" ]
  then
    echo "missing argument"
    exit 0
fi

echo "clearing existing txt files"
rm -f tmp/*txt
echo "copying from $1"
cp ~/Downloads/journal-papers/$1/*pdf tmp/

echo "converting pdf to txt"
cd tmp
for file in *.pdf; do pdftotext "$file" "$file.txt"; done
rm -f *.pdf
cd ..

echo "extracting haikus"
python main.py tmp > found/$1.out 2> /dev/null

echo "output: found/$1.out"
