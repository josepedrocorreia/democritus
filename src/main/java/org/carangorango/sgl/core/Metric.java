package org.carangorango.sgl.core;

/**
 * Something is metric on T if it defines a metric or distance function on T.
 *
 * @param <T>  the type of the set on which the metric is defined
 */
public interface Metric<T> {

    Number distance(T x, T y) throws IllegalArgumentException;

}
