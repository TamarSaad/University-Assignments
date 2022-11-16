#!/bin/sh
# fill gene alternate names according to a dictionary in column 5 of bed file
bed=$1
dictionary=$2
while read line; do
    bed_gene=$(echo $line | awk '{print $4}')
    dict_gene=$(grep $bed_gene $dictionary | cut -f2)
    if [ ! $dict_gene ]
    then
        dict_gene="NA"
    fi
    echo $line | awk -v dict_gene=$dict_gene '{print $1 "\t" $2 "\t" $3 "\t" $4 "\t" dict_gene "\t" $6}'
done < $bed