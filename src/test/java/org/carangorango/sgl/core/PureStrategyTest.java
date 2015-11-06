package org.carangorango.sgl.core;

import com.google.common.collect.ImmutableMap;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class PureStrategyTest {

    private PureStrategy<Integer, Integer> strategy;

    @Before
    public void createExample() throws Exception {
        this.strategy = new PureStrategy<>(ImmutableMap.<Integer, Integer>builder()
                .put(1, 1)
                .put(2, 2)
                .put(3, 2)
                .build());
    }

    @Test
    public void shouldPlayCorrectly() throws Exception {
        assertEquals(Integer.valueOf(1), strategy.play(1));
        assertEquals(Integer.valueOf(2), strategy.play(2));
        assertEquals(Integer.valueOf(2), strategy.play(3));
    }

    @Test(expected = NullPointerException.class)
    public void shouldNotAllowNullArgumentToConstructor() {
        new PureStrategy<>(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void shouldNotAllowEmptyMapArgumentToConstructor() {
        new PureStrategy<>(ImmutableMap.of());
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