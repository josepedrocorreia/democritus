package org.carangorango.sgl.games;

import org.carangorango.sgl.core.CheapTalk;
import org.carangorango.sgl.core.Payoff;
import org.carangorango.sgl.core.PayoffTable;
import org.carangorango.sgl.core.SignalingGame;

import java.util.Optional;
import java.util.Set;

public class LewisianGame<S, M, A> extends SignalingGame<S, M, A> implements CheapTalk<S, A> {

    private PayoffTable<S, A> payoffTable;

    public LewisianGame(Set<S> states, Set<M> messages, Set<A> actions, PayoffTable<S, A> payoffTable) {
        super(states, messages, actions);
        this.payoffTable = payoffTable;
    }

    @Override
    protected Payoff utility(S state, Optional<M> message, A action) {
        return this.payoffTable.get(state, action);
    }

    @Override
    public Payoff utility(S state, A action) {
        return this.utility(state, Optional.<M>empty(), action);
    }
}
