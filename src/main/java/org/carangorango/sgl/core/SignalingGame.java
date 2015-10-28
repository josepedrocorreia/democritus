package org.carangorango.sgl.core;

import java.util.Optional;
import java.util.Set;

public abstract class SignalingGame<S, M, A> {

    private Set<S> states;
    private Set<M> messages;
    private Set<A> actions;

    protected abstract Payoff utility(S state, Optional<M> message, A action);

    public SignalingGame(Set<S> states, Set<M> messages, Set<A> actions) {
        this.states = states;
        this.messages = messages;
        this.actions = actions;
    }

    public Set<S> getStates() {
        return states;
    }

    public Set<M> getMessages() {
        return messages;
    }

    public Set<A> getActions() {
        return actions;
    }
}
