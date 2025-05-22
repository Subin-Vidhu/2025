#!/bin/bash

file='readfile.sh'
while read line; do
echo $line
done < $file


file='myfile.txt'
if [ -f $file ]; then
    echo "File exists, removing"
    rm -r $file
fi
echo "My file with a line" >> $file
cat $file
