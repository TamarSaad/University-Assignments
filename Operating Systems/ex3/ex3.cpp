//Tamar Saad 207256991
#include <iostream>
#include <thread>
#include <mutex>
#include <queue>
#include <string>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <unistd.h>
#include <time.h>
#include <fstream>

using namespace std;

class UnboundedQueue {
private:
    queue<string> m_queue;
    sem_t full{};
    mutex lock;
public:
    UnboundedQueue() {
        sem_init(&full, 0, 0);
    }
    void push(const string& item) {
        lock.lock();
        m_queue.push(item);
        lock.unlock();
        sem_post(&full);
    }
    string pop()
    {
        sem_wait(&full);
        lock.lock();
        string item = m_queue.front();
        m_queue.pop();
        lock.unlock();
        return item;
    }
};

class BoundedQueue {
private:
    queue<string> m_queue;
    sem_t full{};
    sem_t empty{};
    mutex lock;
    int size;

public:
    BoundedQueue(int size) {
        sem_init(&full, 0, 0);
        sem_init(&empty, 0, size);
        this->size = size;
    }
    void push(const string& item) {
        sem_wait(&empty);
        lock.lock();
        m_queue.push(item);
        lock.unlock();
        sem_post(&full);
    }
    string pop()
    {
        sem_wait(&full);
        lock.lock();
        string item = m_queue.front();
        m_queue.pop();
        lock.unlock();
        sem_post(&empty);
        return item;
    }
};

vector<BoundedQueue*> reportsQ;
UnboundedQueue dispatcherQ[3];

class Producer {
private:
    int producerNum;
    int numOfStrings;
    string reports[3] = {" SPORTS ", " NEWS ", " WEATHER "};
    int numOfReports[3] = {0};

public:
    Producer(int p, int nos) {
        producerNum = p;
        numOfStrings = nos;
    }

    void produce() {
//        BoundedQueue* bq = new BoundedQueue(sizeOfQueue);
//        reportsQ.push_back(bq);
        //create the strings one by one
        for (int i=0; i<this->numOfStrings; ++i) {
            //create random number of 0-2
            int rnd = rand() % 3;
            //get the report type
            string report = this->reports[rnd];
            //create the report itself
            string str = "Producer " + to_string(producerNum) + report + to_string(this->numOfReports[rnd]);
            this->numOfReports[rnd] += 1;
            //insert the report to the producer's queue
            reportsQ[producerNum - 1]->push(str);
        }
        reportsQ[producerNum - 1]-> push("DONE");
    }
};

vector<Producer> producersVec;
vector<thread> threadsVec;


class Dispatcher {
private:
    int numOfProducers;
    int numOfActiveProducers;
    string reports[3] = {" SPORTS ", " NEWS ", " WEATHER "};
public:
    Dispatcher(int num) {
        numOfActiveProducers = num;
        numOfProducers = num;
    }
    void dispatch() {
        int* inactiveProducers = new int[numOfActiveProducers];
        for (int i=0; i<numOfActiveProducers; ++i) {
            inactiveProducers[i] = 0;
        }
        //while there are still active producers
        while (numOfActiveProducers > 0) {
            //read a report from every producer (Round Robin)
            for (int i = 0; i < numOfProducers; ++i) {
                //if the producer is active
                if (!inactiveProducers[i])
                getReport(i, inactiveProducers);
            }
        }
        //close the dispatcher queue
        for (auto & i : dispatcherQ) {
            i.push("DONE");
        }
    }
    //read a report from a single producer
    void getReport(int producerNum, int inactiveProducers[]) {
        string str = reportsQ[producerNum]->pop();
        //if the producer finished producing
        if (str == "DONE") {
            inactiveProducers[producerNum] = 1;
            numOfActiveProducers--;
            return;
        }
        //get the type of the report
        int type = getReportType(str);
        dispatcherQ[type].push(str);
    }

    int getReportType(const string& str) {
        for (int i=0; i<reports->size(); ++i) {
            if (str.find(reports[i]) != string::npos) {
                return i;
            }
        }
        perror("Wrong type of string!");
        return -1;
    }
};

class CoEditor {
private:
    int type;
    BoundedQueue* screenManagerQ;
public:
    CoEditor(int i, BoundedQueue* smq) {
        type = i;
        screenManagerQ = smq;
    }
    void readFromQ() {
        while(true) {
            string str = dispatcherQ[type].pop();
            //cout<<"string from coeditor: "<<str<<endl;
            if (str == "DONE") {
                usleep(100000);
                screenManagerQ->push(str);
                return;
            }
            screenManagerQ->push(str);
        }
    }
};

class ScreenManager {
private:
    int numOfActiveCoEditors = 3;
    BoundedQueue* screenManagerQ;
public:
    ScreenManager(BoundedQueue* smq) {
        screenManagerQ = smq;
    }
    void screen() {
        while (numOfActiveCoEditors > 0) {
            string str = screenManagerQ->pop();
            if (str == "DONE") {
                numOfActiveCoEditors--;
                continue;
            }
            cout<<str<<endl;

        }
        cout<<"DONE"<<endl;
    }
};

int readFile(char* fileName) {
    ifstream file;
    file.open(fileName);
    if(!file.is_open())
    {
        cout<<"Unable to open the file."<<endl;
        exit(-1);
    }
    string line1, line2, line3;
    while (getline(file, line1)) {
        //read next line and check if exists
        if (!getline(file, line2)) {
            file.close();
            return stoi(line1);
        }
        getline(file, line3);
        //initialize a new producer
        int producerNum = stoi(line1);
        int numOfStrings = stoi(line2);
        int queueSize = stoi(line3);
        Producer producer = Producer(producerNum, numOfStrings);
        producersVec.push_back(producer);
        //add a bounded queue to the producers queues
        BoundedQueue* bq = new BoundedQueue(queueSize);
        reportsQ.push_back(bq);
        //create a new thread
        threadsVec.emplace_back(thread(&Producer::produce, producer));
        // read empty line
        getline(file, line1);
    }
    file.close();
    sleep(1);
    return -1;
}

void getCoEditors(BoundedQueue* smQ) {
    for (int i=0; i<3; ++i) {
        CoEditor coe = CoEditor(i, smQ);
        threadsVec.emplace_back(thread(&CoEditor::readFromQ, coe));
    }
}


void KolIsrael(int numOfCoEditors) {
    //initialize dispatcher
    Dispatcher dispatcher = Dispatcher(producersVec.size());
    threadsVec.emplace_back(thread(&Dispatcher::dispatch, dispatcher));
    //initialize co-editors
    sleep(1);
    BoundedQueue screenManagerQ(numOfCoEditors);
    getCoEditors(&screenManagerQ);
    sleep(1);
    //create screen manager
    ScreenManager screenManager = ScreenManager(&screenManagerQ);
    threadsVec.emplace_back(thread(&ScreenManager::screen, screenManager));
    //wait for all the threads to finish before main thread will
    for (auto & i : threadsVec) {
        i.join();
    }
    //clean memory
    for (auto &p : reportsQ) {
        delete p;
    }
}


int main(int argc, char **argv) {
    srand(time(nullptr));
    //read file
    int numOfCoEditors = readFile(argv[1]);
    KolIsrael(numOfCoEditors);
    return 0;
}
