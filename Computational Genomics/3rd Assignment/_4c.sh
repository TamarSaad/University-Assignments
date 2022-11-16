#!/bin/sh
path=$1;
size=$2;
end=$3;
# find files with the asked end and bigger ther the asked size. 
find $path -type f -name "*$end" -size +${size}k