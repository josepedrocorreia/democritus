package org.carangorango.sgl.core;

import java.util.Map;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;

public final class PureStrategy<I, C> implements SignalingStrategy<I, C> {

    private Map<I, C> choiceFunction;

    protected PureStrategy(Map<I, C> choiceFunction) {
        this.choiceFunction = choiceFunction;
    }

    @Override
    public C play(I information) {
        checkNotNull(information);
        checkArgument(this.choiceFunction.containsKey(information));
        return choiceFunction.get(information);
    }

    public static <I, C> PureStrategy<I, C> create(Map<I, C> choiceFunction)
            throws NullPointerException, IllegalArgumentException {
        checkNotNull(choiceFunction);
        checkArgument(choiceFunction.size() > 0, "Choice function should have at least one mapping");
        return new PureStrategy<>(choiceFunction);
    }

}
