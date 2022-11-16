//Tamar Saad 207256991
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <signal.h>
#include <unistd.h>


int get_answer(int num1, int num2, char oper[]) {
    int ans = 1;
    if (strcmp(oper, "1\n") == 0) { // +
        ans = num1 + num2;
    }
    if (strcmp(oper, "2\n") == 0) { // -
        ans = num1 - num2;
    }
    if (strcmp(oper, "3\n") == 0) { // *
        ans = num1 * num2;
    }
    if (strcmp(oper, "4\n") == 0) { // :
        ans = num1 / num2;
    }
    else {
        printf("something went wrong in calculation...\n");
    }
    return ans;
}


void sig_handler(int sig) {
    signal(SIGUSR1, sig_handler);
    int pid;
    if ((pid = fork()) < 0) { //fork failed
        //perror("Fork failed\n");
        printf("ERROR_FROM_EX4\n");
        return;
    }
    if (pid == 0) { //child
        //read file from client
        int MAX_LINE_LENGTH = 30;
        char line[MAX_LINE_LENGTH];
        FILE *file = fopen("to_srv.txt", "r");
        if (file == NULL) {
            //perror("Unable to open file!");
            printf("ERROR_FROM_EX4\n");
            exit(1);
        }
        //read 4 lines and remove '\n' characters
        fgets(line, MAX_LINE_LENGTH, file);
        char client_id[MAX_LINE_LENGTH];
        strcpy(client_id, line); //= line;
        client_id[strlen(client_id) - 1] = '\0';
        fgets(line, MAX_LINE_LENGTH, file);
        int first_num = atoi(line);
        fgets(line, MAX_LINE_LENGTH, file);
        char operand[30];
        strcpy(operand, line);
        fgets(line, MAX_LINE_LENGTH, file);
        int second_num = atoi(line);

        if (fclose(file)) {
            printf("ERROR_FROM_EX4\n");
            //perror("Error in closing file!\n");
            exit(-1);
        }
        if (remove("to_srv.txt")) {
            printf("ERROR_FROM_EX4\n");
            //perror("Error in deleting the file!\n");
            exit(-1);
        }
        char answer[80];
        // if we want to divide in 0
        if (second_num == 0 && strcmp(operand, "4\n") == 0) {
            strcpy(answer, "You can't divide by 0! Go and learn math already\n");
        } else { //else - get the solution
            int ans = get_answer(first_num, second_num, operand);
            // cast the int to string
            sprintf(answer, "%d", ans);
        }
        // write the answer in the file for the client
        char file_name[40] = "to_client_";
        strcat(file_name, client_id);
        strcat(file_name, ".txt");
        FILE *fp;
        if ((fp = fopen(file_name, "w")) < 0) printf("ERROR_FROM_EX4\n");
        fputs(answer, fp);
        if (fclose(fp) < 0)   printf("ERROR_FROM_EX4\n");
        //send signal to client
        pid_t cid = atoi(client_id);
        kill(cid, SIGUSR2);
        exit(0);
    }
    else { //parent
        return; //and wait to other clients
    }
}

//alarm signal: if we didn't get calls from clients in 60 seconds- we quit
void sig_alarm(int alrm) {
    printf("The server was closed because no service request was received for the last 60 seconds.\n");
    //kill all zombie processes
    while (wait(NULL) != -1) {};
    //delete remaining files
    remove("to_srv.txt");
    system("rm -f to_client_*.txt");
    exit(-1);
}

int main() {
    signal(SIGALRM, sig_alarm);
    signal(SIGUSR1, sig_handler);


    while (1) {
        // set alarm of 60 seconds
        alarm(60);
        //wait for clients
        pause();
    }
}
