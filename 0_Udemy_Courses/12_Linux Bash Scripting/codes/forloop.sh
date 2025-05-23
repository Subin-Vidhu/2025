#!/bin/bash

for name in bob tom harry; do
    echo "Hello $name"
done

for i in {1..10}
do
    echo "$i"
done

for fn in *; do
    echo "$fn"
done
