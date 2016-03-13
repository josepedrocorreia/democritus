package org.carangorango.sgl.strategies;

import com.google.common.collect.ImmutableSet;
import com.google.common.collect.Table;
import org.apache.commons.math3.distribution.EnumeratedDistribution;
import org.apache.commons.math3.util.Pair;
import org.carangorango.sgl.core.SignalingStrategy;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;

public final class BehavioralStrategy<I, C> implements SignalingStrategy<I, C> {

    private Map<I, EnumeratedDistribution<C>> behavior;

    protected BehavioralStrategy(Map<I, EnumeratedDistribution<C>> behavior) {
        this.behavior = behavior;
    }

    public EnumeratedDistribution<C> expectedPlay(I information) {
        checkArgument(behavior.containsKey(information), "Unknown information");
        return this.behavior.get(information);
    }

    @Override
    public C play(I information) {
        return this.expectedPlay(information).sample();
    }

    // TODO: Simplify please, too freaking complex...
    public static <I, C> BehavioralStrategy<I, C> createBehavioralStrategy(Table<I, C, Double> probabilities)
            throws NullPointerException, IllegalArgumentException {
        checkNotNull(probabilities != null, "Argument should not be null");
        checkArgument(probabilities.size() != 0, "Probability map should not be empty");
        checkArgument(!probabilities.rowKeySet().stream()
                        .map(i -> probabilities.row(i).keySet())
                        .reduce((s1, s2) -> s1.equals(s2) ? s1 : ImmutableSet.of())
                        .get().isEmpty(),
                "Probability map should define probabilities for all information and choice combinations"
        );
        checkArgument(probabilities.rowKeySet().stream()
                        .allMatch(i -> probabilities.row(i).values().stream()
                                .collect(Collectors.summingDouble(Double::doubleValue)) == 1),
                "Every row in the table should be a proper probability mass function over the set of choices");
        HashMap<I, EnumeratedDistribution<C>> behavior = new HashMap<>();
        for (I information : probabilities.rowKeySet()) {
            List<Pair<C, Double>> pairList = probabilities.row(information).entrySet().stream().map(x -> new Pair<>(x.getKey(), x.getValue())).collect(Collectors.toList());
            behavior.put(information, new EnumeratedDistribution<>(pairList));
        }
        return new BehavioralStrategy<>(behavior);
    }

}
