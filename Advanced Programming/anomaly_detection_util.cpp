//
// Created by Tamar Saad on 31/10/2020.
// ID: 207256991
//
#include <math.h>
#include "anomaly_detection_util.h"

using namespace std;

float avg(float *x, int size) {
    float sum = 0;
    for (int i = 0; i < size; ++i) {
        sum += x[i];
    }
    float average = sum / size;
    return average;
}

float var(float *x, int size) {
    //calculate the average
    float average = avg(x, size);
    //calculate the variance
    float sum = 0;
    for (int j = 0; j < size; ++j) {
        sum += pow(x[j], 2);
    }
    float variance = sum / size;
    variance -= pow(average, 2);
    return variance;
}

float cov(float *x, float *y, int size) {
    float xaverage = avg(x, size);
    float yaverage = avg(y, size);
    float sum = 0;
    for (int i = 0; i < size; ++i) {
        sum += (x[i] - xaverage) * (y[i] - yaverage);
    }
    float covariance = sum / size;
    return covariance;
}

// returns the Pearson correlation coefficient of X and Y
float pearson(float *x, float *y, int size) {
    float sdx = sqrt(var(x, size));
    float sdy = sqrt(var(y, size));
    float pearson = cov(x, y, size) / (sdx * sdy);
    if (pearson > 0) {
        return pearson;
    }
    return -pearson;
}


// performs a linear regression and returns the line equation
Line linear_reg(Point **points, int size) {
    float *xarr = new float[size];
    float *yarr = new float[size];
    for (int i = 0; i < size; ++i) {
        xarr[i] = points[i]->x;
        yarr[i] = points[i]->y;
    }

    float a = cov(xarr, yarr, size) / var(xarr, size);
    float b = avg(yarr, size) - a * (avg(xarr, size));
    return Line(a, b);
}

// returns the deviation between point p and the line
float dev(Point p, Line l) {
    float liney = l.f(p.x);
    if (liney > p.y) {
        return liney - p.y;
    }
    return p.y - liney;
}

// returns the deviation between point p and the line equation of the points
float dev(Point p, Point **points, int size) {
    Line line = linear_reg(points, size);
    return dev(p, line);
}




