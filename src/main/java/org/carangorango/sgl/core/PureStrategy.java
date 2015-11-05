package org.carangorango.sgl.core;

import java.util.Map;

public final class PureStrategy<I, C> implements SignalingStrategy<I, C> {

    private Map<I, C> choiceFunction;

    public PureStrategy(Map<I, C> choiceFunction) {
        this.choiceFunction = choiceFunction;
    }

    @Override
    public C play(I information) {
        return choiceFunction.get(information);
    }

}
