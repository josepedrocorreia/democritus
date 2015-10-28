package org.carangorango.sgl.statespaces;

import com.google.common.base.Preconditions;
import org.apache.commons.math3.fraction.Fraction;
import org.carangorango.sgl.core.MetricSpace;

import java.util.Iterator;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class UnitInterval extends MetricSpace<Fraction> {

    private final Set<Fraction> points;

    public UnitInterval(int granularity) {
        Preconditions.checkArgument(granularity >= 2,
                "Granularity should be at least 2, but it was %s", granularity);
        this.points = IntStream.range(0, granularity).mapToObj(
                i -> new Fraction(1, granularity - 1).multiply(i)
        ).collect(Collectors.<Fraction>toSet());
    }

    public Set<Fraction> getPoints() {
        return points;
    }

    @Override
    public Number distance(Fraction x, Fraction y) throws IllegalArgumentException {
        Preconditions.checkArgument(this.contains(x), "Point %s is not contained in the interval", x);
        Preconditions.checkArgument(this.contains(y), "Point %s is not contained in the interval", y);
        return y.subtract(x).abs();
    }

    @Override
    public Iterator<Fraction> iterator() {
        return this.points.iterator();
    }

    @Override
    public int size() {
        return this.points.size();
    }
}
