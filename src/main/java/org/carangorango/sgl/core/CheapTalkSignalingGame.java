package org.carangorango.sgl.core;

import java.util.Optional;

public abstract class CheapTalkSignalingGame<S, M, A> extends SignalingGame<S, M, A> {

    @Override
    protected final Payoff utility(S state, Optional<M> message, A action) {
        return this.utility(state, action);
    }

    public abstract Payoff utility(S state, A action);

}
