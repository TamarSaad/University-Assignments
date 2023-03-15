

#ifndef TIMESERIES_H_
#define TIMESERIES_H_

#include <string.h>
#include <vector>
#include <string>


using namespace std;

class TimeSeries {

private:
    const char *csvName;
    vector<std::string> NamesOfChars;
    vector<vector<float>> DataMat;
    int numOfRows;
    int numOfColumns;

public:

    TimeSeries(const char *CSVfileName);

    void setName(const char *name);

    const char *getName();

    void setNamesOfChars();

    const vector<std::string> getNamesOfChars() const;

    void setValuesOfFile();

    vector<vector<float>> getMat() const;

    void addRow(vector<float>);

    float getValue(int character, string time) const;

    int getNumOfRows() const;

    int getNumOfColumns() const;

    ~TimeSeries();

};


#endif /* TIMESERIES_H_ */
