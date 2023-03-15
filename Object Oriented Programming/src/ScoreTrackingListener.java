/**
 * The type Score tracking listener.
 */
public class ScoreTrackingListener implements HitListener {
    private Counter currentScore;

    /**
     * Instantiates a new Score tracking listener.
     *
     * @param scoreCounter the score counter
     */
    public ScoreTrackingListener(Counter scoreCounter) {
        this.currentScore = scoreCounter;
    }

    //when a hit occurs, 5 points will be added to the score
    @Override
    public void hitEvent(Block beingHit, Ball hitter) {
        this.currentScore.increase(5);
    }
}