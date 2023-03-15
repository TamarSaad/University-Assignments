import biuoop.DrawSurface;

import java.util.ArrayList;
import java.util.List;

/**
 * The type Sprite collection.
 */
public class SpriteCollection {
    private java.util.List<Sprite> sprites = new java.util.ArrayList<Sprite>();

    /**
     * Add sprite.
     *
     * @param s the s
     */
    public void addSprite(Sprite s) {
        sprites.add(s);
    }

    // call timePassed() on all sprites.

    /**
     * Notify all time passed.
     */
    public void notifyAllTimePassed() {
        List<Sprite> sp = new ArrayList<>(this.sprites);
        for (Sprite s : sp) {
            s.timePassed();
        }
    }

    // call drawOn(d) on all sprites.

    /**
     * Draw all on.
     *
     * @param d the d
     */
    public void drawAllOn(DrawSurface d) {
        List<Sprite> sp = new ArrayList<>(this.sprites);
        for (Sprite s : sp) {
            s.drawOn(d);
        }
    }

    /**
     * Remove sprite.
     *
     * @param s the s
     */
    public void removeSprite(Sprite s) {
        this.sprites.remove(s);
    }
}