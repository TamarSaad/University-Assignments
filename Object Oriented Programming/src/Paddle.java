import biuoop.DrawSurface;
import biuoop.KeyboardSensor;

import java.awt.Color;

/**
 * The type Paddle.
 */
public class Paddle implements Sprite, Collidable {
    private Rectangle paddle;
    private biuoop.KeyboardSensor keyboard;
    private int speed;

    /**
     * Instantiates a new Paddle.
     *
     * @param r     the r
     * @param gui   the gui
     * @param speed the speed
     */
    public Paddle(Rectangle r, biuoop.GUI gui, int speed) {
        this.paddle = r;
        this.keyboard = gui.getKeyboardSensor();
        this.speed = speed;
    }

    /**
     * move the paddle to the left, in case the user press the left button.
     */
    private void moveLeft() {
        if (this.paddle.getUpperLeft().getX() - this.speed >= 0) {
            this.paddle = new Rectangle(new Point(
                    this.paddle.getUpperLeft().getX() - this.speed, this.paddle.getUpperLeft().getY()),
                    this.paddle.getWidth(), this.paddle.getHeight());
        }
    }

    /**
     * move the paddle to the right, in case the user press the right button.
     */
    private void moveRight() {
        if (this.paddle.getBottomRight().getX() + this.speed <= 800) {
            this.paddle = new Rectangle(new Point(
                    this.paddle.getUpperLeft().getX() + this.speed, this.paddle.getUpperLeft().getY()),
                    this.paddle.getWidth(), this.paddle.getHeight());
        }
    }

    /**
     * calls the move methods in the class.
     */
    @Override
    public void timePassed() {
        if (keyboard.isPressed(KeyboardSensor.LEFT_KEY)) {
            this.moveLeft();
        }
        if (keyboard.isPressed(KeyboardSensor.RIGHT_KEY)) {
            this.moveRight();
        }
    }

    /**
     * @param d drawsurface
     *          draw the paddle on the board
     */
    @Override
    public void drawOn(DrawSurface d) {
        //draw a black frame
        d.setColor(Color.black);
        d.drawRectangle((int) this.paddle.getUpperLeft().getX(), (int) this.paddle.getUpperLeft().getY(),
                (int) this.paddle.getWidth(), (int) this.paddle.getHeight());
        //paint the rectangle with color
        d.setColor(Color.orange);
        d.fillRectangle((int) this.paddle.getUpperLeft().getX(), (int) this.paddle.getUpperLeft().getY(),
                (int) this.paddle.getWidth(), (int) this.paddle.getHeight());
    }

    /**
     * @return rectangle
     */
    @Override
    public Rectangle getCollisionRectangle() {
        return this.paddle;
    }

    /**
     * @param collisionPoint  c
     * @param currentVelocity c
     * @return velocity
     * in case a ball hits the paddle, its velocity will change according to the place it landed on the paddle
     */
    @Override
    public Velocity hit(Ball hitter, Point collisionPoint, Velocity currentVelocity) {
        double px = this.paddle.getUpperLeft().getX();
        //the upper line of the rectangle
        Line line = new Line(this.paddle.getUpperLeft(),
                new Point(px + this.paddle.getWidth(), this.paddle.getUpperLeft().getY()));
        Velocity newVelocity = null;
        //make 5 different areas on the paddle
        double area = line.length() / 5;
        //the speed remains constant
        double speed = Math.sqrt(Math.pow(currentVelocity.getX(), 2) + Math.pow(currentVelocity.getY(), 2));
        //if the ball lends on the first area on the paddle (left)
        //it will change velocity to hard left
        if (collisionPoint.getX() <= px + area) {
            newVelocity = Velocity.fromAngleAndSpeed(300, speed);
        }
        //if the ball lends on the second area on the paddle (left)
        //it will change velocity to light left
        if (collisionPoint.getX() > px + area && collisionPoint.getX() < px + area * 2) {
            newVelocity = Velocity.fromAngleAndSpeed(330, speed);
        }
        //if the ball lends on the third area on the paddle (center)
        //it will change velocity to straight up
        if (collisionPoint.getX() >= px + area * 2 && collisionPoint.getX() <= px + area * 3) {
            newVelocity = new Velocity(currentVelocity.getX(), -currentVelocity.getY());
        }
        //if the ball lends on the fourth area on the paddle (right)
        //it will change velocity to light right
        if (collisionPoint.getX() > px + area * 3 && collisionPoint.getX() < px + area * 4) {
            newVelocity = Velocity.fromAngleAndSpeed(30, speed);
        }
        //if the ball lends on the fifth area on the paddle (right)
        //it will change velocity to hard right
        if (collisionPoint.getX() >= px + area * 4) {
            newVelocity = Velocity.fromAngleAndSpeed(60, speed);
        }
        return newVelocity;
    }


    /**
     * @param g Add this paddle to the game.
     */
    @Override
    public void addToGame(GameLevel g) {
        g.addCollidable(this);
        g.addSprite(this);
    }
}