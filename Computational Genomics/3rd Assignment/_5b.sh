#!/bin/sh
path=$1;

awk '{split($10,a,"\""); print $1 "\t" $4 "\t" $5 "\t" a[2] "\t" $3 "\t" $7 "\t" > "drosofila_BED.txt"}' $path