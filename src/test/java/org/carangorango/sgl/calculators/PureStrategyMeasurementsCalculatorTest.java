package org.carangorango.sgl.calculators;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableSet;
import org.carangorango.sgl.core.Payoff;
import org.carangorango.sgl.core.PayoffTable;
import org.carangorango.sgl.games.LewisianGame;
import org.carangorango.sgl.strategies.PureStrategy;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class PureStrategyMeasurementsCalculatorTest {

    private ImmutableSet<String> states = ImmutableSet.of("R1", "R2", "R3");
    private ImmutableSet<String> messages = ImmutableSet.of("M1", "M2", "M3");
    private ImmutableSet<String> actions = ImmutableSet.of("C1", "C2", "C3");

    private PureStrategyMeasurementsCalculator<String, String, String> calculator;

    @Before
    public void setUp() throws Exception {
        PayoffTable<String, String> payoffTable =
                PayoffTable.createPureCoordinationTable(states, actions,
                        new double[][]{
                                {1.0, 0.0, 0.0},
                                {0.0, 1.0, 0.0},
                                {0.0, 0.0, 1.0}});
        LewisianGame<String, String, String> gameConventionFigure1 =
                new LewisianGame<>(states, messages, actions, payoffTable);
        calculator = new PureStrategyMeasurementsCalculator<>(gameConventionFigure1);
    }

    @Test
    public void testExpectedUtilityForSeparatingEquilibria() throws Exception {
        PureStrategy<String, String> senderStrategy = PureStrategy.create(states, messages.asList());
        PureStrategy<String, String> receiverStrategy = PureStrategy.create(messages, actions.asList());
        Payoff payoff = calculator.calculateExpectedUtility(senderStrategy, receiverStrategy);
        assertEquals(Double.valueOf(1.0), payoff.getSenderPayoff());
        assertEquals(Double.valueOf(1.0), payoff.getReceiverPayoff());

        ImmutableList<String> messagesInReverseOrder = ImmutableList.of("M3", "M2", "M1");
        ImmutableList<String> actionsInReverseOrder = ImmutableList.of("C3", "C2", "C1");

        senderStrategy = PureStrategy.create(states, messagesInReverseOrder);
        receiverStrategy = PureStrategy.create(messages, actionsInReverseOrder);
        payoff = calculator.calculateExpectedUtility(senderStrategy, receiverStrategy);
        assertEquals(Double.valueOf(1.0), payoff.getSenderPayoff());
        assertEquals(Double.valueOf(1.0), payoff.getReceiverPayoff());
    }

    @Test
    public void testExpectedUtilityForBabblingEquilibria() throws Exception {
        ImmutableList<String> actionsInOtherOrder = ImmutableList.of("C3", "C1", "C2");

        PureStrategy<String, String> senderStrategy = PureStrategy.create(states, messages.asList());
        PureStrategy<String, String> receiverStrategy = PureStrategy.create(messages, actionsInOtherOrder);
        Payoff payoff = calculator.calculateExpectedUtility(senderStrategy, receiverStrategy);
        assertEquals(Double.valueOf(0.0), payoff.getSenderPayoff());
        assertEquals(Double.valueOf(0.0), payoff.getReceiverPayoff());
    }

    @Test
    public void testExpectedUtilityForPoolingEquilibria() throws Exception {
        ImmutableList<String> messagesInPoolingOrder = ImmutableList.of("M1", "M1", "M1");

        PureStrategy<String, String> senderStrategy = PureStrategy.create(states, messagesInPoolingOrder);
        PureStrategy<String, String> receiverStrategy = PureStrategy.create(messages, actions.asList());
        Payoff payoff = calculator.calculateExpectedUtility(senderStrategy, receiverStrategy);
        assertEquals(0.333, payoff.getSenderPayoff(), 0.001);
        assertEquals(0.333, payoff.getReceiverPayoff(), 0.001);

        ImmutableList<String> actionsInPoolingOrder = ImmutableList.of("C1", "C1", "C1");

        senderStrategy = PureStrategy.create(states, messagesInPoolingOrder);
        receiverStrategy = PureStrategy.create(messages, actionsInPoolingOrder);
        payoff = calculator.calculateExpectedUtility(senderStrategy, receiverStrategy);
        assertEquals(0.333, payoff.getSenderPayoff(), 0.001);
        assertEquals(0.333, payoff.getReceiverPayoff(), 0.001);

        senderStrategy = PureStrategy.create(states, messages.asList());
        receiverStrategy = PureStrategy.create(messages, actionsInPoolingOrder);
        payoff = calculator.calculateExpectedUtility(senderStrategy, receiverStrategy);
        assertEquals(0.333, payoff.getSenderPayoff(), 0.001);
        assertEquals(0.333, payoff.getReceiverPayoff(), 0.001);
    }

}