#!/bin/sh
path=$1;
sep1=$2;
sep2=$3;
# replace sep1 with sep2 in the chosen file
sed "s/$sep1/$sep2/g" $path