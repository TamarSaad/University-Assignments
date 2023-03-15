/*
 * Server.h
 *
 *     Author: Tamar Saad 207256991
 */

#ifndef SERVER_H_
#define SERVER_H_

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>
#include <thread>
#include <string.h>
#include "CLI.h"
#include <signal.h>

using namespace std;

using namespace std;

// edit your ClientHandler interface here:
class ClientHandler {
public:
    virtual void handle(int clientID) = 0;
};


// you can add helper classes here and implement on the cpp file
class SocketIO : public DefaultIO {
private:
    int clientID;
public:
    SocketIO(int id) : clientID(id) {}

    string read() override {
        string str = "";
        char letter;
        while (true) {
            recv(clientID, &letter, 1, 0);
            if (letter == '\n')
                break;
            str.append(&letter);
        }
        return str;
    }

    void write(string text) override {
        send(clientID, text.c_str(), text.size(), 0);
    }

    void write(float f) override {
        std::ostringstream oss;
        oss << f;
        write(oss.str());
    }

    void read(float *f) override {
        string str = read();
        *f = stof(str);
    }

};

// edit your AnomalyDetectionHandler class here
class AnomalyDetectionHandler : public ClientHandler {
private:
    CLI* cli;
    SocketIO* sio;
public:
    AnomalyDetectionHandler(){}
    virtual void handle(int clientID)  {
        sio = new SocketIO(clientID);
        cli = new CLI(sio);
        cli->start();
    }
    ~AnomalyDetectionHandler() {
        delete sio;
        delete cli;
    }
};


// implement on Server.cpp
class Server {
private:
    thread *t; // the thread to run the start() method in
    int fd;
    sockaddr_in server;
    sockaddr_in client;
    // you may add data members

public:
    Server(int port) throw(const char *);

    virtual ~Server();

    void start(ClientHandler &ch) throw(const char *);

    void stop();
};


#endif /* SERVER_H_ */
