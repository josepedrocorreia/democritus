package org.carangorango.sgl.statespaces;

import com.google.common.collect.ImmutableSet;
import org.apache.commons.math3.fraction.Fraction;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class UnitIntervalTest {

    @Test(expected = IllegalArgumentException.class)
    public void testInvalidConstructorCall1() {
        UnitInterval.createUnitInterval(1);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testInvalidConstructorCall2() {
        UnitInterval.createUnitInterval(0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testInvalidConstructorCall3() {
        UnitInterval.createUnitInterval(-1);
    }

    @Test
    public void testValidConstructorCall() {
        UnitInterval interval = UnitInterval.createUnitInterval(3);
        assertEquals(ImmutableSet.of(Fraction.ZERO, Fraction.ONE_HALF, Fraction.ONE), interval.getStates());
    }

    @Test
    public void testDistance() throws Exception {
        UnitInterval interval = UnitInterval.createUnitInterval(3);
        Fraction x1 = Fraction.ZERO;
        Fraction x2 = Fraction.ONE_HALF;
        Fraction x3 = Fraction.ONE;
        // coincidence
        assertEquals(0.0, interval.distance(x1, x1).doubleValue(), 0.0);
        // symmetry
        assertEquals(0.5, interval.distance(x1, x2).doubleValue(), 0.0);
        assertEquals(0.5, interval.distance(x2, x1).doubleValue(), 0.0);
        assertEquals(0.5, interval.distance(x2, x3).doubleValue(), 0.0);
        assertEquals(0.5, interval.distance(x3, x2).doubleValue(), 0.0);
        // triangle inequality
        assertEquals(0.5, interval.distance(x1, x2).doubleValue(), 0.0);
        assertEquals(0.5, interval.distance(x2, x3).doubleValue(), 0.0);
        assertEquals(1.0, interval.distance(x1, x3).doubleValue(), 0.0);
    }

}