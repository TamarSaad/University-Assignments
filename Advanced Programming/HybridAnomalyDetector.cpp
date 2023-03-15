
#include "HybridAnomalyDetector.h"

HybridAnomalyDetector::HybridAnomalyDetector() {
    // TODO Auto-generated constructor stub

}

void HybridAnomalyDetector::addCorrelation(Point **points, string feature1, string feature2, float correlation,
                                           int size) {
    SimpleAnomalyDetector::addCorrelation(points, feature1, feature2, correlation, size);
    if (correlation >= this->minCircularCorrelation && correlation < this->minLinearCorrelation) {
        Circle circle = findMinCircle(points, size);
        struct correlatedFeatures cor;
        cor.feature1 = std::move(feature1);
        cor.feature2 = std::move(feature2);
        cor.corrlation = correlation;
        cor.lin_reg = Line(0, 0);
        cor.circleCenter = circle.center;
        cor.threshold = 1.1 * circle.radius;
        this->cf.push_back(cor);
    }
}

void HybridAnomalyDetector::isAnomaly(correlatedFeatures cor, Point p, vector<AnomalyReport> &reports, long time) {
    //if it is linear correlation
    if (cor.corrlation >= this->minLinearCorrelation) {
        SimpleAnomalyDetector::isAnomaly(cor, p, reports, time);
    }
        //if it's circle correlation
    else if (cor.corrlation >= this->minCircularCorrelation) {
        //if the point isn't inside the circle
        if (!isInCircle(p, Circle(cor.circleCenter, cor.threshold))) {
            reports.push_back(AnomalyReport(cor.feature1 + '-' + cor.feature2, time));
        }
    }
}

float HybridAnomalyDetector::getMinCircularCorrelation() {
    return this->minCircularCorrelation;
}

void HybridAnomalyDetector::setMinLinearCorrelation(float f) {
    this->minCircularCorrelation=f;
}

HybridAnomalyDetector::~HybridAnomalyDetector() {
    // TODO Auto-generated destructor stub
}


