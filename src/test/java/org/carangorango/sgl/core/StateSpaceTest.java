package org.carangorango.sgl.core;

import com.google.common.collect.ImmutableSet;
import org.apache.commons.math3.fraction.Fraction;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class StateSpaceTest {

    @Test(expected = NullPointerException.class)
    public void factoryMethodShouldNotAcceptNullArgument() throws Exception {
        StateSpace.createUniform(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldNotAcceptEmptyArgument() throws Exception {
        StateSpace.createUniform(ImmutableSet.of());
    }

    @Test
    public void factoryMethodShouldCorrectlyAttributeUniformProbabilities() throws Exception {
        StateSpace<String> stateSpace = StateSpace.createUniform(ImmutableSet.of("A"));
        assertEquals(Fraction.ONE, stateSpace.getPriorProbability("A"));

        stateSpace = StateSpace.createUniform(ImmutableSet.of("A", "B"));
        assertEquals(Fraction.ONE_HALF, stateSpace.getPriorProbability("A"));
        assertEquals(Fraction.ONE_HALF, stateSpace.getPriorProbability("B"));

        stateSpace = StateSpace.createUniform(ImmutableSet.of("A", "B", "C"));
        assertEquals(Fraction.ONE_THIRD, stateSpace.getPriorProbability("A"));
        assertEquals(Fraction.ONE_THIRD, stateSpace.getPriorProbability("B"));
        assertEquals(Fraction.ONE_THIRD, stateSpace.getPriorProbability("C"));
    }

}