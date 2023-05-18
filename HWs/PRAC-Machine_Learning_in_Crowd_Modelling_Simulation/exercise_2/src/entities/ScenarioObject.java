package entities;

import com.google.gson.JsonObject;

public class ScenarioObject {
    //Scenario class for assigning read Json to the environment as an object. Also get,set and toString are defined
    private final String name;
    private final String description;
    private final String release;
    private final JsonObject processWriters;
    private JsonObject scenario;

    public ScenarioObject(String name, String description, String release, JsonObject processWriters, JsonObject scenario) {
        this.name = name;
        this.description = description;
        this.release = release;
        this.processWriters = processWriters;
        this.scenario = scenario;
    }

    public JsonObject getScenario() {
        return scenario;
    }

    public void setScenario(JsonObject scenario) {
        this.scenario = scenario;
    }

    @Override
    public String toString() {
        //Default toString method is converged into suitable Json format
        return "{" +
                "\"name\" : \"" + name + "\"" +
                ", \"description\" :\"" + description + "\"" +
                ", \"release\" :\"" + release + "\"" +
                ", \"processWriters\":" + processWriters +
                ", \"scenario\":" + scenario +
                '}';
    }
}
