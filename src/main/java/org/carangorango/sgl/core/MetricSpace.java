package org.carangorango.sgl.core;

import java.util.AbstractSet;

public abstract class MetricSpace<S> extends AbstractSet<S> implements Metric<S> {

    @Override
    public abstract Number distance(S x, S y) throws IllegalArgumentException;

}
