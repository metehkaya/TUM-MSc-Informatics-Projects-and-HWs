import entities.Pedestrian;
import entities.ScenarioController;
import entities.ScenarioObject;
import entities.ScenarioReader;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class Main {
    public static void main(String[] args) {
        //Objects are created for Reading from the file
        ScenarioReader scenarioReader = new ScenarioReader();
        ScenarioObject scenarioObject = scenarioReader.getScenarioObject();
        // Controller Object is created and merged with new added pedestrian for modification
        ScenarioController scenarioController = new ScenarioController();
        scenarioController.addPedestrian(scenarioObject);



        String path = "./scenarios/modified.scenario";

        try (PrintWriter out = new PrintWriter(new FileWriter(path))) {
            out.write(String.valueOf(scenarioObject));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }


    }
}
