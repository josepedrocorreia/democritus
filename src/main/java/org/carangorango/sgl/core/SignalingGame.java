package org.carangorango.sgl.core;

import java.util.Optional;
import java.util.Set;

public interface SignalingGame<S, M, A> {

    Set<S> getStates();

    Set<M> getMessages();

    Set<A> getActions();

    Payoff utility(S state, Optional<M> message, A action);

}
