import biuoop.DrawSurface;
import biuoop.Sleeper;

import java.awt.Color;

/**
 * The type Countdown animation.
 */
// The CountdownAnimation will display the given gameScreen,
// for numOfSeconds seconds, and on top of them it will show
// a countdown from countFrom back to 1, where each number will
// appear on the screen for (numOfSeconds / countFrom) seconds, before
// it is replaced with the next one.
public class CountdownAnimation implements Animation {
    private double numOfSeconds;
    private int countFrom;
    private SpriteCollection gameScreen;
    private Sleeper sleeper = new Sleeper();
    private int framesPassed;

    /**
     * Instantiates a new Countdown animation.
     *
     * @param numOfSeconds the num of seconds
     * @param countFrom    the count from
     * @param gameScreen   the game screen
     */
    public CountdownAnimation(double numOfSeconds,
                              int countFrom,
                              SpriteCollection gameScreen) {
        this.numOfSeconds = numOfSeconds;
        this.countFrom = countFrom;
        this.gameScreen = gameScreen;
        this.framesPassed = 0;
    }

@Override
    public void doOneFrame(DrawSurface d) {
        if (this.countFrom == 0) {
            this.gameScreen.drawAllOn(d);
            d.setColor(Color.cyan.darker());
            d.drawText(d.getWidth() / 5, d.getHeight() * 2 / 3, "GO!", 300);
        } else {
            this.gameScreen.drawAllOn(d);
            d.setColor(Color.cyan.darker());
            d.drawText(d.getWidth() * 2 / 5, d.getHeight() * 2 / 3, Integer.toString(this.countFrom), 300);
        }
        frameChanging();
    }

    /**
     * change the frame.
     */
    private void frameChanging() {
        if (this.framesPassed >= this.numOfSeconds * 60 / (this.countFrom + 2)) {
            this.countFrom--;
            this.framesPassed = 0;
        } else {
            this.framesPassed++;
        }
    }

@Override
    public boolean shouldStop() {
        if (this.countFrom == -1) {
            return true;
        }
        return false;
    }
}
