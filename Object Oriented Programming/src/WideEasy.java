import java.awt.Color;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * The type Wide easy.
 */
public class WideEasy implements LevelInformation {
    @Override
    public int numberOfBalls() {
        return 10;
    }

    @Override
    public List<Velocity> initialBallVelocities() {
        List<Velocity> velocities = new ArrayList<>(this.numberOfBalls());
        for (int i = 0; i < this.numberOfBalls(); ++i) {
            velocities.add(Velocity.fromAngleAndSpeed(10 * i - 45, 4));
        }
        return velocities;
    }

    @Override
    public int paddleSpeed() {
        return 7;
    }

    @Override
    public int paddleWidth() {
        return 700;
    }

    @Override
    public String levelName() {
        return "Wide Easy";
    }

    @Override
    public Sprite getBackground() {
        return new Background(Color.pink);
    }

    @Override
    public List<Block> blocks() {
        List<Block> blocks = new ArrayList<>(this.numberOfBlocksToRemove());
        double blockWidth = 50.667;
        for (int i = 0; i < this.numberOfBlocksToRemove(); ++i) {
            Block b = new Block(new Rectangle(new Point(20 + blockWidth * i, 150), blockWidth, 30), getRandomColor());
            blocks.add(b);
        }
        return blocks;
    }

    /**
     * Gets random color.
     *
     * @return the random color
     */
    private Color getRandomColor() {
        //getting a random color
        Random rand = new Random();
        float r = rand.nextFloat();
        float g = rand.nextFloat();
        float b = rand.nextFloat();
        return new Color(r, g, b);
    }

    @Override
    public int numberOfBlocksToRemove() {
        return 15;
    }
}