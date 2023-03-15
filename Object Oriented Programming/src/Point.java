/**
 * .
 */
public class Point {
    private double x;
    private double y;

    // constructor

    /**
     * @param x x
     * @param y y
     */
    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    /**
     * @param other other
     * @return distance -- return the distance of this point to the other point
     */
    public double distance(Point other) {
        double xx = Math.pow((this.x - other.getX()), 2);
        double yy = Math.pow((this.y - other.getY()), 2);
        double distance = Math.sqrt(xx + yy);
        return distance;
    }

    /**
     * @param other other
     * @return equals -- return true if the points are equal, false otherwise
     */
    public boolean equals(Point other) {
        if (this.x == other.x && this.y == other.y) {
            return true;
        }
        return false;
    }

    /**
     * @return Return the x and y values of this point
     */
    public double getX() {
        return this.x;
    }

    /**
     * @return .
     */
    public double getY() {
        return this.y;
    }
}