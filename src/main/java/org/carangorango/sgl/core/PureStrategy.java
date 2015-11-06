package org.carangorango.sgl.core;

import java.util.Map;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;

public final class PureStrategy<I, C> implements SignalingStrategy<I, C> {

    private Map<I, C> choiceFunction;

    public PureStrategy(Map<I, C> choiceFunction) {
        checkNotNull(choiceFunction);
        checkArgument(choiceFunction.size() > 0, "Choice function should have at least one mapping");
        this.choiceFunction = choiceFunction;
    }

    @Override
    public C play(I information) {
        checkNotNull(information);
        checkArgument(this.choiceFunction.containsKey(information));
        return choiceFunction.get(information);
    }

}
