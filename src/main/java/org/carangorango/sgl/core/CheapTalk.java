package org.carangorango.sgl.core;

public interface CheapTalk<S, A> {

    Payoff utility(S state, A action);

}
