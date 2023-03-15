// 20725699    20701609

#ifndef MINCIRCLE_H_
#define MINCIRCLE_H_

#include <iostream>
#include <vector>
#include <math.h>
#include "anomaly_detection_util.h"

using namespace std;



class Circle {
public:
    Point center;
    float radius;

    Circle(Point c, float r) : center(c), radius(r) {}
};


float distance(Point a, Point b);

bool isInCircle(Point p, Circle c);

Point middlePoint(Point a, Point b);

Circle findCircle(Point &point1, Point &point2);

Circle findCircle(Point &point1, Point &point2, Point &point3);

Circle trivialCircle(vector<Point> outsidePoints);

Circle welzl(Point **points, vector<Point> boundaryPoints, size_t size);

Circle findMinCircle(Point **points, size_t size);

#endif /* MINCIRCLE_H_ */
