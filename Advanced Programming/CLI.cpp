#include "CLI.h"

CLI::CLI(DefaultIO *dio) : dio(dio) {
    this->ad = new HybridAnomalyDetector;
    Data *data = new Data(dio, ad);
    this->commands.insert(std::pair<float, Command *>(1, new UploadCommand(data)));
    this->commands.insert(std::pair<float, Command *>(2, new SettingsCommand(data)));
    this->commands.insert(std::pair<float, Command *>(3, new AnomalyDetectionCommand(data)));
    this->commands.insert(std::pair<float, Command *>(4, new DisplayResultsCommand(data)));
    this->commands.insert(std::pair<float, Command *>(5, new UploadAnomaliesCommand(data)));
    this->commands.insert(std::pair<float, Command *>(6, new ExitCommand(data)));
}

void CLI::start() {
    string choice;
    float f;
    do {
        printMenu();
        choice = this->dio->read();
        f = std::stof(choice);
        if(f>=1 && f <= this->commands.size())
        this->commands.at(f)->execute();
    } while (f != this->commands.size());
}

void CLI::printMenu() {
    this->dio->write("Welcome to the Anomaly Detection Server.\nPlease choose an option:\n");
    for (int i = 1; i <= this->commands.size(); ++i) {
        string str = std::to_string(i);
        str.append(".").append(this->commands.at(i)->Description).append("\n");
        this->dio->write(str);
    }
}

CLI::~CLI() {
    for (int i = 1; i <= commands.size(); i++) {
        delete commands.at(i);
    }
    delete this->ad;
}

