#!/bin/sh
RAD=$1;
PI=3.14;
# calculate area of the circle
echo $PI \* $RAD \* $RAD | bc -l;
