import biuoop.DrawSurface;

import java.awt.Color;

/**
 * The type Background.
 */
public class Background implements Sprite {
    private Color color;

    /**
     * Instantiates a new Background.
     *
     * @param c the c
     */
    public Background(Color c) {
        this.color = c;
    }

    @Override
    public void drawOn(DrawSurface d) {
        d.setColor(this.color);
        d.fillRectangle(0, 0, d.getWidth(), d.getHeight());
    }

    @Override
    public void timePassed() {
        return;
    }

    @Override
    public void addToGame(GameLevel gameLevel) {
        gameLevel.addSprite(this);
    }
}
