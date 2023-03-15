import biuoop.DrawSurface;
import biuoop.KeyboardSensor;

/**
 * The class is a decorator that in charge of the keyboard sensor-
 * if a key is pressed it will acknowledge the right class.
 */
public class KeyPressStoppableAnimation implements Animation {
    private KeyboardSensor keyboard;
    private String key;
    private Animation animation;
    private boolean stop;
    private boolean isAlreadyPressed;

    /**
     * Instantiates a new Key press stoppable animation.
     *
     * @param sensor    the sensor
     * @param key       the key
     * @param animation the animation
     */
    public KeyPressStoppableAnimation(KeyboardSensor sensor, String key, Animation animation) {
        this.keyboard = sensor;
        this.key = key;
        this.animation = animation;
        this.stop = false;
        this.isAlreadyPressed = true;
    }

    @Override
    public void doOneFrame(DrawSurface d) {
        //if the class's key is pressed, but wasn't pressed already- the class will react
        if (this.keyboard.isPressed(this.key) && !this.isAlreadyPressed) {
            this.stop = true;
        } else {
            this.isAlreadyPressed = false;
            this.animation.doOneFrame(d);
        }
    }

    @Override
    public boolean shouldStop() {
        return this.stop;
    }
}
