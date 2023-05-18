package entities;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import static java.lang.System.exit;

public class ScenarioController {

    public void addPedestrian(ScenarioObject scenarioObject) {
        /* adding the wanted pedestrian to the fetched scenario */
        JsonObject scenarioContent = scenarioObject.getScenario();
        // Checked whether the scenario fetched is corrupted or not
        if (!scenarioContent.has("topography")) {
            System.out.println("Scenario file is bad formatted. No topography field could be found.");
            exit(0);
        }
        //For modifying dynamic elements Json Objects are created and assigned to these environments JsonObjects
        JsonObject topography = (JsonObject) scenarioContent.get("topography");
        JsonArray dynamicElements = (JsonArray) topography.get("dynamicElements");
        JsonObject dynamicElements_inside = new JsonObject();

        //From the sample json that generated from vadere gui, suitable format and values are generated
        JsonObject attributes = new JsonObject();
        attributes.addProperty("id", 4);
        attributes.addProperty("radius", 0.2);
        attributes.addProperty("densityDependentSpeed", false);
        attributes.addProperty("speedDistributionMean", 1.34);
        attributes.addProperty("speedDistributionStandardDeviation", 0.26);
        attributes.addProperty("minimumSpeed", 0.5);
        attributes.addProperty("maximumSpeed", 2.2);
        attributes.addProperty("acceleration", 2.0);
        attributes.addProperty("footstepHistorySize", (double) 4);
        attributes.addProperty("searchRadius", 1.0);
        attributes.addProperty("walkingDirectionCalculation", "BY_TARGET_CENTER");
        attributes.addProperty("walkingDirectionSameIfAngleLessOrEqual", 45.0);


        JsonObject position = new JsonObject();
        position.addProperty("x", (double) 13);
        position.addProperty("y", (double) 3);

        JsonObject velocity = new JsonObject();
        velocity.addProperty("x", (double) 0);
        velocity.addProperty("y", (double) 0);


        JsonObject threatMemory = new JsonObject();
        JsonArray allThreats = new JsonArray();
        threatMemory.add("allThreats", allThreats);
        threatMemory.addProperty("latestThreatUnhandled", false);

        JsonObject knowledgeBase = new JsonObject();
        JsonArray knowledge = new JsonArray();
        knowledgeBase.add("knowledge", knowledge);
        knowledgeBase.addProperty("informationState", "NO_INFORMATION");
        JsonObject psychologyStatus = new JsonObject();
        psychologyStatus.addProperty("mostImportantStimulus", (String) null);
        psychologyStatus.add("threatMemory", threatMemory);
        psychologyStatus.addProperty("selfCategory", "TARGET_ORIENTED");
        psychologyStatus.addProperty("groupMembership", "OUT_GROUP");
        psychologyStatus.add("knowledgeBase", knowledgeBase);
        JsonArray perceivedStimuli = new JsonArray();
        psychologyStatus.add("perceivedStimuli", perceivedStimuli);
        JsonArray nextPerceivedStimuli = new JsonArray();
        psychologyStatus.add("nextPerceivedStimuli", nextPerceivedStimuli);

        JsonObject trajectory = new JsonObject();
        JsonArray footSteps = new JsonArray();
        trajectory.add("footSteps", footSteps);

        dynamicElements_inside.add("attributes", attributes);
        dynamicElements_inside.addProperty("source", (String) null);
        JsonArray targetIds = new JsonArray();
        targetIds.add(40);
        dynamicElements_inside.add("targetIds", targetIds);  // add target id otherwise wont move
        dynamicElements_inside.addProperty("nextTargetListIndex", 0);
        dynamicElements_inside.addProperty("isCurrentTargetAnAgent", false);
        dynamicElements_inside.add("position", position);
        dynamicElements_inside.add("velocity", velocity);
        dynamicElements_inside.addProperty("freeFlowSpeed", 1.4517543027091087);
        JsonArray followers = new JsonArray();
        dynamicElements_inside.add("followers", followers);
        dynamicElements_inside.addProperty("idAsTarget", -1);
        dynamicElements_inside.addProperty("isChild", false);
        dynamicElements_inside.addProperty("isLikelyInjured", false);
        dynamicElements_inside.add("psychologyStatus", psychologyStatus);
        dynamicElements_inside.addProperty("healthStatus", (String) null);
        dynamicElements_inside.addProperty("infectionStatus", (String) null);
        JsonArray groupIds = new JsonArray();
        dynamicElements_inside.add("groupIds", groupIds);
        JsonArray groupSizes = new JsonArray();
        dynamicElements_inside.add("groupSizes", groupSizes);
        JsonArray agentsInGroup = new JsonArray();
        dynamicElements_inside.add("agentsInGroup", agentsInGroup);
        dynamicElements_inside.add("trajectory", trajectory);
        JsonObject modelPedestrianMap = new JsonObject();
        dynamicElements_inside.add("modelPedestrianMap", modelPedestrianMap);
        dynamicElements_inside.addProperty("type", "PEDESTRIAN");


        System.out.println(dynamicElements_inside);

        dynamicElements.add(dynamicElements_inside);
        //Created dynamic elements attribute assigned with the wanted values
        topography.add("dynamicElements", dynamicElements);
        scenarioContent.add("topography", topography);
        scenarioObject.setScenario(scenarioContent);


    }
}
