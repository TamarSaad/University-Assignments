/**
 *
 */
public class CollisionInfo {
    private Point collision;
    private Collidable object;

    /**
     * @param p point
     * @param c c
     */
    public CollisionInfo(Point p, Collidable c) {
        this.collision = p;
        this.object = c;
    }

    /**
     * @return collision point
     */
    // the point at which the collision occurs.
    public Point collisionPoint() {
        return this.collision;
    }

    /**
     * @return collision object
     */
    // the collidable object involved in the collision.
    public Collidable collisionObject() {
        return this.object;
    }
}
