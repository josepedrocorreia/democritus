package org.carangorango.sgl.statespaces;

import com.google.common.collect.ImmutableSet;
import org.apache.commons.math3.fraction.Fraction;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class UnitIntervalTest {

    @Test
    public void testConstructor() {
        UnitInterval interval = new UnitInterval(3);
        assertEquals(ImmutableSet.of(new Fraction(0), new Fraction(1, 2), new Fraction(1)), interval.getPoints());
    }

    @Test
    public void testDistance() throws Exception {
        UnitInterval interval = new UnitInterval(3);
        Fraction x1 = new Fraction(0);
        Fraction x2 = new Fraction(1, 2);
        Fraction x3 = new Fraction(1);
        assertEquals(new Fraction(0), interval.distance(x1, x1));
        assertEquals(new Fraction(1, 2), interval.distance(x1, x2));
        assertEquals(new Fraction(1, 2), interval.distance(x2, x3));
        assertEquals(new Fraction(1, 2), interval.distance(x3, x2));
        assertEquals(new Fraction(1, 2), interval.distance(x2, x1));
    }
}