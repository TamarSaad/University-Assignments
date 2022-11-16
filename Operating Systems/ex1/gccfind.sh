#!/bin/bash
#Tamar Saad 207256991

#receive input
if (($# < 2)); then
    echo "Not enough parameters";
fi
DIR_PATH=$1
WORD=$2
#input check
if [[ ! -d $DIR_PATH ]]; then
    echo "First input should be a directory path"
    exit 2
fi
#we don't check if the second input is a string, since in bash everything is consdidered a string.
#delete all compiled files
rm -f ${DIR_PATH}/*.out
#compile all the files that contain the word
for file in $(ls ${DIR_PATH}/*.c 2> /dev/null); do
    if grep -qiw $file -e ${WORD}  ; then
        gcc $file -w -o ${file%.c}.out
    fi
done
#if we received a flag for recurssion
if [[ $3 = "-r" ]]; then
    #go through each directory and call the script recursively
    for dir in $DIR_PATH*; do
        if [ -d $dir ]; then
            bash $0 $dir/ $WORD -r
        fi
    done 
fi