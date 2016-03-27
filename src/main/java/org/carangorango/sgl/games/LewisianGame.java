package org.carangorango.sgl.games;

import org.carangorango.sgl.core.CheapTalkSignalingGame;
import org.carangorango.sgl.core.Payoff;
import org.carangorango.sgl.core.PayoffTable;
import org.carangorango.sgl.core.StateSpace;

import java.util.Set;

public class LewisianGame<S, M, A> implements CheapTalkSignalingGame<S, M, A> {

    private StateSpace<S> states;
    private Set<M> messages;
    private Set<A> actions;
    private PayoffTable<S, A> payoffTable;

    public LewisianGame(Set<S> states, Set<M> messages, Set<A> actions, PayoffTable<S, A> payoffTable) {
        this.states = StateSpace.createUniform(states);
        this.messages = messages;
        this.actions = actions;
        this.payoffTable = payoffTable;
    }

    public StateSpace<S> getStateSpace() {
        return this.states;
    }

    public Set<M> getMessages() {
        return this.messages;
    }

    public Set<A> getActions() {
        return this.actions;
    }

    @Override
    public Payoff utility(S state, A action) {
        return this.payoffTable.get(state, action);
    }

}
