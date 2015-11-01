package org.carangorango.sgl.statespaces;

import com.google.common.collect.ImmutableSet;
import org.apache.commons.math3.fraction.Fraction;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class UnitIntervalTest {

    @Test(expected = IllegalArgumentException.class)
    public void testInvalidConstructorCall1() {
        new UnitInterval(1);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testInvalidConstructorCall2() {
        new UnitInterval(0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testInvalidConstructorCall3() {
        new UnitInterval(-1);
    }

    @Test
    public void testValidConstructorCall() {
        UnitInterval interval = new UnitInterval(3);
        assertEquals(ImmutableSet.of(new Fraction(0), new Fraction(1, 2), new Fraction(1)), interval.getPoints());
    }

    @Test
    public void testDistance() throws Exception {
        UnitInterval interval = new UnitInterval(3);
        Fraction x1 = new Fraction(0);
        Fraction x2 = new Fraction(1, 2);
        Fraction x3 = new Fraction(1);
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