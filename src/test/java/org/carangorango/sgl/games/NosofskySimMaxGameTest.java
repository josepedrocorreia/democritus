package org.carangorango.sgl.games;

import com.google.common.collect.ImmutableSet;
import org.apache.commons.math3.fraction.Fraction;
import org.carangorango.sgl.statespaces.UnitInterval;
import org.junit.Test;

import java.util.Set;

import static org.junit.Assert.assertEquals;

public class NosofskySimMaxGameTest {

    @Test
    public void shouldAllowModelingSimpleUnitIntervalGame() {
        NosofskySimMaxGame<Fraction, String> game = new NosofskySimMaxGame<>(new UnitInterval(3), ImmutableSet.<String>of(), 0.5);
        Set<Fraction> expectedStates = ImmutableSet.of(new Fraction(0), new Fraction(1, 2), new Fraction(1));
        assertEquals(expectedStates, game.getStates());
        assertEquals(ImmutableSet.of(), game.getMessages());
        assertEquals(expectedStates, game.getActions());
        assertEquals(0.606, game.utility(new Fraction(0), new Fraction(1)).getSenderPayoff(), 0.001);
        assertEquals(0.606, game.utility(new Fraction(0), new Fraction(1)).getReceiverPayoff(), 0.001);
        assertEquals(0.882, game.utility(new Fraction(0), new Fraction(1, 2)).getSenderPayoff(), 0.001);
        assertEquals(0.882, game.utility(new Fraction(0), new Fraction(1, 2)).getReceiverPayoff(), 0.001);
        assertEquals(0.882, game.utility(new Fraction(1, 2), new Fraction(1)).getSenderPayoff(), 0.001);
        assertEquals(0.882, game.utility(new Fraction(1, 2), new Fraction(1)).getReceiverPayoff(), 0.001);
    }

}