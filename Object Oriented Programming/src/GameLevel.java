import biuoop.DrawSurface;
import biuoop.GUI;

import java.awt.Color;

/**
 * The type Game level.
 */
public class GameLevel implements Animation {
    private SpriteCollection sprites = new SpriteCollection();
    private GameEnvironment environment = new GameEnvironment();
    private biuoop.GUI gui;
    private int width;
    private int height;
    private Counter numOfBlocks = new Counter();
    private Counter numOfBalls = new Counter();
    private Counter score;
    private AnimationRunner runner;
    private boolean running;
    private LevelInformation levelInformation;


    /**
     * Instantiates a new Game level.
     *
     * @param li  the li
     * @param ar  the ar
     * @param gui the gui
     * @param w   the w
     * @param h   the h
     * @param s   the s
     */
    public GameLevel(LevelInformation li, AnimationRunner ar, biuoop.GUI gui, int w, int h, Counter s) {
        this.levelInformation = li;
        this.runner = ar;
        this.gui = gui;
        this.running = false;
        this.width = w;
        this.height = h;
        this.score = s;
    }

    /**
     * Num of balls int.
     *
     * @return the int
     */
    public int numOfBalls() {
        return this.numOfBalls.getValue();
    }

    /**
     * Add collidable.
     *
     * @param c the c
     */
    public void addCollidable(Collidable c) {
        this.environment.addCollidable(c);
    }

    /**
     * Add sprite.
     *
     * @param s the s
     */
    public void addSprite(Sprite s) {
        this.sprites.addSprite(s);
    }

    /**
     * Gets gui.
     *
     * @return the gui
     */
    public GUI getGui() {
        return this.gui;
    }


    /**
     * Gets width.
     *
     * @return the width
     */
    public int getWidth() {
        return this.width;
    }

    /**
     * Gets height.
     *
     * @return the height
     */
    public int getHeight() {
        return this.height;
    }


    /**
     * Initialize.
     */
    public void initialize() {
        //create the background
        this.levelInformation.getBackground().addToGame(this);
        //add the paddle
        Point point = new Point((this.getWidth() - this.levelInformation.paddleWidth()) / 2, this.getHeight() - 20);
        Rectangle p = new Rectangle(point, this.levelInformation.paddleWidth(), 20);
        Paddle paddle = new Paddle(p, this.getGui(), this.levelInformation.paddleSpeed());
        paddle.addToGame(this);
        setBorders();
        //initialize the balls
        addBalls();
        //add the blocks and the listeners
        addBlocks();
    }

    /**
     * add balls.
     */
    private void addBalls() {
        //initialize the balls
        Ball[] balls = new Ball[this.levelInformation.numberOfBalls()];
        this.numOfBalls.increase(balls.length);
        for (int i = 0; i < balls.length; ++i) {
            balls[i] = new Ball(new Point(this.getWidth() / 2, this.height - 30), 5, Color.blue);
            balls[i].setVelocity(this.levelInformation.initialBallVelocities().get(i));
            balls[i].setGameEnvironment(this.environment);
            balls[i].addToGame(this);
        }
    }


    /**
     * Run.
     * run the game
     */
    public void run() {
        //create a new runner
        this.runner = new AnimationRunner(this.getGui());
        //run the countdown
        this.runner.run(new CountdownAnimation(2.0, 3, this.sprites));
        this.running = true;
        // run the current level
        this.runner.run(this);
    }

    /**
     * add the blocks to the game.
     */
    private void addBlocks() {
        //add the hitlisteners:
        //the one that counts the remaining blocks, and the one that counts the score
        HitListener blockRemover = new BlockRemover(this, this.numOfBlocks);
        HitListener scoreCounter = new ScoreTrackingListener(this.score);
        //add the number of blocks to the counter
        this.numOfBlocks.increase(this.levelInformation.numberOfBlocksToRemove());
        //adding the blocks from the current level
        for (Block b : this.levelInformation.blocks()) {
            b.addToGame(this);
            b.addHitListener(blockRemover);
            b.addHitListener(scoreCounter);
        }
        //add the ball's remover listener and the death region
        HitListener ballRemover = new BallRemover(this, this.numOfBalls);
        Rectangle r = new Rectangle(new Point(0, 590), 800, 10);
        Block deathRegion = new Block(r, Color.black);
        deathRegion.addToGame(this);
        deathRegion.addHitListener(ballRemover);

        //add the score printer to the game
        ScoreIndicator scoreIndicator = new ScoreIndicator(this.score);
        scoreIndicator.addToGame(this);
        //add the game's name to the game
        GameName gn = new GameName(scoreIndicator.getCollisionRectangle(), this.levelInformation.levelName());
        gn.addToGame(this);

    }

    /**
     * set borders.
     */
    private void setBorders() {
        //setting the board's borders
        //not setting the bottom border, because there will be the death region
        Block[] blocks = new Block[3];
        blocks[0] = new Block(new Rectangle(new Point(0, 0), 20, this.getHeight()), Color.BLACK);
        blocks[1] = new Block(new Rectangle((new Point(0, 0)), this.getWidth(), 20), Color.BLACK);
        blocks[2] = new Block(new Rectangle(new Point(this.getWidth() - 20, 0), 20, this.getHeight()), Color.BLACK);
        for (Block b : blocks) {
            b.addToGame(this);
        }
    }


    /**
     * Remove collidable.
     *
     * @param c the c
     */
    public void removeCollidable(Collidable c) {
        this.environment.removeCollidable(c);
    }

    /**
     * Remove sprite.
     *
     * @param s the s
     */
    public void removeSprite(Sprite s) {
        this.sprites.removeSprite(s);
    }

    //run a single frame of the game
    @Override
    public void doOneFrame(DrawSurface d) {
        //draw all the sprites
        this.sprites.drawAllOn(d);
        //change all the sprites according to their methods
        this.sprites.notifyAllTimePassed();
        //if the "p" key is pressed- the game will stop
        if (this.getGui().getKeyboardSensor().isPressed("p")) {
            this.runner.run(new KeyPressStoppableAnimation(this.gui.getKeyboardSensor(), "space", new PauseScreen()));
        }

        //if there are no more blocks/balls, the game is over
        if (this.numOfBlocks.getValue() == 0 || this.numOfBalls.getValue() == 0) {
            //if the player won, the score will increase in 100 points
            if (this.numOfBlocks.getValue() == 0) {
                this.score.increase(100);
            }
            //close and end the game
            this.running = false;
        }
    }

    @Override
    public boolean shouldStop() {
        return !this.running;
    }
}