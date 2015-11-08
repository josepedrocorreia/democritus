package org.carangorango.sgl.core;

import java.util.Optional;

public interface CheapTalkSignalingGame<S, M, A> extends SignalingGame<S, M, A> {

    @Override
    default Payoff utility(S state, Optional<M> message, A action) {
        return this.utility(state, action);
    }

    Payoff utility(S state, A action);

}
