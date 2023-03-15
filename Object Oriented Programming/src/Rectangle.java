
/**
 * The type Rectangle.
 */
public class Rectangle {
    private Point upperLeft;
    private Point bottomRight;
    private double width;
    private double height;

    // Create a new rectangle with location and width/height.

    /**
     * Instantiates a new Rectangle.
     *
     * @param upperLeft u
     * @param width     w
     * @param height    h                  constructor
     */
    public Rectangle(Point upperLeft, double width, double height) {
        this.upperLeft = upperLeft;
        this.bottomRight = new Point(upperLeft.getX() + width, upperLeft.getY() + height);
        this.width = width;
        this.height = height;
    }

    // Return a (possibly empty) List of intersection points
    // with the specified line.

    /**
     * Intersection points java . util . list.
     *
     * @param line l
     * @return a list of Points
     */
    public java.util.List<Point> intersectionPoints(Line line) {
        //creating an array list of points
        java.util.List<Point> intersections = new java.util.ArrayList<Point>();
        double lx = this.getUpperLeft().getX();
        double ly = this.getUpperLeft().getY();
        Line[] lines = new Line[4];
        lines[0] = new Line(lx, ly, lx, this.getBottomRight().getY());
        lines[1] = new Line(lx, ly, this.getBottomRight().getX(), ly);
        lines[2] = new Line(this.getBottomRight().getX(), ly,
                this.getBottomRight().getX(), this.getBottomRight().getY());
        lines[3] = new Line(lx, this.getBottomRight().getY(),
                this.getBottomRight().getX(), this.getBottomRight().getY());
        for (Line i : lines) {
            Point point = line.intersectionWith(i);
            if (point != null) {
                intersections.add(point);
                // System.out.println(point.getY());
            }
        }
        return intersections;
    }

    // Return the width and height of the rectangle

    /**
     * Gets width.
     *
     * @return width width
     */
    public double getWidth() {
        return this.width;
    }

    /**
     * Gets height.
     *
     * @return height height
     */
    public double getHeight() {
        return this.height;
    }


    /**
     * Gets upper left.
     *
     * @return the upper-left point of the rectangle.
     */
    public Point getUpperLeft() {
        return this.upperLeft;
    }

    /**
     * Gets bottom right.
     *
     * @return the bottom right point of the rectangle
     */
    public Point getBottomRight() {
        return this.bottomRight;
    }
}