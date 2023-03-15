import biuoop.DrawSurface;

import java.awt.Color;

/**
 * The class pauses the game when the key "p" is pressed.
 */
public class PauseScreen implements Animation {

    /**
     * @param d drawsurface
     */
    public void doOneFrame(DrawSurface d) {
        d.setColor(Color.pink);
        d.drawText(20, d.getHeight() / 2, "paused -- press space to continue", 50);
    }
    /**
     * @return false
     */
    public boolean shouldStop() {
        return false;
    }
}
