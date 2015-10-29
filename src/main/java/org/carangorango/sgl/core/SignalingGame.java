package org.carangorango.sgl.core;

import java.util.Optional;
import java.util.Set;

public abstract class SignalingGame<S, M, A> {

    public abstract Set<S> getStates();

    public abstract Set<M> getMessages();

    public abstract Set<A> getActions();

    protected abstract Payoff utility(S state, Optional<M> message, A action);

}
