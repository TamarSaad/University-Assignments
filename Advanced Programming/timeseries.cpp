#include "timeseries.h"
#include <string.h>
#include <stdio.h>
#include <vector>
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>

using namespace std;

//constructor
TimeSeries::TimeSeries(const char *CSVfileName) {
    setName(CSVfileName);
    //extract the data from file to matrix
    setValuesOfFile();
}

//set the name of the file
void TimeSeries::setName(const char *name) {
    char *csvName = new char[strlen(name) + 1];
    strcpy(csvName, name);
    this->csvName = csvName;
}

const char *TimeSeries::getName() {
    return this->csvName;
}

//get the vector of the chracter's names
const vector<std::string> TimeSeries::getNamesOfChars() const {
    return this->NamesOfChars;
}

//read the data from the file and transfer it to a matrix
void TimeSeries::setValuesOfFile() {
    fstream fin;
    fin.open(this->getName(), ios::in);
    if (!fin.is_open()) {
        exit(EXIT_FAILURE);
    }
    vector<vector<float>> Data;
    std::string line;
    int count = 0;
    //read line after line from file
    while (getline(fin, line, '\n')) {
        //get the characters names
        if (count == 0) {
            std::istringstream iss(line);
            vector<string> names;
            std::string name;
            while (std::getline(iss, name, ',')) {
                names.push_back(name);
            }
            this->NamesOfChars = names;
            this->numOfColumns = names.size();
            Data.resize(this->numOfColumns);
            //get the digital data
        } else {
            std::istringstream iss(line);
            std::string num;
            int column = 0;
            while (getline(iss, num, ',')) {
                Data[column].push_back(stof(num));
                ++column;
            }
        }
        count++;
    }
    this->DataMat = Data;
    this->numOfRows = count - 1;
    fin.close();
}

vector<vector<float>> TimeSeries::getMat() const {
    return this->DataMat;
}

void TimeSeries::addRow(vector<float> row) {
    this->DataMat.push_back(row);
}


float TimeSeries::getValue(int character, string time) const {
    vector<string> strs = this->getNamesOfChars();
    std::vector<string>::iterator itr = std::find(strs.begin(), strs.end(), time);
    return this->getMat()[itr - strs.begin()][character];
}

int TimeSeries::getNumOfRows() const {
    return this->numOfRows;
}

int TimeSeries::getNumOfColumns() const {
    return this->numOfColumns;
}

TimeSeries::~TimeSeries() {
    delete this->csvName;
};





