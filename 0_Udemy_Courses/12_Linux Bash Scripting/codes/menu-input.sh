#!/bin/bash

echo "Choose color"
select color in red green blue
do
    break
done
echo "You chose $color"
