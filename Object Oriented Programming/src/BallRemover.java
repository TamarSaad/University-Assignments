/**
 * The type Ball remover.
 */
public class BallRemover implements HitListener {
    private GameLevel gameLevel;
    private Counter remainingBalls;

    /**
     * Instantiates a new Ball remover.
     *
     * @param g            the g
     * @param removedBalls the removed balls
     */
    public BallRemover(GameLevel g, Counter removedBalls) {
        this.gameLevel = g;
        this.remainingBalls = removedBalls;
    }

    @Override
    public void hitEvent(Block beingHit, Ball hitter) {
        //if the ball touches the bottom border, it will be removed from the game
        hitter.removeFromGame(this.gameLevel);
        this.remainingBalls.decrease(1);
    }
}
