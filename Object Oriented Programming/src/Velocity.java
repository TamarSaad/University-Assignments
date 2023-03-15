/**
 * Velocity specifies the change in position on the `x` and the `y` axes.
 */
public class Velocity {
    private double dx;
    private double dy;

    /**
     * @param dx x
     * @param dy constructor
     */
    public Velocity(double dx, double dy) {
        this.dx = dx;
        this.dy = dy;
    }

    /**
     * @param angle a
     * @param speed s
     * @return get an angel and a speed and turns it into a velocity
     */
    public static Velocity fromAngleAndSpeed(double angle, double speed) {
        double dx = speed * Math.sin(Math.toRadians(angle));
        double dy = speed * Math.cos(Math.toRadians(angle));
        return new Velocity(dx, -dy);
    }

    /**
     * @return return the dx and dy values of velocity
     */
    public double getX() {
        return this.dx;
    }

    /**
     * @return r
     */
    public double getY() {
        return this.dy;
    }

    /**
     * @param p p
     * @return Take a point with position (x,y) and return a new point
     * with position (x+dx, y+dy)
     */
    public Point applyToPoint(Point p) {
        return new Point((p.getX() + this.dx), (p.getY() + this.dy));
    }

}