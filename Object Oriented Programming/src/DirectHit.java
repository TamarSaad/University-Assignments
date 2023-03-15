import java.awt.Color;
import java.util.ArrayList;
import java.util.List;

/**
 * The type Direct hit.
 */
public class DirectHit implements LevelInformation {

    @Override
    public int numberOfBalls() {
        return 1;
    }

    @Override
    public List<Velocity> initialBallVelocities() {
        List<Velocity> velocities = new ArrayList<>();
        velocities.add(Velocity.fromAngleAndSpeed(0.0, 5.0));
        return velocities;
    }

    @Override
    public int paddleSpeed() {
        return 7;
    }

    @Override
    public int paddleWidth() {
        return 85;
    }

    @Override
    public String levelName() {
        return "Direct Hit";
    }

    @Override
    public Sprite getBackground() {
        return new Background(Color.cyan.brighter());
    }

    @Override
    public List<Block> blocks() {
        List<Block> blocks = new ArrayList<>();
        Block b = new Block(new Rectangle(new Point(385, 100), 30, 30), Color.red);
        blocks.add(b);
        return blocks;
    }

    @Override
    public int numberOfBlocksToRemove() {
        return 1;
    }
}
