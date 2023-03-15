import java.awt.Color;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * The type Final four.
 */
public class FinalFour implements LevelInformation {
    @Override
    public int numberOfBalls() {
        return 3;
    }

    @Override
    public List<Velocity> initialBallVelocities() {
        List<Velocity> velocities = new ArrayList<>();
        for (int i = 0; i < this.numberOfBalls(); ++i) {
            velocities.add(Velocity.fromAngleAndSpeed(40 * i - 40, 4));
        }
        return velocities;
    }

    @Override
    public int paddleSpeed() {
        return 7;
    }

    @Override
    public int paddleWidth() {
        return 75;
    }

    @Override
    public String levelName() {
        return "Final Four";
    }

    @Override
    public Sprite getBackground() {
        return new Background(Color.yellow.brighter());
    }

    @Override
    public List<Block> blocks() {
        List<Block> blocks = new ArrayList<>(this.numberOfBlocksToRemove());
        double blockWidth = 50.6;
        int blocksPerLine = 15;
        int numOfLines = 7;
        for (int j = 0; j < numOfLines; ++j) {
            Color color = getRandomColor();
            for (int i = 0; i < blocksPerLine; ++i) {
                Block b = new Block(new Rectangle(new Point(
                        730 - blockWidth * i, 130 + j * 30), blockWidth, 30), color);
                blocks.add(b);
            }
        }
        return blocks;
    }

    /**
     * @return random color
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
        return 105;
    }
}
