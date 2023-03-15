import biuoop.DrawSurface;

import java.awt.Color;

/**
 * The type Score indicator.
 */
public class ScoreIndicator implements Sprite, Collidable {
    private Block block;
    private Counter count;

    /**
     * Instantiates a new Score indicator.
     *
     * @param c the c
     */
    public ScoreIndicator(Counter c) {
        //the counter is a pointer to the ScoreTrackingListener counter
        this.count = c;
        this.block = new Block(new Rectangle(new Point(0, 20), 800, 17), Color.pink);
    }

    @Override
    public void drawOn(DrawSurface d) {
        Rectangle rect = this.block.getCollisionRectangle();
        //draw the rectangle
        d.setColor(Color.gray);
        d.fillRectangle((int) rect.getUpperLeft().getX(), (int) rect.getUpperLeft().getY(),
                (int) rect.getWidth(), (int) rect.getHeight());
        String print = "Score: " + this.count.getValue();
        double rectMidlleX = (rect.getUpperLeft().getX() + rect.getWidth()) / 2;
        d.setColor(Color.black);
        //the text will be displayed in the middle of the block, and it will be
        //the score the player achieved
        d.drawText((int) rectMidlleX, (int) rect.getBottomRight().getY() - 2, print, 15);
    }

    //this method doesn't do anything, but since it's belong to the interface it must be implemented
    @Override
    public void timePassed() {
    }

    @Override
    public void addToGame(GameLevel gameLevel) {
        gameLevel.addSprite(this);
        gameLevel.addCollidable(this);
    }

    @Override
    public Rectangle getCollisionRectangle() {
        return this.block.getCollisionRectangle();
    }

    @Override
    public Velocity hit(Ball hitter, Point collisionPoint, Velocity currentVelocity) {
        return this.block.hit(hitter, collisionPoint, currentVelocity);
    }
}
