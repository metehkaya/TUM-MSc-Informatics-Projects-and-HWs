# Exercise 2 - Vadere

### Setup

1. Install vadere

2. Add or modify the source codes (.java files) given in src folder
	- modified:   VadereGui/src/org/vadere/gui/components/model/DefaultSimulationConfig.java
	- modified:   VadereGui/src/org/vadere/gui/components/model/SimulationModel.java
	- modified:   VadereGui/src/org/vadere/gui/postvisualization/view/PostvisualizationRenderer.java
	- modified:   VadereSimulator/src/org/vadere/simulator/models/groups/AbstractGroupModel.java
	- new file:   VadereSimulator/src/org/vadere/simulator/models/groups/sir/SIRGroup.java
	- new file:   VadereSimulator/src/org/vadere/simulator/models/groups/sir/SIRGroupModel.java
	- new file:   VadereSimulator/src/org/vadere/simulator/models/groups/sir/SIRType.java
	- modified:   VadereSimulator/src/org/vadere/simulator/projects/dataprocessing/processor/FootStepGroupIDProcessor.java
	- modified:   VadereSimulator/src/org/vadere/simulator/projects/dataprocessing/processor/FootStepProcessor.java
	- new file:   VadereState/src/org/vadere/state/attributes/models/AttributesSIRG.java
	- modified:   VadereState/src/org/vadere/state/scenario/Pedestrian.java

3. Add or modify the scenario files (.scenario files) given in Scenarios folder
	- modified:   Scenarios/ModelTests/TestOSM/scenarios/basic_2_density_discrete_ca.scenario
	- new file:   Scenarios/ModelTests/TestOSM/scenarios/task4_sc1.scenario
	- new file:   Scenarios/ModelTests/TestOSM/scenarios/task4_sc2.scenario
	- new file:   Scenarios/ModelTests/TestOSM/scenarios/task5_sc1.scenario
	- new file:   Scenarios/ModelTests/TestOSM/scenarios/task5_sc2.scenario

4. Optionally, you can delete VadereManager/src/org/vadere/manager/client/TestClient.java which is an independent src file for testing purposes if it gives compile error(s).

5. Rebuild the projects VadereState, VadereSimulator and VadereGui in order and run vadere.
