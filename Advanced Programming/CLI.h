
#ifndef CLI_H_
#define CLI_H_

#include <string.h>
#include "commands.h"
#include <map>

using namespace std;

class CLI {
    DefaultIO *dio;
    map<float, Command *> commands;
    SimpleAnomalyDetector *ad;
    // you can add data members
public:
    CLI(DefaultIO *dio);

    void start();

    void printMenu();

    virtual ~CLI();
};

#endif /* CLI_H_ */
