package org.vadere.simulator.models.groups.sir;


import org.vadere.annotation.factories.models.ModelClass;
import org.vadere.simulator.models.Model;
import org.vadere.simulator.models.groups.AbstractGroupModel;
import org.vadere.simulator.models.groups.Group;
import org.vadere.simulator.models.groups.GroupSizeDeterminator;
import org.vadere.simulator.models.groups.cgm.CentroidGroup;
import org.vadere.simulator.models.potential.fields.IPotentialFieldTarget;
import org.vadere.simulator.projects.Domain;
import org.vadere.state.attributes.Attributes;
import org.vadere.simulator.models.groups.sir.SIRGroup;
import org.vadere.state.attributes.models.AttributesSIRG;
import org.vadere.state.attributes.scenario.AttributesAgent;
import org.vadere.state.scenario.DynamicElement;
import org.vadere.state.scenario.DynamicElementContainer;
import org.vadere.state.scenario.Pedestrian;
import org.vadere.state.scenario.Topography;
import org.vadere.util.geometry.LinkedCellsGrid;
import org.vadere.util.geometry.PointPositioned;
import org.vadere.util.geometry.shapes.VPoint;

import java.util.*;

/**
 * Implementation of groups for a susceptible / infected / removed (SIR) model.
 */
@ModelClass
public class SIRGroupModel extends AbstractGroupModel<SIRGroup> {

    private class NotComparableObject implements PointPositioned {
        public int value;
        public VPoint coord;

        public NotComparableObject(int value, VPoint coord) {
            this.value = value;
            this.coord = coord;
        }
        @Override
        public VPoint getPosition() {
            return coord;
        }
    }

    private Random random;
    private LinkedHashMap<Integer, SIRGroup> groupsById;
    private Map<Integer, LinkedList<SIRGroup>> sourceNextGroups;
    private AttributesSIRG attributesSIRG;
    private Topography topography;
    private IPotentialFieldTarget potentialFieldTarget;
    private int totalInfected = 0;
    private int initiallyInfected = 0;
    private int totalSusceptible = 0;
    private int totalRecovered = 0;
    private double lastSimTimeInSec = 0;
    private int nUpdate = 0;

    private final double DELTA_TIME = 1;

    public SIRGroupModel() {
        this.groupsById = new LinkedHashMap<>();
        this.sourceNextGroups = new HashMap<>();
    }

    @Override
    public void initialize(List<Attributes> attributesList, Domain domain,
                           AttributesAgent attributesPedestrian, Random random) {
        this.attributesSIRG = Model.findAttributes(attributesList, AttributesSIRG.class);
        this.topography = domain.getTopography();
        this.random = random;
        this.totalInfected = 0;
        this.initiallyInfected = 0;
        this.totalSusceptible = 0;
        this.totalRecovered = 0;
        this.lastSimTimeInSec = 0;
        this.nUpdate = 0;
    }

    @Override
    public void setPotentialFieldTarget(IPotentialFieldTarget potentialFieldTarget) {
        this.potentialFieldTarget = potentialFieldTarget;
        // update all existing groups
        for (SIRGroup group : groupsById.values()) {
            group.setPotentialFieldTarget(potentialFieldTarget);
        }
    }

    @Override
    public IPotentialFieldTarget getPotentialFieldTarget() {
        return potentialFieldTarget;
    }

    private int getFreeGroupId() {
        if(this.random.nextDouble() < this.attributesSIRG.getInfectionRate()
                || this.initiallyInfected < this.attributesSIRG.getInfectionsAtStart()) {
            if(!getGroupsById().containsKey(SIRType.ID_INFECTED.ordinal()))
            {
                SIRGroup g = getNewGroup(SIRType.ID_INFECTED.ordinal(), Integer.MAX_VALUE/2);
                getGroupsById().put(SIRType.ID_INFECTED.ordinal(), g);
            }
            this.totalInfected += 1;
            this.initiallyInfected += 1;
            return SIRType.ID_INFECTED.ordinal();
        }
        else{
            if(!getGroupsById().containsKey(SIRType.ID_SUSCEPTIBLE.ordinal()))
            {
                SIRGroup g = getNewGroup(SIRType.ID_SUSCEPTIBLE.ordinal(), Integer.MAX_VALUE/2);
                getGroupsById().put(SIRType.ID_SUSCEPTIBLE.ordinal(), g);
            }
            this.totalSusceptible += 1;
            return SIRType.ID_SUSCEPTIBLE.ordinal();
        }
    }


    @Override
    public void registerGroupSizeDeterminator(int sourceId, GroupSizeDeterminator gsD) {
        sourceNextGroups.put(sourceId, new LinkedList<>());
    }

    @Override
    public int nextGroupForSource(int sourceId) {
        return Integer.MAX_VALUE/2;
    }

    @Override
    public SIRGroup getGroup(final Pedestrian pedestrian) {
        SIRGroup group = groupsById.get(pedestrian.getGroupIds().getFirst());
        assert group != null : "No group found for pedestrian";
        return group;
    }

    @Override
    protected void registerMember(final Pedestrian ped, final SIRGroup group) {
        groupsById.putIfAbsent(ped.getGroupIds().getFirst(), group);
    }

    @Override
    public Map<Integer, SIRGroup> getGroupsById() {
        return groupsById;
    }

    @Override
    protected SIRGroup getNewGroup(final int size) {
        return getNewGroup(getFreeGroupId(), size);
    }

    @Override
    protected SIRGroup getNewGroup(final int id, final int size) {
        if(groupsById.containsKey(id))
        {
            return groupsById.get(id);
        }
        else
        {
            return new SIRGroup(id, this);
        }
    }

    private void initializeGroupsOfInitialPedestrians() {
        // get all pedestrians already in topography
        DynamicElementContainer<Pedestrian> c = topography.getPedestrianDynamicElements();

        if (c.getElements().size() > 0) {
            // Here you can fill in code to assign pedestrians in the scenario at the beginning (i.e., not created by a source)
            //  to INFECTED or SUSCEPTIBLE groups. This is not required in the exercise though.
        }
    }

    protected void assignToGroup(Pedestrian ped, int groupId) {
        SIRGroup currentGroup = getNewGroup(groupId, Integer.MAX_VALUE/2);
        currentGroup.addMember(ped);
        ped.getGroupIds().clear();
        ped.getGroupSizes().clear();
        ped.addGroupId(currentGroup.getID(), currentGroup.getSize());
        registerMember(ped, currentGroup);
    }

    protected void assignToGroup(Pedestrian ped) {
        int groupId = getFreeGroupId();
        assignToGroup(ped, groupId);
    }


    /* DynamicElement Listeners */

    @Override
    public void elementAdded(Pedestrian pedestrian) {
        assignToGroup(pedestrian);
    }

    @Override
    public void elementRemoved(Pedestrian pedestrian) {
        Group group = groupsById.get(pedestrian.getGroupIds().getFirst());
        if (group.removeMember(pedestrian)) { // if true pedestrian was last member.
            groupsById.remove(group.getID());
        }
    }

    /* Model Interface */

    @Override
    public void preLoop(final double simTimeInSec) {
        initializeGroupsOfInitialPedestrians();
        topography.addElementAddedListener(Pedestrian.class, this);
        topography.addElementRemovedListener(Pedestrian.class, this);
    }

    @Override
    public void postLoop(final double simTimeInSec) {
    }

    @Override
    public void update(final double simTimeInSec) {
        // check the positions of all pedestrians and switch groups to INFECTED (or REMOVED).
        DynamicElementContainer<Pedestrian> c = topography.getPedestrianDynamicElements();

        if (c.getElements().size() > 0) {

            this.nUpdate++;

            double left = topography.getBounds().getX();
            double top = topography.getBounds().getY();
            double width = topography.getBounds().getWidth();
            double height = topography.getBounds().getHeight();
            double sideLength = topography.getAttributes().getBoundingBoxWidth();
            LinkedCellsGrid<NotComparableObject> linkedCellsObject = new LinkedCellsGrid<NotComparableObject>(left, top,
                    width, height, sideLength);

            int p_id = 0;
            for(Pedestrian p : c.getElements()) {
                p_id++;
                SIRGroup g = getGroup(p);
                if(g.getID() != SIRType.ID_INFECTED.ordinal())
                    continue;
                linkedCellsObject.addObject(new NotComparableObject(p_id, p.getPosition()));
            }

            for(Pedestrian p : c.getElements()) {
                SIRGroup g = getGroup(p);
                if(g.getID() == SIRType.ID_SUSCEPTIBLE.ordinal()) {
                    List<NotComparableObject> infectedClosePedestrians = linkedCellsObject.getObjects(
                            p.getPosition(), attributesSIRG.getInfectionMaxDistance());
                    int nInfectedClosePedestrians = infectedClosePedestrians.size();
                    int totalInfectedPedestrians = p.getTotalInfectedPedestrians();
                    totalInfectedPedestrians += nInfectedClosePedestrians;
                    p.setTotalInfectedPedestrians(totalInfectedPedestrians);
                }
            }

            if(simTimeInSec >= this.lastSimTimeInSec + DELTA_TIME) {
                for(Pedestrian p : c.getElements()) {
                    SIRGroup g = getGroup(p);
                    if(g.getID() != SIRType.ID_INFECTED.ordinal())
                        continue;
                    if(this.random.nextDouble() < attributesSIRG.getRecoveryRate()) {
                        this.totalInfected -= 1;
                        this.totalRecovered += 1;
                        elementRemoved(p);
                        assignToGroup(p, SIRType.ID_RECOVERED.ordinal());
                    }
                }
                for(Pedestrian p : c.getElements()) {
                    SIRGroup g = getGroup(p);
                    if(g.getID() == SIRType.ID_SUSCEPTIBLE.ordinal()) {
                        int totalInfectedPedestrians = p.getTotalInfectedPedestrians();
                        int avgInfectedClosePedestrians = totalInfectedPedestrians / this.nUpdate;
                        for( int i = 0 ; i < avgInfectedClosePedestrians ; i++ )
                            if(this.random.nextDouble() < attributesSIRG.getInfectionRate()) {
                                this.totalSusceptible -= 1;
                                this.totalInfected += 1;
                                elementRemoved(p);
                                assignToGroup(p, SIRType.ID_INFECTED.ordinal());
                                break;
                            }
                        p.setTotalInfectedPedestrians(0);
                    }
                }
                this.nUpdate = 0;
                this.lastSimTimeInSec = simTimeInSec;
            }
        }

        // System.out.println("Count(" + simTimeInSec + "): " + this.totalSusceptible + " " + this.totalInfected + " " + this.totalRecovered);
    }
}