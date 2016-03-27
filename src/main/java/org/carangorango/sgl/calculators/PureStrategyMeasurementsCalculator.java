package org.carangorango.sgl.calculators;

import org.apache.commons.math3.fraction.Fraction;
import org.carangorango.sgl.core.Payoff;
import org.carangorango.sgl.core.SignalingGame;
import org.carangorango.sgl.core.StateSpace;
import org.carangorango.sgl.strategies.PureStrategy;

import java.util.Optional;

public class PureStrategyMeasurementsCalculator<S, M, A> {

    private SignalingGame<S, M, A> game;

    public PureStrategyMeasurementsCalculator(SignalingGame<S, M, A> game) {
        this.game = game;
    }

    public Payoff calculateExpectedUtility(PureStrategy<S, M> senderStrategy,
                                           PureStrategy<M, A> receiverStrategy) {
        // TODO: check arguments
        Fraction senderExpectedUtility = Fraction.ZERO;
        Fraction receiverExpectedUtility = Fraction.ZERO;
        StateSpace<S> stateSpace = game.getStateSpace();
        for (S state : stateSpace.getStates()) {
            Fraction statePriorProbability = stateSpace.getPriorProbability(state);
            M message = senderStrategy.play(state);
            A action = receiverStrategy.play(message);
            Payoff utility = game.utility(state, Optional.of(message), action);
            senderExpectedUtility = senderExpectedUtility.add(statePriorProbability.multiply(new Fraction(utility.getSenderPayoff())));
            receiverExpectedUtility = receiverExpectedUtility.add(statePriorProbability.multiply(new Fraction(utility.getReceiverPayoff())));
        }
        return new Payoff(senderExpectedUtility.doubleValue(), receiverExpectedUtility.doubleValue());
    }

}
