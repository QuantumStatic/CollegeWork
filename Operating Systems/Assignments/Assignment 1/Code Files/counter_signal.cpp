#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>

pid_t pid;

void
sigint_handler(int sig)
{	if (pid>0) 
	{
		printf("Caught SIGINT to kill the child process!\n");
		kill(pid, SIGTERM);
	}
}

int main(int argc, char **argv)
{
	int input;
	int counter=0;
	int status=0;
	int i;
	//pid_t pid;
	signal(SIGINT, sigint_handler);
	printf ("--- Process %d is running\n", getpid());
	printf ("Enter a number: ");
	scanf ("%d", &input);
	pid=fork();
	if (pid > 0)
	{ // parent process
		pid=wait(&status);
		printf("--- End of Parent Process %d\n", getpid());
	}
	else if (pid == 0)
	{ // child process
		for (i=0; i<input; ++i)
		{
			printf("Child Process %d: counter=%d\n", getpid(), ++counter);
			sleep(1);  // count slowly
		}
	}
	else
	{ // fork failed
		printf("fork () failed!\n");
		exit (EXIT_FAILURE);
	}
	exit (EXIT_SUCCESS);
}		
