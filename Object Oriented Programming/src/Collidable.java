/**
 * The interface Collidable.
 */
public interface Collidable {
    // Return the "collision shape" of the object.

    /**
     * Gets collision rectangle.
     *
     * @return r collision rectangle
     */
    Rectangle getCollisionRectangle();

    // Notify the object that we collided with it at collisionPoint with
    // a given velocity.
    // The return is the new velocity expected after the hit (based on
    // the force the object inflicted on us).

    /**
     * Hit velocity.
     *
     * @param hitter          the hitter
     * @param collisionPoint  c
     * @param currentVelocity c
     * @return r velocity
     */
    Velocity hit(Ball hitter, Point collisionPoint, Velocity currentVelocity);
}