//Tamar Saad 207256991
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>
#include <ctype.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <dirent.h>
#include <errno.h>

int files_list[5];
int readLine(int file, char *path) {
    int f, i = 0;
    while ((f = read(file, &path[i], 1)) > 0 && path[i] != '\n') {
        ++i;
    }
    if (f < 0) {
        write(1, "Error in: reading configuration file\n", strlen("Error in: reading configuration file\n"));
        return -1;
    }
    path[i] = '\0';
    return 1;
}

//function accepts path to .c file and compile it
//return 1 if succeed, -1 if compilation error, exit if system call failed
int compileFiles(char *cpath, char* dir_path, char* output_name) {
    pid_t pid;
//    char compiled_file[151];
//    strcpy(compiled_file, dir_path);
//    strcat(compiled_file, output_name);
    char* compile[] = {"gcc", cpath, "-o", output_name, NULL};
    int status;
    pid = fork();
    if (pid < 0) {
        write(1, "Error in: fork\n", strlen("Error in: fork\n"));
        exit(-1);
    } else if (pid == 0) { //if we're in son
        if (execvp(compile[0], compile) < 0) {
            write(1, "Error in: ececvp\n", strlen("Error in: ececvp\n"));
            exit(-1);
        }
        return 1;
    } else { //we're in father
        wait(&status);
        return WEXITSTATUS(status);
    }
}

//function receives path to .c file to run, and path to file with input for the running
//returns 1 if succeed, -1 if compilation error, exit if system call failed
int runCFile(char *comp_path, char *input, char* output) {
    pid_t pid;
//    char comp_path[151];
//    strcat(strcpy(comp_path, cpath), "./a.out");
    char *run[] = {comp_path, NULL};
    int status;

    pid = fork();
    if (pid < 0) { //fork failed
        write(1, "Error in: fork\n", strlen("Error in: fork\n"));
        exit(-1);
    } else if (pid == 0) { //if we're in son
        int fd1, fd2;
        //set stdin to be input file and stdout to be output file
        if ((fd1 = open(input, O_RDONLY)) < 0) {
            write(1, "Error in opening input file\n", strlen("Error in opening input file\n"));
            exit(-1);
        }
        if ((fd2 = open(output, O_WRONLY | O_CREAT | O_TRUNC, 0777)) < 0) {
            write(1, "Error in opening output file\n", strlen("Error in opening output file\n"));
            exit(-1);
        }
        dup2(fd1, 0);
        dup2(fd2, 1);
        close(fd1);
        close(fd2);

        if (execvp(run[0], run) < 0) {
            perror("Error in running file\n");
            exit(-1);
        }
        return 1;
    }
    else { //we're in father
        wait(&status);
        return WEXITSTATUS(status);
    }
}

//run the compiled file of the first part of the assignment
int runEx21(char* comp_path, char* f1, char*f2) {
    pid_t pid;
    char *run[] = {comp_path, f1, f2, NULL};
    int status;

    pid = fork();
    if (pid < 0) { //fork failed
        write(1, "Error in: fork\n", strlen("Error in: fork\n"));
        exit(-1);
    } else if (pid == 0) { //if we're in son

        if (execvp(run[0], run) < 0) {
            perror("Error in running file\n");
            exit(-1);
        }
        return 1;
    }
    else { //we're in father
        wait(&status);
        return WEXITSTATUS(status);
    }
}

int compareOutputs(char* ex21_comp, char* students_output, char* real_output) {
    int returned_val, grade = -1;
    //run ex21 to check the output of the assignment
    returned_val = runEx21(ex21_comp, students_output, real_output);
    //check output
    if (returned_val == 2) //files are different
        grade = 50;
    else if (returned_val == 3) //files are similar
        grade = 75;
    else if (returned_val == 1) //files are identical
        grade = 100; //Woooooo
    else
        write(1, "wrong return value!\n", strlen("wrong return value!\n"));
    return grade;

}

void writeGrade(int grade, char* student) {
    int fd;
    char comment[30];
    char line[185];
    if ((fd = open("results.csv", O_CREAT | O_WRONLY | O_APPEND, 0777)) < 0) {
        write(1, "Error in: opening results file\n", strlen("Error in: opening results file\n"));
        return;
    }
    files_list[4] = fd;
    //find the right comment
    switch (grade) {
        case 0:
            strcpy(comment,",0,NO_C_FILE\n");
            break;
        case 10:
            strcpy(comment,",10,COMPILATION_ERROR\n");
            break;
        case 50:
            strcpy(comment,",50,WRONG\n");
            break;
        case 75:
            strcpy(comment,",75,SIMILAR\n");
            break;
        case 100:
            strcpy(comment,",100,EXCELLENT\n");
            break;
        default:
            write(1, "Error in: writing to results file\n", strlen("Error in: writing to results file\n"));
    }
    //get the full lime with name, grade and comment
    strcat(strcpy(line, student), comment);
    if (write(fd, line, strlen(line)) < 0) {
        write(1, "Error in: writing to results file\n", strlen("Error in: writing to results file\n"));
    }
    close(fd);
}

//this function receive a student's directory and look for .c file in it to compile, run and check output
int executeFiles(struct dirent *pDir, DIR *dp, char *students_path, char *input_path, char *output_path, char* dir_name) {
    int flag = 0; //flag if we found a c file to compile
    int returned_val, grade;
    char cpath[151];
    char compiled_file_path[151];
    char student_output[151];
    //chdir(students_path);
    //go through the directory's files
    while ((pDir = readdir(dp)) != NULL) {
        //check if it's a c file
        char *dot = strrchr(pDir->d_name, '.');
        if (dot && !strcmp(dot, ".c")) { //we found a c file! congratulations
            flag = 1; //indicate we found a c file
            //create a string for te c file path
            strcpy(cpath, students_path);
            strcat(strcat(cpath ,"/"), pDir->d_name);
            //create a string for the compiled file path
            strcat(strcpy(compiled_file_path, students_path), "/a.out");
            returned_val = compileFiles(cpath, students_path, compiled_file_path);
            if (returned_val != 0) { //compile error
                grade = 10;
                break;
            } else { //compilation was successful
                //create a string for the student's output path
                char cwd[151];
                char ex21_compiled[151];
                getcwd(cwd, sizeof(cwd));
                strcat(strcpy(student_output, cwd), "/student_output.txt");
                returned_val = runCFile(compiled_file_path, input_path, student_output);
                //compare the student's output and the real output
                //string for current working directory
                //string for the compiled file
                strcpy(ex21_compiled, cwd);
                strcat(ex21_compiled, "/comp.out");
                if ((returned_val = compareOutputs(ex21_compiled, student_output, output_path)) < 0) {
                    exit(-1);
                }
                grade = returned_val;
            }
            if (remove(compiled_file_path) < 0 || remove(student_output) < 0) {
                write(1, "Error in: deleting files\n", strlen("Error in: deleting files\n"));
                return -1;
            }
            break; //if we found a .c file there is no need to keep looking for it
        }
    }
    if (flag == 0) grade = 0;
    //update the results file
    writeGrade(grade, dir_name);
    return 1;
}

//this function go over all the student's directories
int startAssignment(char *dir_path, char *input_file, char *output_file) {
    struct dirent *pDirent;
    DIR *dir_strct;
    //opening the directory
    if ((dir_strct = opendir(dir_path)) == NULL) {
        write(1, "Not a valid directory\n", strlen("Not a valid directory\n"));
        //write(1, dir_path, strlen(dir_path));
        exit(-1);
    }
    //go over all the directories in the input directory
    while ((pDirent = readdir(dir_strct)) != NULL) {
        //the first two directories are the current one and the father
        if (strcmp(pDirent->d_name, ".") == 0 || strcmp(pDirent->d_name, "..") == 0) {
            continue;
        }
        //create the path for the next directory
        DIR *dp_student;
        struct dirent *pDir_student;
        char students_dir_path[151];
        strcpy(students_dir_path, dir_path);
        strcat(strcat(students_dir_path, "/"), pDirent->d_name);

        //try to open the directory
        if ((dp_student = opendir(students_dir_path)) == NULL) {
            //if the error is enotdir - we got to a file and move on
            if (errno == ENOTDIR)
                continue;
            write(1, "Error in: opening directory\n", strlen("Error in: opening directory\n"));
            continue;
        }
        if ((pDir_student = readdir(dp_student)) == NULL) {
            write(1, "Error in: reading directory\n", strlen("Error in: reading directory\n"));
            continue;
        }
        //execute the files in the directory
        executeFiles(pDir_student, dp_student, students_dir_path, input_file, output_file, pDirent->d_name);
    }
    return 0;
}

void closeFiles() {
    int i;
    for (i=0; i<5; ++i) {
        close(files_list[i]);
    }
}

int main(int argc, char **argv) {
    //array with pointers to all files so we could close them conveniently
    //set the errors to be written in error file
    int fid;
    if ((fid = open("errors.txt", O_CREAT | O_WRONLY, 0777)) < 0) {
        perror("Error in: opening errors file");
        exit(-1);
    }
    dup2(fid, 2);
    //input check
    if (argc != 2) {
        write(1, "Error in: Wrong number of inputs\n", strlen("Error in: Wrong number of inputs\n"));
        exit(-1);
    }
    int conf;
    if ((conf = open(argv[1], O_RDONLY)) < 0) {
        write(1, "Error in: opening configuration file\n", strlen("Error in: opening configuration file\n"));
        exit(-1);
    }
    //get the input from conf file
    char dirpath[151];
    char input_file_path[151];
    char output_file_path[151];
    int val;
    val = readLine(conf, dirpath);
    val += readLine(conf, input_file_path);
    val += readLine(conf, output_file_path);
    if (val < 3) exit(-1);
    //check if paths are relative or absolute, and change them accordingly
    char buffer[151];
    char cwd[151];
    getcwd(cwd, sizeof(cwd));
    if (dirpath[0] != '/') {
        strcpy(buffer, cwd);
        strcat(strcat(buffer, "/"), dirpath);
        strcpy(dirpath, buffer);
    }
    if (input_file_path[0] != '/') {
        strcpy(buffer, cwd);
        strcat(strcat(buffer, "/"), input_file_path);
        strcpy(input_file_path, buffer);
    }
    if (output_file_path[0] != '/') {
        strcpy(buffer, cwd);
        strcat(strcat(buffer, "/"), output_file_path);
        strcpy(output_file_path, buffer);
    }
    //check if the paths are valid
    int input_file, output_file;
    if ((input_file = open(input_file_path, O_RDONLY)) <= 0) {
        write(1, "Input file not exist\n", strlen("Input file not exist\n"));
        exit(-1);
    }
    if ((output_file = open(output_file_path, O_RDONLY)) <= 0) {
        write(1, "Output file not exist\n", strlen("Output file not exist\n"));
        exit(-1);
    }
    files_list[0] = conf;
    files_list[1] = input_file;
    files_list[2] = output_file;
    files_list[3] = fid; //errors file

    if (close(conf) < 0) {
        write(1, "Error in: closing config file\n", strlen("Error in: closing config file\n"));
        exit(-1);
    }
    close(input_file); //we will open them again in a different location
    close(output_file);
    startAssignment(dirpath, input_file_path, output_file_path);
    closeFiles();
}
