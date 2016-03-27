package org.carangorango.sgl.games;

import org.carangorango.sgl.core.CheapTalkSignalingGame;
import org.carangorango.sgl.core.MetricSpace;
import org.carangorango.sgl.core.Payoff;
import org.carangorango.sgl.core.StateSpace;

import java.util.Set;

public class NosofskySimMaxGame<S, M> implements CheapTalkSignalingGame<S, M, S> {

    private MetricSpace<S> stateSpace;
    private Set<M> messages;
    private Double scalingFactor;

    public NosofskySimMaxGame(MetricSpace<S> stateSpace, Set<M> messages, Double scalingFactor) {
        this.stateSpace = stateSpace;
        this.messages = messages;
        this.scalingFactor = scalingFactor;
    }

    @Override
    public StateSpace<S> getStateSpace() {
        return this.stateSpace;
    }

    @Override
    public Set<M> getMessages() {
        return this.messages;
    }

    @Override
    public Set<S> getActions() {
        return this.stateSpace.getStates();
    }

    @Override
    public Payoff utility(S state1, S state2) {
        Double payoff = Math.exp(-scalingFactor *
                Math.pow(this.stateSpace.distance(state1, state2).doubleValue(), 2));
        return new Payoff(payoff, payoff);

    }
}
