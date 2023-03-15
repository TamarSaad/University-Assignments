/**
 * submit: Tamar Saad.
 * 207256991
 */

import biuoop.GUI;

import java.util.ArrayList;
import java.util.List;


public class Ass6Game {

    /**
     * @param args none
     */
    public static void main(String[] args) {
        //a list of the levels
        List<LevelInformation> levels = new ArrayList<>();
        //the switch-case will determine the levels order, by the arguments we received
        for (String s : args) {
            switch (s) {
                case "1" -> levels.add(new DirectHit());
                case "2" -> levels.add(new WideEasy());
                case "3" -> levels.add(new Green3());
                case "4" -> levels.add(new FinalFour());
            }
        }
        //if we didn't receive arguments, or none of them is relevant-
        //we will run the levels by order
        if (levels.size()==0) {
            levels.add(new DirectHit());
            levels.add(new WideEasy());
            levels.add(new Green3());
            levels.add(new FinalFour());
        }
        //open the gui and run the game
        GUI gui = new GUI("game", 800, 600);
        AnimationRunner runner = new AnimationRunner(gui);
        GameFlow game = new GameFlow(runner, gui.getKeyboardSensor(), gui);
        game.runLevels(levels);
    }
}
