package org.vadere.state.attributes.models;

import java.util.Arrays;
import java.util.List;

import org.vadere.annotation.factories.attributes.ModelAttributeClass;
import org.vadere.state.attributes.Attributes;

@ModelAttributeClass
public class AttributesSIRG extends Attributes {

    private int infectionsAtStart = 10;
    private double infectionRate = 0.5;
    private double infectionMaxDistance = 1;
    private double recoveryRate = 0;

    public int getInfectionsAtStart() { return infectionsAtStart; }

    public double getInfectionRate() {
        return infectionRate;
    }

    public double getInfectionMaxDistance() {
        return infectionMaxDistance;
    }

    public double getRecoveryRate() {
        return recoveryRate;
    }

}
