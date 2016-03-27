package org.carangorango.sgl.statespaces;

import com.google.common.base.Preconditions;
import org.apache.commons.math3.fraction.Fraction;
import org.carangorango.sgl.core.MetricSpace;

import java.util.HashSet;
import java.util.Set;

public class UnitInterval extends MetricSpace<Fraction> {

    @Override
    public Number distance(Fraction x, Fraction y) throws IllegalArgumentException {
        Preconditions.checkArgument(getStates().contains(x), "Point %s is not contained in the interval", x);
        Preconditions.checkArgument(getStates().contains(y), "Point %s is not contained in the interval", y);
        return y.subtract(x).abs();
    }

    public static UnitInterval createUnitInterval(int granularity) {
        Preconditions.checkArgument(granularity >= 2,
                "Granularity should be at least 2, but it was %s", granularity);
        Set<Fraction> states = new HashSet<>();
        for (int i = 0; i < granularity; i++) {
            states.add(new Fraction(1, granularity - 1).multiply(i));
        }
        Fraction statePriorProbability = new Fraction(1, states.size());
        UnitInterval unitInterval = new UnitInterval();
        for (Fraction state : states) {
            unitInterval.setPriorProbability(state, statePriorProbability);
        }
        return unitInterval;
    }

}
