import biuoop.DrawSurface;

import java.awt.Color;
import java.util.ArrayList;
import java.util.List;

/**
 * The type Block.
 */
public class Block implements Collidable, Sprite, HitNotifier {

    private Rectangle rect;
    private java.awt.Color color;
    private List<HitListener> hitListeners = new ArrayList<HitListener>();

    //constructor

    /**
     * Instantiates a new Block.
     *
     * @param rectangle the rectangle
     * @param color     the color
     */
    public Block(Rectangle rectangle, java.awt.Color color) {
        this.color = color;
        this.rect = rectangle;
    }

    /**
     * Instantiates a new Block.
     *
     * @param upperLeft the upper left
     * @param width     the width
     * @param height    the height
     * @param color     the color
     */
    public Block(Point upperLeft, double width, double height, java.awt.Color color) {
        this.rect = new Rectangle(upperLeft, width, height);
        this.color = color;
    }

    /**
     * @return rectangle
     */
    @Override
    public Rectangle getCollisionRectangle() {
        return this.rect;
    }

    /**
     * @param collisionPoint  c
     * @param currentVelocity c
     * @return velocity
     * in case a ball hits the block, it will change its velocity according to this method
     */
    @Override
    public Velocity hit(Ball hitter, Point collisionPoint, Velocity currentVelocity) {
        double epsilon = 0.1;
        //the top left point
        double lx = this.rect.getUpperLeft().getX();
        double ly = this.rect.getUpperLeft().getY();
        //the bottom right point
        double rx = this.rect.getBottomRight().getX();
        double ry = this.rect.getBottomRight().getY();
        //the velocity values
        double newx = currentVelocity.getX();
        double newy = currentVelocity.getY();
        //if the ball collide with vertical side
        if (Math.abs(collisionPoint.getX() - lx) <= epsilon || Math.abs(collisionPoint.getX() - rx) <= epsilon) {
            newx = (-newx);
        }
        //if the ball collide with horizontal side
        if (Math.abs(collisionPoint.getY() - ly) <= epsilon || Math.abs(collisionPoint.getY() - ry) <= epsilon) {
            newy = (-newy);
        }
        notifyHit(hitter);
        //set a new velocity for the ball

        return new Velocity(newx, newy);
    }

    /**
     * @param surface the method get a surface and draws the block on it
     */
    @Override
    public void drawOn(DrawSurface surface) {
        //draw a black frame
        surface.setColor(Color.black);
        surface.drawRectangle((int) this.rect.getUpperLeft().getX(), (int) this.rect.getUpperLeft().getY(),
                (int) this.rect.getWidth(), (int) this.rect.getHeight());
        //fill the rectangle with its color
        surface.setColor(this.color);
        surface.fillRectangle((int) this.rect.getUpperLeft().getX(), (int) this.rect.getUpperLeft().getY(),
                (int) this.rect.getWidth(), (int) this.rect.getHeight());
    }

    /**
     * right now, the method does nothing.
     */
    @Override
    public void timePassed() {
    }

    /**
     * @param gameLevel adds the block to the game, as both sprite and collidable
     */
    @Override
    public void addToGame(GameLevel gameLevel) {
        gameLevel.addSprite(this);
        gameLevel.addCollidable(this);
    }

    @Override
    public void addHitListener(HitListener hl) {
        this.hitListeners.add(hl);
    }

    @Override
    public void removeHitListener(HitListener hl) {
        this.hitListeners.remove(hl);
    }

    /**
     * Notify hit.
     *
     * @param hitter ball
     */
    private void notifyHit(Ball hitter) {
        // Make a copy of the hitListeners before iterating over them.
        List<HitListener> listeners = new ArrayList<HitListener>(this.hitListeners);
        // Notify all listeners about a hit event:
        for (HitListener hl : listeners) {
            hl.hitEvent(this, hitter);
        }
    }

    /**
     * Remove from game.
     *
     * @param gameLevel the game level
     */
    public void removeFromGame(GameLevel gameLevel) {
        gameLevel.removeCollidable(this);
        gameLevel.removeSprite(this);
    }

}