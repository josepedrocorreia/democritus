package org.carangorango.sgl.strategies;

import org.apache.commons.math3.distribution.EnumeratedDistribution;
import org.carangorango.sgl.core.SignalingStrategy;

public final class MixedStrategy<I, C> implements SignalingStrategy<I, C> {

    private EnumeratedDistribution<PureStrategy<I, C>> strategiesDistribution;

    protected MixedStrategy(EnumeratedDistribution<PureStrategy<I, C>> strategiesDistribution) {
        this.strategiesDistribution = strategiesDistribution;
    }

    @Override
    public C play(I information) {
        return this.strategiesDistribution.sample().play(information);
    }

}
