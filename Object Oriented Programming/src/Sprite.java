import biuoop.DrawSurface;

/**
 *
 */
public interface Sprite {
    // draw the sprite to the screen

    /**
     * @param d d
     */
    void drawOn(DrawSurface d);

    // notify the sprite that time has passed

    /**
     *
     */
    void timePassed();

    //adding a new object to the game

    /**
     * @param gameLevel game
     */
    void addToGame(GameLevel gameLevel);
}