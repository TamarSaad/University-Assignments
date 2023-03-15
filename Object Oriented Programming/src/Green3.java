import java.awt.Color;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * The type Green 3.
 */
public class Green3 implements LevelInformation {
    @Override
    public int numberOfBalls() {
        return 2;
    }

    @Override
    public List<Velocity> initialBallVelocities() {
        List<Velocity> velocities = new ArrayList<>();
        for (int i = 0; i < this.numberOfBalls(); ++i) {
            velocities.add(Velocity.fromAngleAndSpeed(80 * i - 40, 4));
        }
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
        return "Green 3";
    }

    @Override
    public Sprite getBackground() {
        return new Background(new Color(51, 204, 255));
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
    public List<Block> blocks() {
        List<Block> blocks = new ArrayList<>(this.numberOfBlocksToRemove());
        double blockWidth = 50;
        int blocksPerLine = 10;
        int numOfLines = 5;
        for (int j = 0; j < numOfLines; ++j) {
            Color color = getRandomColor();
            for (int i = 0; i < blocksPerLine; ++i) {
                Block b = new Block(new Rectangle(new Point(
                        730 - blockWidth * i, 150 + j * 30), blockWidth, 30), color);
                blocks.add(b);
            }
            blocksPerLine--;
        }
        return blocks;
    }

    @Override
    public int numberOfBlocksToRemove() {
        return 40;
    }
}
