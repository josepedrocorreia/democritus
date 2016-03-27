package org.carangorango.sgl.strategies;

import com.google.common.collect.ImmutableSet;
import com.google.common.collect.Table;
import org.apache.commons.math3.distribution.EnumeratedDistribution;
import org.apache.commons.math3.fraction.Fraction;
import org.apache.commons.math3.util.Pair;
import org.carangorango.sgl.core.SignalingStrategy;

import java.util.Map;
import java.util.stream.Collectors;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;

public final class BehavioralStrategy<I, C> implements SignalingStrategy<I, C> {

    private Map<I, Map<C, Fraction>> behavior;

    protected BehavioralStrategy(Map<I, Map<C, Fraction>> behavior) {
        this.behavior = behavior;
    }

    public Map<C, Fraction> expectedPlay(I information) {
        checkArgument(behavior.containsKey(information), "Unknown information");
        return behavior.get(information);
    }

    public Fraction getPlayProbability(I information, C choice) {
        checkArgument(behavior.containsKey(information), "Unknown information");
        checkArgument(behavior.get(information).containsKey(choice), "Unknown choice");
        return behavior.get(information).get(choice);
    }

    @Override
    public C play(I information) {
        Map<C, Fraction> expectedPlay = this.expectedPlay(information);
        // TODO: Optimize
        EnumeratedDistribution<C> distribution =
                new EnumeratedDistribution<>(expectedPlay.entrySet().stream().map(
                        entry -> new Pair<>(entry.getKey(), entry.getValue().doubleValue())
                ).collect(Collectors.toList()));
        return distribution.sample();
    }

    // TODO: Simplify please, too freaking complex...
    public static <I, C> BehavioralStrategy<I, C> createBehavioralStrategy(Table<I, C, Fraction> probabilities)
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
                                .collect(Collectors.summingDouble(Fraction::doubleValue)) == 1),
                "Every row in the table should be a proper probability mass function over the set of choices");
        return new BehavioralStrategy<>(probabilities.rowMap());
    }

}
