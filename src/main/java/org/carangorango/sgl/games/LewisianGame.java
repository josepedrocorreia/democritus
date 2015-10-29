package org.carangorango.sgl.games;

import org.carangorango.sgl.core.CheapTalk;
import org.carangorango.sgl.core.Payoff;
import org.carangorango.sgl.core.PayoffTable;
import org.carangorango.sgl.core.SignalingGame;

import java.util.Optional;
import java.util.Set;

public class LewisianGame<S, M, A> extends SignalingGame<S, M, A> implements CheapTalk<S, A> {

    private Set<S> states;
    private Set<M> messages;
    private Set<A> actions;
    private PayoffTable<S, A> payoffTable;

    public LewisianGame(Set<S> states, Set<M> messages, Set<A> actions, PayoffTable<S, A> payoffTable) {
        this.states = states;
        this.messages = messages;
        this.actions = actions;
        this.payoffTable = payoffTable;
    }

    public Set<S> getStates() {
        return this.states;
    }

    public Set<M> getMessages() {
        return this.messages;
    }

    public Set<A> getActions() {
        return this.actions;
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
