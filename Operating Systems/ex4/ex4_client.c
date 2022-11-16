//Tamar Saad 207256991
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <fcntl.h>

//set global variables
char num1[30], num2[30], operand[30];


void check_input(int argc, char *argv[]) {
    if (argc != 5) { //wrong number of inputs
        //perror("Wrong number of inputs! Who taught you to count??\n");
        printf("ERROR_FROM_EX4\n");
        exit(-1);
    }
    if (atoi(argv[3]) < 1 || atoi(argv[3]) > 4) { //wrong distribution of operator
        //perror("Operand must be between 1 to 4! Shame on you\n");
        printf("ERROR_FROM_EX4\n");
        exit(-1);
    }
}


//alarm signal: if we didn't get respond from server in 30 seconds- we quit
void sig_alarm(int alrm) {
    printf("Client closed because no respond was received from the server for 30 seconds.\n");
    exit(-1);
}


char* get_opernad(char oper[]) {
    if (strcmp(oper, "1") == 0) { // +
        return "+";
    }
    if (strcmp(oper, "2") == 0) { // -
        return "-";
    }
    if (strcmp(oper, "3") == 0) { // *
        return "*";
    }
    if (strcmp(oper, "4") == 0) { // :
        return "/";
    }
    else
        return "error";
}



//handler of signal from server
void sig_handler(int sig) {
    //get the file name
    int id = getpid();
    char cid[30];
    sprintf(cid, "%d", id); //convert from int to str
    char file_name[40] = "to_client_";
    strcat(strcat(file_name, cid), ".txt");
    //read file of solution
    char line[80];
    FILE *file = fopen(file_name, "r");
    if (file == NULL) {
        //perror("Unable to open file!");
        printf("ERROR_FROM_EX4\n");
        exit(1);
    }
    //read line and print solution
    fgets(line, 80, file);
    printf("Client %s asked the question %s %s %s.\n The solution is: %s\n", cid, num1, get_opernad(operand), num2, line);
    //delete the file
    if(fclose(file) < 0) {
        //perror("Unable to close file!\n");
        printf("ERROR_FROM_EX4\n");
    }
    if (remove(file_name)) {
        printf("ERROR_FROM_EX4\n");
        //perror("Error in deleting the file!\n");
        exit(-1);
    }
    exit(0);
}


int main(int argc, char *argv[]) {
    signal(SIGALRM, sig_alarm);
    //input check
    check_input(argc, argv);
    // check if file exists
    int i = 0;
    int file;
    while ((( file = open("to_srv.txt", O_WRONLY | O_CREAT | O_EXCL, 0644)) < 0) && i < 10) {
        //the file exist already and we need to try again
        int randnum = (rand() % 5) + 1;
        sleep(randnum);
        ++i;
    }
    //the file doesn't exist, or we tried 10 times already
    if (i == 10) {
        //we tried too many times
        printf("I tried to open the file too many times. What did you think, that I'll wait for you forever? pffft\n");
        exit(-1);
    }
    //file doesnt exist and we are the bosses! wooooo
    int id = getpid();
    char cid[30];
    sprintf(cid, "%d", id);
    strcat(cid, "\n");
    char firstnum[30];
    strcat(num1, argv[2]);
    strcat(strcat(firstnum, num1), "\n");
    char oper[30];
    strcpy(operand, argv[3]);
    strcat(strcpy(oper, operand), "\n");
    char secnum[30];
    strcpy(num2, argv[4]);
    strcpy(secnum, num2);
    //strcat(strcat(secnum, num2), "\n");
    // write to file
    write(file, cid, strlen(cid));
    write(file, firstnum, strlen(firstnum));
    write(file, oper, strlen(oper));
    write(file, secnum, strlen(secnum));
    //signal server by pid
    int server_id = atoi(argv[1]);
    kill(server_id, SIGUSR1);
    //get signal back
    signal(SIGUSR2, sig_handler);
    //wait for response up to 30 seconds
    alarm(30);
    pause();
    return 0;
}
