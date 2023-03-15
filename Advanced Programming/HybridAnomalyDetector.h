

#ifndef HYBRIDANOMALYDETECTOR_H_
#define HYBRIDANOMALYDETECTOR_H_

#include "SimpleAnomalyDetector.h"
#include "minCircle.h"

class HybridAnomalyDetector : public SimpleAnomalyDetector {
protected:
    float minCircularCorrelation = 0.5;
public:
    HybridAnomalyDetector();

    ~HybridAnomalyDetector();

    virtual void addCorrelation(Point **points, string feature1, string feature2, float correlation,
                                int size);

    void isAnomaly(correlatedFeatures cor, Point p, vector<AnomalyReport> &reports, long time);
    float getMinCircularCorrelation();
    void setMinLinearCorrelation(float f);

};

#endif /* HYBRIDANOMALYDETECTOR_H_ */
