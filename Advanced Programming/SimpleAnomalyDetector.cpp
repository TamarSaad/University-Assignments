
#include "SimpleAnomalyDetector.h"
#include "anomaly_detection_util.h"
#include "sstream"
#include "fstream"
#include <utility>
#include <vector>
#include <iostream>


SimpleAnomalyDetector::SimpleAnomalyDetector() {
    // TODO Auto-generated constructor stub

}

SimpleAnomalyDetector::~SimpleAnomalyDetector() {
    // TODO Auto-generated destructor stub

}


void SimpleAnomalyDetector::learnNormal(const TimeSeries &ts) {
    vector<vector<float>> source = ts.getMat();
    vector<vector<float>> target;

    //fill the correlations matrix with 0
    for (int i = 0; i < ts.getNumOfColumns(); ++i) {
        vector<float> vec;
        vec.assign(ts.getNumOfColumns(), 0);
        target.push_back(vec);
    }
    //checks pearsons and puts them in test, in upper triangular matrix form
    for (int i = 0; i < ts.getNumOfColumns() - 1; ++i) {
        for (int j = i + 1; j < ts.getNumOfColumns(); ++j) {
            target[i][j] = pearson(fromVecToPointerOfFloats(source[i]), fromVecToPointerOfFloats(source[j]),
                                   ts.getNumOfRows());
            string feature1 = ts.getNamesOfChars()[i];
            string feature2 = ts.getNamesOfChars()[j];
            int size = ts.getNumOfRows();
            float *fl1 = fromVecToPointerOfFloats(source[i]);
            float *fl2 = fromVecToPointerOfFloats(source[j]);
            Point **points = fromFloatsToPoints(fl1, fl2, ts.getNumOfRows());
            //add the correlation to the structs, if needed
            addCorrelation(points, feature1, feature2, target[i][j], size);
            for (int t = 0; t < ts.getNumOfRows(); ++t) {
                delete points[t];
            }
            delete[] points;
            delete fl1;
            delete fl2;
        }
    }
}

void
SimpleAnomalyDetector::addCorrelation(Point **points, string feature1, string feature2, float correlation, int size) {
    if (correlation >= this->minLinearCorrelation) {
        struct correlatedFeatures cor;
        cor.feature1 = std::move(feature1);
        cor.feature2 = std::move(feature2);
        cor.corrlation = correlation;
        cor.lin_reg = linear_reg(points, size);
        cor.threshold = ThresholdCal(cor.lin_reg, points, size);
        this->cf.push_back(cor);
    }
}

float *SimpleAnomalyDetector::fromVecToPointerOfFloats(vector<float> vec) {
    float *arr = new float[vec.size()];
    for (int i = 0; i < vec.size(); ++i) {
        arr[i] = vec[i];
    }
    return arr;
}

Point **SimpleAnomalyDetector::fromFloatsToPoints(float *x, float *y, int size) {
    Point **points = new Point *[size];
    for (int i = 0; i < size; ++i) {
        points[i] = new Point(x[i], y[i]);
    }
    return points;
}

float SimpleAnomalyDetector::ThresholdCal(Line line, Point **points, int size) {
    float max = 0;
    for (int i = 0; i < size; ++i) {
        float dis = dev(*points[i], line);
        if (max < dis) {
            max = dis;
        }
    }
    return 1.1 * max;
}


vector<AnomalyReport> SimpleAnomalyDetector::detect(const TimeSeries &ts) {
    vector<AnomalyReport> reports;
    //going over all correlations
    for (int i = 0; i < this->getNormalModel().size(); ++i) {
        struct correlatedFeatures cor = this->getNormalModel()[i];
        //for each correlation- checking all the anomalies
        for (int j = 0; j < ts.getNumOfRows(); ++j) {
            //create a point and checks the distance between it and the line
            Point p = Point(ts.getValue(j, cor.feature1), ts.getValue(j, cor.feature2));
            isAnomaly(cor, p, reports, j + 1);
        }
    }
    return reports;
}

void SimpleAnomalyDetector::isAnomaly(correlatedFeatures cor, Point p, vector<AnomalyReport> &reports, long time) {
    if (dev(p, cor.lin_reg) > cor.threshold) {
        reports.push_back(AnomalyReport(cor.feature1 + '-' + cor.feature2, time));
    }
}

float SimpleAnomalyDetector::getMinLinearCorrelation() {
    return this->minLinearCorrelation;
}

void SimpleAnomalyDetector::setMinLinearCorrelation(float f) {
    this->minLinearCorrelation = f;
}

