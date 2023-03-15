import biuoop.DrawSurface;

import java.awt.Color;

/**
 * The type Ball.
 */
public class Ball implements Sprite {
    private Point point;
    private int r;
    private Color color;
    private Velocity velocity;
    private GameEnvironment gameEnviroment;

    /**
     * Instantiates a new Ball.
     *
     * @param point the point
     * @param r     the r
     * @param color the color
     */
    public Ball(Point point, int r, Color color) {
        this.point = new Point((int) point.getX(), (int) point.getY());
        this.r = r;
        this.color = color;
    }

    /**
     * Instantiates a new Ball.
     *
     * @param x     the x
     * @param y     the y
     * @param r     the r
     * @param color the color
     */
    public Ball(int x, int y, int r, Color color) {
        this.point = new Point(x, y);
        this.r = r;
        this.color = color;
    }

    /**
     * Gets x.
     *
     * @return the x
     */
    public int getX() {
        return (int) this.point.getX();
    }

    /**
     * Gets y.
     *
     * @return the y
     */
    public int getY() {
        return (int) this.point.getY();
    }

    /**
     * Gets size.
     *
     * @return the size
     */
    public int getSize() {
        return this.r;
    }

    /**
     * Gets color.
     *
     * @return the color
     */
    public Color getColor() {
        return this.color;
    }

    /**
     * Gets scope.
     *
     * @return the scope
     */
    public double getScope() {
        return this.r * 2 * Math.PI;
    }

    /**
     * Gets area.
     *
     * @return the area
     */
    public double getArea() {
        return this.r * this.r * Math.PI;
    }

    /**
     * @param surface draw the ball on the given DrawSurface
     */
    public void drawOn(DrawSurface surface) {
        surface.setColor(this.color);
        surface.fillCircle(this.getX(), this.getY(), this.r);
    }

    /**
     * Sets velocity.
     *
     * @param dx the dx
     * @param dy the dy
     */
    public void setVelocity(double dx, double dy) {
        this.velocity = new Velocity(dx, dy);
    }

    /**
     * Gets velocity.
     *
     * @return the velocity
     */
    public Velocity getVelocity() {
        return this.velocity;
    }

    /**
     * Sets velocity.
     *
     * @param v the v
     */
    public void setVelocity(Velocity v) {
        this.velocity = v;
    }

    /**
     * Gets game environment.
     *
     * @return the game environment
     */
    public GameEnvironment getGameEnvironment() {
        return this.gameEnviroment;
    }

    /**
     * Sets game environment.
     *
     * @param ge the ge
     */
    public void setGameEnvironment(GameEnvironment ge) {
        this.gameEnviroment = ge;
    }

    /**
     * Move one step.
     *
     * @param left  the left
     * @param down  the down
     * @param right the right
     * @param up    the up
     */
    public void moveOneStep(int left, int down, int right, int up) {
        //if the x is out of borders
        //change diraction
        if ((this.point.getX() + this.r + this.getVelocity().getX()) > right
                || (this.point.getX() - this.r + this.getVelocity().getX() < left)) {
            this.setVelocity(-this.getVelocity().getX(), this.getVelocity().getY());
        }
        //if y is out of borders
        //change direction
        if ((this.point.getY() + this.r + this.getVelocity().getY()) > up
                || (this.point.getY() - this.r + this.getVelocity().getY()) < down) {
            this.setVelocity(this.getVelocity().getX(), -this.getVelocity().getY());
        }
        this.point = this.getVelocity().applyToPoint(this.point);
    }

    /**
     * move the ball one step, according to its velocity and collides.
     */
    private void moveOneStep() {
        //define the trajectory of the ball
        Point target = new Point(this.getVelocity().getX() + this.point.getX(),
                this.getVelocity().getY() + this.point.getY());
        Line trajectory = new Line(this.point, target);
        //get the closest collision, if exist
        CollisionInfo collision = this.gameEnviroment.getClosestCollision(trajectory);
        //if there is a collision, calls to hit in order to change velocity
        //and get the ball to the collision point
        if (collision != null) {
            Velocity newv = collision.collisionObject().hit(this, collision.collisionPoint(), this.getVelocity());
            this.setVelocity(newv);
        }
        //moving the ball

        this.point = this.getVelocity().applyToPoint(this.point);
    }

    /**
     * calls the moveOneStep method.
     */
    @Override
    public void timePassed() {
        this.moveOneStep();
    }

    /**
     * @param gameLevel adds the ball to the game class, as sprite
     */
    public void addToGame(GameLevel gameLevel) {
        gameLevel.addSprite(this);
    }

    /**
     * Remove from game.
     *
     * @param gameLevel the game level
     */
    public void removeFromGame(GameLevel gameLevel) {
        gameLevel.removeSprite(this);
    }


}
