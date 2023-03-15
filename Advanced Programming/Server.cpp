
#include "Server.h"

Server::Server(int port) throw(const char *) {
    fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0)
        throw "socket failed";
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(port);
    if (bind(fd, (struct sockaddr*) &server, sizeof(server)) < 0)
        throw "bind failed";
    if (listen(fd, 2) < 0)
        throw "listen failed";
}

void Server::start(ClientHandler &ch) throw(const char *) {
    this->t = new thread([&ch, this]() {
        for(int i=0; i<2; ++i) {
            socklen_t clientSize = sizeof(client);
            int aClient = accept(fd, (struct sockaddr *) &client, &clientSize);
            if (aClient < 0)
                throw "accept failed";
            ch.handle(aClient);
            close(aClient);
        }
        close(fd);
    });
}

void Server::stop() {
    t->join(); // do not delete this!
}


Server::~Server() {
    delete t;
}

