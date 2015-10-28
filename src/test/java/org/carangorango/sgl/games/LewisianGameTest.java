package org.carangorango.sgl.games;

import com.google.common.collect.ImmutableSet;
import org.carangorango.sgl.core.PayoffTable;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class LewisianGameTest {

    @Test
    public void shouldAllowModelingConventionFigure1() {
        ImmutableSet<String> states = ImmutableSet.of("R1", "R2", "R3");
        ImmutableSet<String> messages = ImmutableSet.of();
        ImmutableSet<String> actions = ImmutableSet.of("C1", "C2", "C3");
        PayoffTable<String, String> payoffTable =
                PayoffTable.createPureCoordinationTable(states, actions,
                        new double[][]{
                                {1.0, 0.0, 0.0},
                                {0.0, 1.0, 0.0},
                                {0.0, 0.0, 1.0}});
        LewisianGame<String, String, String> game = new LewisianGame<>(states, messages, actions, payoffTable);
        assertEquals(states, game.getStates());
        assertEquals(messages, game.getMessages());
        assertEquals(actions, game.getActions());
        assertEquals(Double.valueOf(1.0), game.utility("R1", "C1").getSenderPayoff());
        assertEquals(Double.valueOf(1.0), game.utility("R1", "C1").getReceiverPayoff());
    }

    @Test
    public void shouldAllowModelingConventionFigure2() {
        ImmutableSet<String> states = ImmutableSet.of("R1", "R2", "R3");
        ImmutableSet<String> messages = ImmutableSet.of();
        ImmutableSet<String> actions = ImmutableSet.of("C1", "C2", "C3");
        PayoffTable<String, String> payoffTable =
                PayoffTable.createTable(states, actions,
                        new double[][]{
                                {1.5, 0.5, 0.5},
                                {0.2, 1.2, 0.2},
                                {0.0, 0.0, 1.0}},
                        new double[][]{
                                {1.5, 0.2, 0.0},
                                {0.5, 1.2, 0.0},
                                {0.5, 0.2, 1.0}});
        LewisianGame<String, String, String> game = new LewisianGame<>(states, messages, actions, payoffTable);
        assertEquals(states, game.getStates());
        assertEquals(messages, game.getMessages());
        assertEquals(actions, game.getActions());
        assertEquals(Double.valueOf(1.5), game.utility("R1", "C1").getSenderPayoff());
        assertEquals(Double.valueOf(1.5), game.utility("R1", "C1").getReceiverPayoff());
        assertEquals(Double.valueOf(0.2), game.utility("R2", "C1").getSenderPayoff());
        assertEquals(Double.valueOf(0.5), game.utility("R2", "C1").getReceiverPayoff());
        assertEquals(Double.valueOf(0.5), game.utility("R1", "C2").getSenderPayoff());
        assertEquals(Double.valueOf(0.2), game.utility("R1", "C2").getReceiverPayoff());
    }

}