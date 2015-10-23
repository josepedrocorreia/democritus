package org.carangorango.sgl.statespaces;

import com.google.common.base.Preconditions;
import org.apache.commons.math3.fraction.Fraction;
import org.carangorango.sgl.core.MetricSpace;

import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import java.util.stream.IntStream;

public class UnitInterval extends MetricSpace<Fraction> {

    private final Set<Fraction> points;

    public UnitInterval(int granularity) {
        Preconditions.checkArgument(granularity < 2,
                "Unit space granularity should not be lower than 2 but was %s", granularity);
        this.points = new HashSet<>();
        IntStream.range(0, granularity).forEach(
                i -> this.points.add(new Fraction(1, granularity - 1).multiply(i)));
    }

    @Override
    public Number distance(Fraction x, Fraction y) throws IllegalArgumentException {
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
