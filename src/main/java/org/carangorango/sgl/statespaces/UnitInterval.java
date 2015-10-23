package org.carangorango.sgl.statespaces;

import com.google.common.base.Preconditions;
import org.apache.commons.math3.fraction.Fraction;
import org.carangorango.sgl.core.MetricSpace;

import java.util.Set;
import java.util.TreeSet;
import java.util.stream.IntStream;

public class UnitInterval extends MetricSpace<Fraction> {

    private final Set<Fraction> points;

    public UnitInterval(int granularity) {
        Preconditions.checkArgument(granularity >= 2,
                "Granularity should be at least 2, but it was %s", granularity);
        this.points = new TreeSet<>();
        IntStream.range(0, granularity).forEach(
                i -> this.points.add(new Fraction(1, granularity - 1).multiply(i)));
    }

    public Set<Fraction> getPoints() {
        return points;
    }

    @Override
    public Number distance(Fraction x, Fraction y) throws IllegalArgumentException {
        Preconditions.checkArgument(points.contains(x), "Point %s is not contained in the interval", x);
        Preconditions.checkArgument(points.contains(y), "Point %s is not contained in the interval", y);
        return y.subtract(x).abs();
    }

}
