package org.carangorango.sgl.strategies;

import org.carangorango.sgl.core.SignalingStrategy;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

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

    public static <I, C> PureStrategy<I, C> create(Set<I> informationSet, List<C> choices)
            throws NullPointerException, IllegalArgumentException {
        checkNotNull(informationSet);
        checkNotNull(choices);
        checkArgument(informationSet.size() > 0, "Information set should have at least one value");
        checkArgument(choices.size() > 0, "Choice set should have at least one value");
        checkArgument(informationSet.size() == choices.size(),
                "Information set and choice set should have the same number of values");
        HashMap<I, C> choiceFunction = new HashMap<>();
        int choiceIndex = 0;
        for (I info : informationSet) {
            choiceFunction.put(info, choices.get(choiceIndex));
            choiceIndex++;
        }
        return new PureStrategy<>(choiceFunction);
    }

}
