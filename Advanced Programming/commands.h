#ifndef COMMANDS_H_
#define COMMANDS_H_

#include<iostream>
#include <string.h>
#include <sstream>
#include <fstream>
#include <vector>
#include <iomanip>
#include "HybridAnomalyDetector.h"

using namespace std;

class DefaultIO {
public:
    virtual string read() = 0;

    virtual void write(string text) = 0;

    virtual void write(float f) = 0;

    virtual void read(float *f) = 0;

    virtual ~DefaultIO() {}
};

struct ContinuesAnomaly {
    long start;
    long end;
    string description;
};

class Data {
public:
    DefaultIO *dio;
    TimeSeries *train;
    TimeSeries *test;
    SimpleAnomalyDetector *anomalyDetector;
    vector<AnomalyReport> reports;
    vector<ContinuesAnomaly> continuesAnomalies;

    Data(DefaultIO *dio, SimpleAnomalyDetector *ad) : dio(dio), anomalyDetector(ad) {}

    ~Data() {
        delete train;
        delete test;
    }
};

class Command {
protected:
    Data *data;
public:
    string Description;

    Command(Data *d) : data(d) {}

    virtual void execute() = 0;

    virtual ~Command() {}
};

class UploadCommand : public Command {
public:
    UploadCommand(Data *data) : Command(data) {
        Command::Description = "upload a time series csv file";
    }

    void execute() override {
        AskForUpload("train", "anomalyTrain.csv");
        this->data->train = new TimeSeries("anomalyTrain.csv");
        AskForUpload("test", "anomalyTest.csv");
        this->data->test = new TimeSeries("anomalyTest.csv");
    }

    void AskForUpload(string type, string name) {
        string s = "Please upload your local ";
        s.append(type).append(" CSV file.\n");
        this->data->dio->write(s);
        CreateCSV(name);
        this->data->dio->write("Upload complete.\n");
    }

    void CreateCSV(string name) {
        ofstream out(name);
        string line;
        line = this->data->dio->read();
        while (line != "done") {
            out << line << endl;
            line = this->data->dio->read();
        }
        out.close();
    }
};

class SettingsCommand : public Command {
public:
    SettingsCommand(Data *data) : Command(data) {
        Command::Description = "algorithm settings";
    }

    void execute() override {
        string s = "The current correlation threshold is ";
        s.append(to_string(this->data->anomalyDetector->getMinLinearCorrelation())).append("\n");
        this->data->dio->write(s);
        float *threshold = new float;
        while (true) {
            this->data->dio->write("Type a new threshold.\n");
            this->data->dio->read(threshold);
            if (*threshold >= 0 && *threshold <= 1)
                break;
            this->data->dio->write("please choose a value between 0 and 1.\n");
        }
        this->data->anomalyDetector->setMinLinearCorrelation(*threshold);
        delete threshold;
    }
};

class AnomalyDetectionCommand : public Command {
public:
    AnomalyDetectionCommand(Data *data) : Command(data) {
        Command::Description = "detect anomalies";
    }

    void execute() override {
        this->data->anomalyDetector->learnNormal(*this->data->train);
        this->data->reports = this->data->anomalyDetector->detect(*this->data->test);
        this->data->dio->write("anomaly detection complete.\n");
    }
};

class DisplayResultsCommand : public Command {
public:
    DisplayResultsCommand(Data *data) : Command(data) {
        Command::Description = "display results";
    }

    void execute() override {
        vector<AnomalyReport> *ar = &this->data->reports;
        if (ar != nullptr) {
            for (AnomalyReport &report : *ar) {
                string str = to_string(report.timeStep).append("\t").append(report.description).append("\n");
                this->data->dio->write(str);
            }
        }
        this->data->dio->write("Done.\n");
    }
};

class UploadAnomaliesCommand : public Command {
public:
    UploadAnomaliesCommand(Data *data) : Command(data) {
        Command::Description = "upload anomalies and analyze results";
    }

    void createContinuesAnomaly() {
        if (!this->data->continuesAnomalies.empty())
            return;
        vector<AnomalyReport> ar = this->data->reports;
        long start = ar[0].timeStep, end = ar[0].timeStep;
        string description = ar[0].description;
        for (int i = 1; i < ar.size(); ++i) {
            while (ar[i].timeStep == ar[i - 1].timeStep + 1 && ar[i].description == ar[i - 1].description&&i<ar.size()) {
                end = ar[i].timeStep;
                ++i;
            }
            ContinuesAnomaly ca = ContinuesAnomaly{start, end, ar[i - 1].description};
            this->data->continuesAnomalies.push_back(ca);
            if(i<ar.size()) {
                start = ar[i].timeStep;
                description = ar[i].description;
            }
        }
    }

    vector<ContinuesAnomaly> acceptAnomalies() {
        vector<ContinuesAnomaly> acceptedAnomalies;
        string line = this->data->dio->read();
        while (line != "done") {
            std::istringstream iss(line);
            vector<string> numbers;
            std::string number;
            while (std::getline(iss, number, ',')) {
                numbers.push_back(number);
            }
            ContinuesAnomaly ca = ContinuesAnomaly{std::stol(numbers[0]), std::stol(numbers[1]), ""};
            acceptedAnomalies.push_back(ca);
            line = this->data->dio->read();
        }
        this->data->dio->write("Upload complete.\n");
        return acceptedAnomalies;
    }

    long getNValue(vector<ContinuesAnomaly> aa) {
        long n = (long)this->data->test->getNumOfRows();
        for (int i = 0; i < aa.size(); ++i) {
            n -= (aa[i].end - aa[i].start + 1);
        }
        return n;
    }

    bool aOverlapB(ContinuesAnomaly a, ContinuesAnomaly b) {
        if ((a.start >= b.start && a.start <= b.end)
            || (a.end >= b.start &&a.end <= b.end))
            return true;
        return false;
    }

    bool isOverlap(ContinuesAnomaly a, ContinuesAnomaly b) {
        if (aOverlapB(a, b) || aOverlapB(b, a))
            return true;
        return false;
    }

    void compareAnomalies(vector<ContinuesAnomaly> aa) {
        long tp = 0, fp = 0;
        bool detected;
        vector<ContinuesAnomaly> ca = this->data->continuesAnomalies;
        for (int i = 0; i < ca.size(); ++i) {
            detected = false;
            for (int j = 0; j < aa.size(); ++j) {
                if (isOverlap(ca[i], aa[j])) {
                    detected = true;
                }
            }
            if (detected) {
                tp += 1;
            } else {
                fp += 1;
            }
        }
        long n = getNValue(aa);
        long truePositiveRate = (float)tp / (float) aa.size() *1000;
        long falseAlarmRate = (float)fp / (float)n *1000;
        float tpr= (float)truePositiveRate/1000, far=(float)falseAlarmRate/1000;
        std::stringstream ss;
        ss  << std::setprecision(3) <<std::noshowpoint << tpr;
        std::string mystring = ss.str();
        string line = "True Positive Rate: ";
        line.append(mystring.append("\n"));
        this->data->dio->write(line);
        std::stringstream sa;
        sa << std::setprecision(3) << std::noshowpoint <<far;
        mystring = sa.str();
         line = "False Positive Rate: ";
        line.append(mystring.append("\n"));
        this->data->dio->write(line);
    }

    void execute() override {
        createContinuesAnomaly();
        this->data->dio->write("Please upload your local anomalies file.\n");
        vector<ContinuesAnomaly> acceptedAnomalies = acceptAnomalies();
        compareAnomalies(acceptedAnomalies);
    }
};

class ExitCommand : public Command {
public:
    ExitCommand(Data *data) : Command(data) {
        Command::Description = "exit";
    }

    void execute() override {
    }
};

#endif /* COMMANDS_H_ */
