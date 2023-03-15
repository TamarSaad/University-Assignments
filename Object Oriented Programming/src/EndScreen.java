import biuoop.DrawSurface;

import java.awt.Color;

/**
 * The class prints the end screen-
 * different messages for winning/losing situations.
 */
public class EndScreen implements Animation {
    private Counter score;
    private boolean win;

    /**
     * Instantiates a new End screen.
     *
     * @param score the score
     * @param win   the win
     */
    public EndScreen(Counter score, boolean win) {
        this.score = score;
        this.win = win;
    }

    @Override
    public void doOneFrame(DrawSurface d) {
        d.setColor(Color.blue.brighter());
        //if the player win
        if (this.win) {
            d.drawText(230, d.getHeight() / 2 - 100, "You Win! ", 70);
        } else {       //if the player lose
            d.drawText(200, d.getHeight() / 2 - 100, "Game Over. ", 70);
        }
        //anyway- the score will be printed
        d.drawText(120, d.getHeight() / 2, "Your score is " + this.score.getValue(), 70);
    }

    @Override
    public boolean shouldStop() {
        return false;
    }
}
