package entities;

import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Paths;


public class ScenarioReader {
    // Class for reading .json file into a Json object in the project
    static BufferedReader bufferedReader;
    String fileName, pathToScenarioFile = "./configuration/scenario_path.txt";

    private ScenarioObject scenarioObject;


    public ScenarioReader() {
        //Wrapper for readScenarioFilename and readScenario
        readScenarioFileName();
        readScenario();
    }

    private void readScenarioFileName() {
        //Method for obtaining filepath from configuration file
        try {
            bufferedReader = new BufferedReader(new FileReader((pathToScenarioFile)));

            this.fileName = bufferedReader.readLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void readScenario() {
        // Method for reading .json file into Gson object in environment
        try {
            Gson gson = new Gson();
            Reader reader = Files.newBufferedReader(Paths.get(this.fileName));
            this.scenarioObject = gson.fromJson(reader, ScenarioObject.class);
            reader.close();


        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public ScenarioObject getScenarioObject() {
        return scenarioObject;
    }
}
