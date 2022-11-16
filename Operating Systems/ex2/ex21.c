//Tamar Saad 207256991
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <fcntl.h>

//this function checks if all characters in files from a certain point are spaces
int isEmpty(int file, char* ch) {
    int f;
    while((f = read(file, &ch, 1)) > 0) {
        if(!isspace(*ch)) { //if the character is not space then the file is not empty
            return 0;
        }
    }
    if (f == 0) { //we finished reading and the file is empty
        return 1;
    }
    return -1;  //if we got here then there was an error
}

//this function receive 2 files and checks if they are identical(1), similar(3) or different(2)
int compareFiles(int firstf, int secondf) {
    int returnval = 1; //return value is initialized as 1 -> the files are identical
    char ch1, ch2;
    int file1, file2;
    //read the files letter by letter
    file1 = read(firstf, &ch1, 1);
    file2 = read(secondf, &ch2, 1);
    int flag1, flag2; //flags tell us if we reached a white space

    while (file1 > 0 && file2 > 0) {
        flag1 = 0, flag2 = 0;
        //if one of the characters is space
        if (isspace(ch1)) {
            flag1 = 1;
        }
        if (isspace(ch2)) {
            flag2 = 1;
        }

        if (flag1 && !flag2) { //if only first char is space, we want to keep reading only that file
            returnval = 3; //the files are now in similar status
            file1 = read(firstf, &ch1, 1);
            continue;
        } else if (flag2 && !flag1) { //only second char is space- same as above
            returnval = 3;
            file2 = read(secondf, &ch2, 1);
            continue;
        }

        if (ch1 != ch2) { //if the characters are not identical
            if (flag1 && flag2) {  //both characters are spaces but not from the same type
                returnval = 3;
            } else if (toupper(ch1) == toupper(ch2)) { //the same characters but upper/lower case
                returnval = 3;
            }
            else return 2; //the characters are different and so are the files
        }
        //keep reading
        file1 = read(firstf, &ch1, 1);
        file2 = read(secondf, &ch2, 1);
    }
    //if we are out of the loop- we either had an error or finished reading at least one of the files

    //if we had an error
    if (file1 < 0 || file2 < 0) {
        perror("Error in: reading file\n");
        return -1;
    }

    if (file1 == 0 && file2 == 0) return returnval; //we finished reading both files
    //if we got here it means we finished reading only one file
    int val;
    if (file1 == 0) { //we only finished reading the first file
        val = isEmpty(secondf, &ch2);    //we want to check if the other file only contains spaces
    }
    else if (file2 == 0) {
        val = isEmpty(firstf, &ch1);
    }
    if (val > 0) return 3; //files are similar
    else if (val == 0) return 2; //files are different
    else if (val < 0) {
        perror("Error in: reading file");
        return -1;
    }
    return -2;  //we are not supposed to get here at all
}

int main(int argc, char **argv) {
    //check input
    if (argc != 3) {
        perror("Wrong number of inputs");
        return -1;
    }

    //read files if exist
    int firstf, secondf;
    if ((firstf = open(argv[1], O_RDONLY)) < 0) {
        perror("Error in: opening first file\n");
        return -1;
    }
    if ((secondf = open(argv[2], O_RDONLY)) < 0) {
        perror("Error in: opening second file\n");
        return -1;
    }
    int val;
    val = compareFiles(firstf, secondf);
    if (close(firstf) < 0) perror("Error in: closing first file");
    if (close(secondf) < 0) perror("Error in: closing second file");
    if (val == -2) {
        perror("Error in: we got something we were'nt supposed to");
        val = -1;
    }
    exit(val);
}

