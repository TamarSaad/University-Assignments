//Tamar Saad 207256991
//Shell

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>

//char* builin_commands[] = { "exit", "cd", "history" };
static char* names_cmds[100];
static pid_t ids_cmds[100];
static int num_of_command = 0;

//get input from user
int getInput(char* inp) {
    char* line=NULL; size_t len = 100; ssize_t lineSize;
	printf("$ ");
	fflush(stdout);
    //read line
	if ((lineSize = getline(&line, &len, stdin)) == -1) { //failure
		if (feof(stdin)) {
			exit(0);  // We read an empty line
		}
		else {
			perror("getinput");
			exit(1);
		}
	}
    if ('\n' == line[0]) { //an empty line
        return 1;
    }
	if (lineSize != 0) { //if we read the line successfully
		inp = strcpy(inp, line); //put the value inside inp
		return 0;
	}
}
//seperate the input string into an array of seperated words
int seperateInput(char* inp, char** sep) {
    char* word;
    int i = 0;
    word = strtok(inp, " \n");
    while (word != NULL) {
        sep[i] = word;
        word = strtok(NULL, " \n");
        ++i;
    }
    sep[i] = NULL;
    }

void addPaths(int argc, char **argv) {
    int i;
 	char* pathway = getenv("PATH");
    for (i=0; i<argc; i++) {
        pathway = strcat(pathway,":");
        strcat(pathway,argv[i]);
    }
    setenv("PATH", pathway, 1);
}

//if the command isn't built in- we will use the system command
void systemCall(char* input, char** args) {
    char inputcpy[100];

    strcpy(inputcpy, input);
    //create son's process
    pid_t pid = fork();

    if (pid == -1) { //the fork failed
		perror("fork failed\n");
		return;
    }
    //if we're in son
    else if (pid == 0) {
        execvp(args[0], args);
		if (execvp(args[0], args) < 0) {
			perror("exec failed\n");
		}
		exit(0);
    }

    else { //we're in parent
    //wait for son to finish running
        wait(NULL);
        names_cmds[num_of_command]= strdup(inputcpy);
		ids_cmds[num_of_command] = pid;
		++num_of_command;
		return;
    }

}

//check if the command is a builtin command and execute it if so
//else- ask bash to execute it
void asYouWish(char* input, char** args) {
    char inputcpy[100];
    strcpy(inputcpy, input);
    //if the command is cd
    if (!strcmp(args[0], "cd")) {
        if (chdir(args[1]) != 0) {
	        perror("chdir failed");
        }
        //add the command to history array
        names_cmds[num_of_command]= strdup(inputcpy);
		ids_cmds[num_of_command] = getpid();
		++num_of_command;
    }
    //if the command is exit
    else if (!strcmp(args[0], "exit")) {
        exit(0);
    }
    //if the command is history
    else if (!strcmp(args[0], "history")) {
        //add the history command to the command history
        names_cmds[num_of_command]= strdup(inputcpy);
		ids_cmds[num_of_command] = getpid();
		++num_of_command;
        int i=0;
        //print the commands
        for (i; i<num_of_command; ++i) {
			printf("%d\t %s", ids_cmds[i], names_cmds[i]);
        }
    }
    //if the command isn't builtin
    else {
        systemCall(inputcpy, args);
    }
}

int main(c) {
    //add pathways to PATH environment
    addPaths(argc, argv);
    //initialize variables for the processess
    char input[100], inputcpy[100]; //the input line
    char* sepinput[100]; //the input seperated by words


    //infinate loop for the user's commands 
    while(1) {  
        //get input from user
        if (getInput(input)) {
            continue;
        }
        //parse it to an array of strings
        strcpy(inputcpy, input);
        seperateInput(inputcpy, sepinput);
        //execute the command
        asYouWish(input, sepinput);
    }
    return 0;
}