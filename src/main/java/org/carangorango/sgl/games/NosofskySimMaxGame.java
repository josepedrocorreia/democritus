package org.carangorango.sgl.games;

import org.carangorango.sgl.core.CheapTalk;
import org.carangorango.sgl.core.MetricSpace;
import org.carangorango.sgl.core.Payoff;
import org.carangorango.sgl.core.SignalingGame;

import java.util.Optional;
import java.util.Set;

public class NosofskySimMaxGame<S, M> extends SignalingGame<S, M, S> implements CheapTalk<S, S> {

    private MetricSpace<S> states;
    private Set<M> messages;
    private Double scalingFactor;

    public NosofskySimMaxGame(MetricSpace<S> states, Set<M> messages, Double scalingFactor) {
        this.states = states;
        this.messages = messages;
        this.scalingFactor = scalingFactor;
    }

    @Override
    public Set<S> getStates() {
        return this.states;
    }

    @Override
    public Set<M> getMessages() {
        return this.messages;
    }

    @Override
    public Set<S> getActions() {
        return this.states;
    }

    @Override
    protected Payoff utility(S state1, Optional<M> message, S state2) {
        Double payoff = Math.exp(-scalingFactor *
                Math.pow(this.states.distance(state1, state2).doubleValue(), 2));
        return new Payoff(payoff, payoff);
    }

    @Override
    public Payoff utility(S state1, S state2) {
        return this.utility(state1, Optional.<M>empty(), state2);
    }
}
