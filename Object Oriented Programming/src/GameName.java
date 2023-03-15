import biuoop.DrawSurface;

import java.awt.Color;

/**
 * The type Game name.
 */
public class GameName implements Sprite {
    private Rectangle rect;
    private String name;

    /**
     * Instantiates a new Game name.
     *
     * @param rec the rec
     * @param s   the s
     */
    public GameName(Rectangle rec, String s) {
        this.rect = rec;
        this.name = "Level Name: " + s;
    }

    @Override
    public void drawOn(DrawSurface d) {
        double xLoc = this.rect.getWidth() * 3.5 / 5;
        double yloc = this.rect.getBottomRight().getY() - 2;
        d.setColor(Color.black);
        d.drawText((int) xLoc, (int) yloc, this.name, 15);
    }

    @Override
    public void timePassed() {
    }

    @Override
    public void addToGame(GameLevel gameLevel) {
        gameLevel.addSprite(this);
    }
}
