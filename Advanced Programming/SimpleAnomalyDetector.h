

#ifndef SIMPLEANOMALYDETECTOR_H_
#define SIMPLEANOMALYDETECTOR_H_

#include "anomaly_detection_util.h"
#include "AnomalyDetector.h"
#include <vector>
#include <algorithm>
#include <string.h>
#include <math.h>

struct correlatedFeatures {
    string feature1, feature2;  // names of the correlated features
    float corrlation;
    Line lin_reg;
    Point circleCenter = Point(0, 0);
    float threshold;
};


class SimpleAnomalyDetector : public TimeSeriesAnomalyDetector {
protected:
    vector<correlatedFeatures> cf;
    float minLinearCorrelation = 0.9;
public:
    SimpleAnomalyDetector();

    virtual ~SimpleAnomalyDetector();

    virtual void learnNormal(const TimeSeries &ts);

    virtual vector<AnomalyReport> detect(const TimeSeries &ts);

    vector<correlatedFeatures> getNormalModel() {
        return cf;
    }

    Point **fromFloatsToPoints(float *x, float *y, int size);

    float ThresholdCal(Line line, Point **points, int size);

    float *fromVecToPointerOfFloats(vector<float> vec);

    virtual void addCorrelation(Point **points, string feature1, string feature2, float correlation, int size);

    virtual void isAnomaly(correlatedFeatures cor, Point p, vector<AnomalyReport> &reports, long time);

    float getMinLinearCorrelation();

    void setMinLinearCorrelation(float f);


};


#endif /* SIMPLEANOMALYDETECTOR_H_ */
