#include "minCircle.h"


float distance(Point a, Point b) {
    float x = pow(a.x - b.x, 2);
    float y = pow(a.y - b.y, 2);
    return sqrt(x + y);
}

bool isInCircle(Point p, Circle c) {
    if (distance(c.center, p) > c.radius) {
        return false;
    }
    return true;
}

Point middlePoint(Point a, Point b) {
    float x = (a.x + b.x) / 2;
    float y = (a.y + b.y) / 2;
    return Point(x, y);
}

Circle findCircle(Point &point1, Point &point2) {
    return Circle(middlePoint(point1, point2), distance(point1, point2) / 2);
}

Circle findCircle(Point &point1, Point &point2, Point &point3) {
    // try to make a circle from 2 points
    Circle circle = findCircle(point1, point2);
    if (isInCircle(point3, circle))
        return circle;
    circle = findCircle(point2, point3);
    if (isInCircle(point1, circle))
        return circle;
    circle = findCircle(point3, point1);
    if (isInCircle(point2, circle))
        return circle;
    // make circle from 3 points
    float A = point1.x * (point2.y - point3.y) - point1.y * (point2.x - point3.x) + point2.x * point3.y -
              point3.x * point2.y;
    float B = (pow(point1.x, 2) + pow(point1.y, 2)) * (point3.y - point2.y) +
              (pow(point2.x, 2) + pow(point2.y, 2)) * (point1.y - point3.y) +
              (pow(point3.x, 2) + pow(point3.y, 2)) * (point2.y - point1.y);
    float C = (pow(point1.x, 2) + pow(point1.y, 2)) * (point2.x - point3.x) +
              (pow(point2.x, 2) + pow(point2.y, 2)) * (point3.x - point1.x) +
              (pow(point3.x, 2) + pow(point3.y, 2)) * (point1.x - point2.x);
    Point middlePoint = Point((-1 * B) / (2 * A), (-1 * C) / (2 * A));
    float radius = distance(middlePoint, point1);
    return Circle(middlePoint, radius);
}

Circle trivialCircle(vector<Point> outsidePoints) {
    if (outsidePoints.size() == 0)
        return Circle(Point(0, 0), 0);
    if (outsidePoints.size() == 1)
        return Circle(outsidePoints[0], 0);
    if (outsidePoints.size() == 2)
        return findCircle(outsidePoints[0], outsidePoints[1]);
    if (outsidePoints.size() == 3)
        return findCircle(outsidePoints[0], outsidePoints[1], outsidePoints[2]);
}

Circle welzl(Point **points, vector<Point> boundaryPoints, size_t size) {
    if (size == 0 || boundaryPoints.size() == 3) {
        return trivialCircle(boundaryPoints);
    }
    Circle circle = welzl(points, boundaryPoints, size - 1);
    if (isInCircle(*points[size - 1], circle)) {
        return circle;
    }
    boundaryPoints.push_back(*points[size - 1]);
    return welzl(points, boundaryPoints, size - 1);
}

Circle findMinCircle(Point **points, size_t size) {
    vector<Point> boundaryPoints;
    return welzl(points, boundaryPoints, size);
}
