package org.carangorango.sgl.strategies;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableMap;
import com.google.common.collect.ImmutableSet;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class PureStrategyTest {

    private PureStrategy<Integer, Integer> strategy;

    @Before
    public void createExample() throws Exception {
        this.strategy = PureStrategy.create(ImmutableSet.of(1, 2, 3), ImmutableList.of(1, 2, 2));
    }

    @Test
    public void shouldPlayCorrectly() throws Exception {
        assertEquals(Integer.valueOf(1), strategy.play(1));
        assertEquals(Integer.valueOf(2), strategy.play(2));
        assertEquals(Integer.valueOf(2), strategy.play(3));
    }

    @Test(expected = NullPointerException.class)
    public void factoryMethodShouldNotAllowNullArgument() {
        PureStrategy.create(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldNotAllowEmptyMapArgument() {
        PureStrategy.create(ImmutableMap.of());
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldNotAllowEmptyInformationSetArgument() {
        PureStrategy.create(ImmutableSet.of(), ImmutableList.of("A"));
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldNotAllowEmptyChoiceListArgument() {
        PureStrategy.create(ImmutableSet.of("A"), ImmutableList.of());
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldNotAllowDifferentSizeArguments1() {
        PureStrategy.create(ImmutableSet.of("A"), ImmutableList.of("A", "B"));
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldNotAllowDifferentSizeArguments2() {
        PureStrategy.create(ImmutableSet.of("A", "B"), ImmutableList.of("A"));
    }

    @Test(expected = NullPointerException.class)
    public void shouldNotAllowNullArgumentToPlayMethod() {
        strategy.play(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void shouldNotAllowUnknownInformationArgumentToPlayMethod() {
        strategy.play(-1);
    }

}