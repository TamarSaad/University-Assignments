/**
 *
 */
public class Line {

    private Point start;
    private Point end;

    // constructors

    /**
     * @param start start
     * @param end   end
     */
    public Line(Point start, Point end) {
        this.start = start;
        this.end = end;
    }

    /**
     * @param x1 x
     * @param y1 y
     * @param x2 x
     * @param y2 y
     */
    public Line(double x1, double y1, double x2, double y2) {
        this.start = new Point(x1, y1);
        this.end = new Point(x2, y2);
    }

    /**
     * @return Return the length of the line
     */
    public double length() {
        double xx = Math.pow((this.start.getX() - this.end.getX()), 2);
        double yy = Math.pow((this.start.getY() - this.end.getY()), 2);
        double distance = Math.sqrt(xx + yy);
        return distance;
    }

    /**
     * @return Returns the middle point of the line
     */
    public Point middle() {
        double x, y;
        x = (this.start.getX() + this.end.getX()) / 2;
        y = (this.start.getY() + this.end.getY()) / 2;
        Point middle = new Point(x, y);
        return middle;
    }

    /**
     * @return Returns the start point of the line
     */
    public Point start() {
        return this.start;
    }

    /**
     * @return Returns the end point of the line
     */
    public Point end() {
        return this.end;
    }

    /**
     * @param other other
     * @return Returns true if the lines intersect, false otherwise
     */
    public boolean isIntersecting(Line other) {
        //check if the lines are equal
        if (equals(other)) {
            return false;
        }
        //checks the difference between the slopes
        double slope = slopeCal(other);
        //if the slopes are the same
        if (slope == 0) {
            //if the start point of one line equals the end point of the other
            if (this.start.equals(other.end) || this.end.equals(other.start)
                    || other.start.equals(this.end) || other.end.equals(this.start)) {
                return true;
            }
            return false;
        }

        //check for interaction point
        Point intersection = interactionPoint(other, slope);
        //checks if point is in rage
        if (isInRage(intersection, other)) {
            return true;
        }
        return false;

    }

    /**
     * @param other other
     * @return calcolate the difference between 2 slopes
     */
    public double slopeCal(Line other) {
        double slope =
                ((this.start.getX() - this.end.getX()) * (other.start.getY() - other.end.getY()))
                        - ((this.start.getY() - this.end.getY()) * (other.start.getX() - other.end.getX()));
        return slope;
    }

    /**
     * @param other other
     * @param slope slope
     * @return calculate the intersection point of the 2 lines.
     * Yet, the point might not be in the lines range
     */

    public Point interactionPoint(Line other, double slope) {
        //giving simpler names
        double x1, x2, x3, x4, y1, y2, y3, y4;
        x1 = this.start.getX();
        x2 = this.end.getX();
        x3 = other.start.getX();
        x4 = other.end.getX();
        y1 = this.start.getY();
        y2 = this.end.getY();
        y3 = other.start.getY();
        y4 = other.end.getY();
        double px, py;
        //calculate the intersection point
        px = (((x1 * y2 - y1 * x2) * (x3 - x4)) - (x1 - x2) * (x3 * y4 - y3 * x4)) / slope;
        py = (((x1 * y2 - y1 * x2) * (y3 - y4)) - (y1 - y2) * (x3 * y4 - y3 * x4)) / slope;
        Point intersection = new Point(px, py);
        return intersection;
    }

    /**
     * @param intersection intersection
     * @param other        other
     * @return check if the intersection point is in the lines range
     */
    public boolean isInRage(Point intersection, Line other) {
        double epsilon = Math.pow(10, -13);
        //if the distance between the intersection point to the middle point equals or smaller
        //than the line's length- it is in the line's range
        if ((intersection.distance(this.middle()) <= this.length() * 0.5 + epsilon)
                && intersection.distance(other.middle()) <= other.length() * 0.5 + epsilon) {
            return true;
        }
        return false;
    }

    /**
     * @param other other
     * @return Returns the intersection point if the lines intersect,
     * and null otherwise.
     */

    public Point intersectionWith(Line other) {
        //check if the lines are equal
        if (equals(other)) {
            return null;
        }
        double epsilon = 0.1;
        //checks the difference between the slopes
        double slope = slopeCal(other);
        if (Math.abs(slope) <= epsilon) {
            //if the slopes are the same, maybe one line's start is the other's end
            if (this.start.equals(other.end) || this.start.equals(other.start)) {
                return this.start;
            }
            if (this.end.equals(other.start) || this.end.equals((other.end))) {
                return this.end;
            } else {
                return null;
            }
        }

        //check for interaction point
        Point intersection = interactionPoint(other, slope);
        //checks if point is in rage
        if (isInRage(intersection, other)) {
            return intersection;
        } else {
            return null;
        }


    }

    /**
     * @param other other
     * @return equals -- return true is the lines are equal, false otherwise
     */
    public boolean equals(Line other) {
        if (this.start.getX() == other.start.getX() && this.end.getX() == other.end.getX()
                && this.start.getY() == other.start.getY() && this.end.getY() == other.end.getY()) {
            return true;
        }
        return false;

    }

    // If this line does not intersect with the rectangle, return null.
    // Otherwise, return the closest intersection point to the
    // start of the line.

    /**
     * @param rect r
     * @return point
     */
    public Point closestIntersectionToStartOfLine(Rectangle rect) {
        Line line = new Line(this.start, this.end);
        java.util.List<Point> points = rect.intersectionPoints(line);
        if (points.isEmpty()) {
            return null;
        }
        Point intersection = null;
        double dmin = 1000.0;
        for (Point p : points) {
            double d = this.start.distance(p);
            if (dmin > d) {
                dmin = d;
                intersection = p;
            }
        }

        return intersection;

    }
}