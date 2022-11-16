#!/bin/sh
path=$1;
awk '$1!="#chrom" {print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 ":" $7 "\t" "+" > "human_BED.txt"}' $path