import java.util.ArrayList;
import java.util.List;

/**
 * The type Game environment.
 */
public class GameEnvironment {
    private java.util.List<Collidable> collidables = new java.util.ArrayList<Collidable>();


    // add the given collidable to the environment.

    /**
     * Add collidable.
     *
     * @param c the c
     */
    public void addCollidable(Collidable c) {
        this.collidables.add(c);
    }


    /**
     * Gets closest collision.
     *
     * @param trajectory the trajectory
     * @return the closest collision
     */
    public CollisionInfo getClosestCollision(Line trajectory) {
        //if there are no collidables
        if (collidables.size() == 0) {
            return null;
        }
        //the flag will helps us know if we had any collision
        boolean flag = true;
        Collidable minC = null;
        Point minP = null;
        double minD = 0;
        //a loop that goes over all the collidables and check for collision
        List<Collidable> co = new ArrayList<>(this.collidables);
        for (Collidable c : co) {
            //the method returns the closest collision point with a specific collidable, if exist
            Point p = trajectory.closestIntersectionToStartOfLine(c.getCollisionRectangle());
            //if the point exist
            if (p != null) {
                double d = p.distance(trajectory.start());
                //the first point will go inside the if,
                // and then any other point that is closer to the start of the line
                if (flag || minD > d) {
                    minP = p;
                    minD = d;
                    minC = c;
                    flag = false;
                }
            }
        }
        //if there are no collisions at all
        if (flag) {
            return null;
        }
        //else- return the closest collision point
        return new CollisionInfo(minP, minC);
    }

    /**
     * Remove collidable.
     *
     * @param c the c
     */
    public void removeCollidable(Collidable c) {
        this.collidables.remove(c);
    }

}