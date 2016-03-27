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
        NosofskySimMaxGame<Fraction, String> game = new NosofskySimMaxGame<>(UnitInterval.createUnitInterval(3), ImmutableSet.<String>of(), 0.5);
        Set<Fraction> expectedStates = ImmutableSet.of(Fraction.ZERO, Fraction.ONE_HALF, Fraction.ONE);
        assertEquals(expectedStates, game.getStateSpace().getStates());
        assertEquals(ImmutableSet.of(), game.getMessages());
        assertEquals(expectedStates, game.getActions());
        assertEquals(0.606, game.utility(Fraction.ZERO, Fraction.ONE).getSenderPayoff(), 0.001);
        assertEquals(0.606, game.utility(Fraction.ZERO, Fraction.ONE).getReceiverPayoff(), 0.001);
        assertEquals(0.882, game.utility(Fraction.ZERO, Fraction.ONE_HALF).getSenderPayoff(), 0.001);
        assertEquals(0.882, game.utility(Fraction.ZERO, Fraction.ONE_HALF).getReceiverPayoff(), 0.001);
        assertEquals(0.882, game.utility(Fraction.ONE_HALF, Fraction.ONE).getSenderPayoff(), 0.001);
        assertEquals(0.882, game.utility(Fraction.ONE_HALF, Fraction.ONE).getReceiverPayoff(), 0.001);
    }

}