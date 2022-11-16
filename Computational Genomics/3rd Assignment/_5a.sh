#!/bin/sh
path=$1
# find lines that are in chr3R, bigger than 1000 and on + strand.
awk '$1=="chr3R"&&$3-$2>=1000&&$6=="+" {print $0}' $path