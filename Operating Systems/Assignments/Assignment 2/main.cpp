    //  CS3103 Operating Systems
    //  Semester B 2020/21
    //  Homework 2
    //  Created by Utkarsh JAIN and Aarnav GUPTA on 07/03/21.

#include <fstream>
#include <iostream>
#include <iomanip>
#include <pthread.h>
#include <semaphore.h>
#include <stdlib.h>
#include <sys/ioctl.h>      // This head file is used to obtain window size of the terminal
#include <unistd.h>
#include "generator.cpp"

using std::cerr;
using std::cin;
using std::cout;
using std::endl;
using std::fstream;
using std::ios;
using std::left;            // using some keywords from the standard namespace
using std::right;
using std::setw;
using std::string;
using std::to_string;
#define RUNNING 0
#define START_REST 1
#define REST_COMPLETE 2
#define QUIT 3

unsigned int labels[13] = {0}, get_label(string), interval_A = 0, interval_B = 0, interval_C = 0, job_size = 0, give_signal[3] = {0}, window_width;         /* get_label takes in the string and returns the integer label value  for that string. job_size is what the question refers as 'm', it refers to the articles that a crawler needs to process to rest. give_signal is used to communicate between strategy manager and crawler threads */
bool complete = false, crawler_output_stream_empty[3] = {false}; /* complete becomes true when all labels are more than or equal to 5. Mutexes are not FIFO or LIFO but they randomly let any thread pass. When the execution completes this boolean variable used to check if all crawlers print their respective outputs before the classifier proceeds to empty the buffer  */
void *crawler(void*), *classifier(void*), *strategy_manager(void*), wait_till_completion(), output(string, int);  /* wait_till_completion is the function that flips the complete variable from false to true when all labels have 5 or more articles*/
string remove_symbols_and_format(string);   /* This function is used to remove symbols from the original string and convert all letters to smaller case */
static pthread_mutex_t output_mutex = PTHREAD_MUTEX_INITIALIZER;
sem_t crawlers, classificaiton, job_done[3];    /* crawlers semaphore is used to make sure crawlers don't write into the queue when there is no space. Classification semaphore is used to make sure that classifier thread doesn't pop from an empty queue. job_done semaphore is used to halt a crawler thread when its communicating with strategy manager.*/
char* str_generator(void);

class Buffer {
private:
    string storage[12];
    int last_occupied_index;
    pthread_mutex_t buffer_mutex;
public:
    inline Buffer(){
        last_occupied_index = -1;                   // constructor to make a buffer
        buffer_mutex = PTHREAD_MUTEX_INITIALIZER;
    }
    inline bool isEmpty(){                          // function to check if the buffer empty
        return this->last_occupied_index < 0;
    }
    inline void insert(string);                     // function to insert into the buffer
    string pop();                                   // function to pop from the buffer
} buffer;                                           // creating a global Buffer object called buffer

int main(int argc, const char *argv[]) {
    interval_A = atoi(argv[1]);
    interval_B = atoi(argv[2]);                     // accepting arguments from the terminal
    interval_C = atoi(argv[3]);
    job_size = atoi(argv[4]);
    
    pthread_t crawler_threads[3], classifier_thread, strategy_manager_thread;
    int thread_id[3] = {0};
    
    sem_init(&classificaiton, 0, 0);
    sem_init(&crawlers, 0, 12);                     // initialising the semaphores
    for (int i = 0; i < 3; i++)
        sem_init(&job_done[i], 0, 0);
    
    struct winsize w;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &w);           // function to get terminal window size and set width size accordingly
    window_width = ceil(w.ws_col / 5);
    cout << setw(window_width) << left << "crawler 1"
         << setw(window_width) << left << "crawler 2"
         << setw(window_width) << left << "crawler 3"
         << setw(window_width) << left << "classifier"
         << setw(window_width) << left << "Manager" << endl;
    
    for (int i = 0; i < 3; i++) {
        thread_id[i] = i;
        if (pthread_create(&crawler_threads[i], NULL, crawler, (void *) &thread_id[i])){
            cerr << "Error when creating crawler thread " << i << '!' << endl;
            exit(-1);
        }
    }
    if (pthread_create(&classifier_thread, NULL, classifier, NULL)) {
        cerr << "Error when creating classifier thread!" << endl;
        exit(-1);
    }
    if (pthread_create(&strategy_manager_thread, NULL, strategy_manager, NULL)) {
        cerr << "Error when creating strategy manager thread!" << endl;
        exit(-1);
    }
    
    wait_till_completion();             /* this function checks if all labels are full and then makes the complete variable true */
    
    void* retval;
    for (int i = 0; i < 3; i++)
        if (pthread_join(crawler_threads[i], &retval)){
            cerr << "Error when joining crawler thread " << i << '!' << endl;
            exit(-1);
        }
    if (pthread_join(classifier_thread, &retval)) {
        cerr << "Error when joining classifier thread!" << endl;
        exit(-1);
    }
    if (pthread_join(strategy_manager_thread, &retval)) {
        cerr << "Error when joining strategy manager thread!" << endl;
        exit(-1);
    }
    
    sem_destroy(&crawlers);
    sem_destroy(&classificaiton);
    for (int i = 0; i < 3; i++)
        sem_destroy(&job_done[i]);
    pthread_exit(NULL);
}

void wait_till_completion(){                        /* function checks if all labels are greater equal to 5 and then marks complete = true */
    for(int i = 0; i < 13;)
        if (labels[i] >= 5)
            i++;
    complete = true;
}

void* crawler(void* arg){
    int id = *(int*) arg, articles_processed = 0;   // ID is the unique id of a crawler which is passed at thread creation
    output("start", id);
    
    while (not complete) {
        if (articles_processed == job_size){        // job size is given articles after which crawler needs to rest
            give_signal[id] = START_REST;           // crawler is informing the strategy manager that rest is  starting
            sem_wait(&job_done[id]);
            if (give_signal[id] == QUIT)            // Check if the program completed while resting
                break;
            output("rest", id);
            usleep(interval_C);
            give_signal[id] = REST_COMPLETE;        // crawler is informing the strategy manager that rest is completed
            sem_wait(&job_done[id]);
            output("s-rest",id);
            if (give_signal[id] == QUIT)            // Check if the program completed while resting
                break;
            articles_processed = 0;
        }
        
        string article = string(str_generator());
        if (sem_trywait(&crawlers) != 0){       /* if the thread is going to wait then this conditional evaluates to true*/
            output("wait", id);
            sem_wait(&crawlers); 
            output("s-wait", id);
        }
        
        if (give_signal[id] == QUIT)                // Check if the program completed while resting
            break;
        output("grab", id);
        buffer.insert(article);
        usleep(interval_A);
        output("f-grab", id);
        sem_post(&classificaiton);
        articles_processed++;
    }
    
    output("quit", id);
    crawler_output_stream_empty[id] = true;         /* since the crawler will not print anything more the output stream is empty */
    pthread_exit((NULL));
}

void* classifier(void* arg){
    int id = 3, article_key = 0;
    output("start", id);
    fstream file;
    file.open("text_corpus.txt", ios::out | ios::trunc);
    
    while (not complete){
        sem_wait(&classificaiton);
        output("clfy", id);
        string to_classify = buffer.pop();
        int label = get_label(remove_symbols_and_format(to_classify));
        labels[label-1]++;
        file << ++article_key <<' '<< label <<' '<< to_classify <<' '<< endl;
        usleep(interval_B);
        output("f-clfy", id);
        sem_post(&crawlers);
    }
    
    for (int i = 0; i < 3; i++){
        give_signal[i] = QUIT;
        sem_post(&crawlers);                /* Telling crawlers to resume execution and making crawlers flow if they were waiting */
    }
    
    for (int i = 0; i < 3;)                 /* Checking if any of the crawlers put anything in the output stream it's printed before we print k-enough */
        if (crawler_output_stream_empty[i])
            i++;
    
    output(to_string(article_key) + "-enough", id);
    
    while (not buffer.isEmpty()){
        output("clfy", id);
        string to_classify = buffer.pop();
        int label = get_label(remove_symbols_and_format(to_classify));
        labels[label-1]++;
        file << ++article_key <<' '<< label <<' '<< to_classify <<' '<< endl;
        usleep(interval_B);
        output("f-clfy", id);
    }
    
    output(to_string(article_key) + "-store", id);
    output("quit", id);
    file.close();
    pthread_exit((NULL));
}

void* strategy_manager(void* arg){
    int id = 4;
    output("Start", id);
    
    while (not complete) for (int i=0; i < 3; i++)
        if (give_signal[i] != RUNNING) {
            if (give_signal[i] == START_REST)               /* Checking if thread gave a signal other than running, what is it  and reacting to it accordingly */
                output("get-cr" + to_string(i+1), id);
            else if (give_signal[i] == REST_COMPLETE)
                output ("up-cr" + to_string(i+1),id);
            give_signal[i] = RUNNING;
            sem_post(&job_done[i]);
        }
    
    for (int i = 0; i < 3; i++){
        give_signal[i] = QUIT;          /* Telling crawlers to quit and making crawlers flow again if they were waiting */
        sem_post(&job_done[i]);
    }
    
    output("quit", id);
    pthread_exit((NULL));
}

void Buffer::insert(string str) {
    pthread_mutex_lock(&this->buffer_mutex);
    storage[++last_occupied_index] = str;           /* inserting in a thread safe manner into the buffer while maintaining queue property */
    pthread_mutex_unlock(&this->buffer_mutex);
}

string Buffer::pop() {
    if (this->last_occupied_index < 0)
        return NULL;
    
    pthread_mutex_lock(&this->buffer_mutex);
    string retVal = this->storage[0];
    for (int i = 0; i < this->last_occupied_index; i++)     /* popping from the buffer in a thread safe manner while maintaing a queue property */
        this->storage[i] = this->storage[i+1];
    this->last_occupied_index--;
    pthread_mutex_unlock(&this->buffer_mutex);
    
    return retVal;
}

string remove_symbols_and_format(string str){
    string formattedString;
    for (char ch: str)
        if (isalpha(ch))
            formattedString += tolower(ch);
    return formattedString;
}

unsigned int get_label(string toLabel){
    return (int)(toLabel[0] - 'a') % 13 + 1;
}

void output(string to_output, int id){
    int width = window_width*id;
    if (id < 3)
        width += 8;
    else if (id == 3)           /* formating output based on the their heading widths*/
        width += 10;
    else if (id == 4)
        width += 7;
    
    pthread_mutex_lock(&output_mutex);
    cout << setw(width) << right << to_output << endl;
    pthread_mutex_unlock(&output_mutex);
}
