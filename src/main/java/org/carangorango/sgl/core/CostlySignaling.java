package org.carangorango.sgl.core;

public interface CostlySignaling<S, M, A> {

    Payoff utility(S state, M message, A action);

}
