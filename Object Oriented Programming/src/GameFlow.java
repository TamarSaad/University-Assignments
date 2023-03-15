import biuoop.GUI;
import biuoop.KeyboardSensor;

import java.util.List;

/**
 * The type Game flow.
 */
public class GameFlow {
    private AnimationRunner animationRunner;
    private KeyboardSensor keyboardSensor;
    private biuoop.GUI gui;
    private Counter score = new Counter();
    private boolean win;


    /**
     * Instantiates a new Game flow.
     *
     * @param ar  the ar
     * @param ks  the ks
     * @param gui the gui
     */
    public GameFlow(AnimationRunner ar, KeyboardSensor ks, GUI gui) {
        this.animationRunner = ar;
        this.keyboardSensor = ks;
        this.gui = gui;
        this.win = true;
    }


    /**
     * Gets gui.
     *
     * @return the gui
     */
    public biuoop.GUI getGui() {
        return this.gui;
    }


    /**
     * Run levels.
     *
     * @param levels the levels
     */
    public void runLevels(List<LevelInformation> levels) {
        //the loop runs through the levels
        for (LevelInformation levelInfo : levels) {
            //create a new game level and run it
            GameLevel level = new GameLevel(levelInfo,
                    this.animationRunner, this.getGui(), 800, 600, this.score);

            level.initialize();
            level.run();
            //if there are no more balls- the player lose and the game is over
            if (level.numOfBalls() == 0) {
                this.win = false;
                this.animationRunner.run(new KeyPressStoppableAnimation(this.keyboardSensor,
                        "space", new EndScreen(this.score, this.win)));
                break;
            }
        }
        //if the game was over without losing- the player won
        if (this.win) {
            this.animationRunner.run(new KeyPressStoppableAnimation(this.keyboardSensor,
                    "space", new EndScreen(this.score, this.win)));
        }
        //close the screen
        this.getGui().close();
    }
}
