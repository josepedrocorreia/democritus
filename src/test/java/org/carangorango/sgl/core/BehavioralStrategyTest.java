package org.carangorango.sgl.core;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableTable;
import org.apache.commons.math3.util.Pair;
import org.junit.BeforeClass;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class BehavioralStrategyTest {

    private static BehavioralStrategy<Integer, Integer> strategy;

    @BeforeClass
    public static void createExampleStrategy() {
        strategy = BehavioralStrategy.createBehavioralStrategy(
                ImmutableTable.<Integer, Integer, Double>builder()
                        .put(1, 1, 0.1)
                        .put(1, 2, 0.9)
                        .put(2, 1, 0.2)
                        .put(2, 2, 0.8)
                        .build());
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldThrowExceptionOnNullArgument() throws Exception {
        BehavioralStrategy.createBehavioralStrategy(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldThrowExceptionOnEmptyTableArgument() throws Exception {
        BehavioralStrategy.createBehavioralStrategy(ImmutableTable.<Integer, Integer, Double>of());
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldThrowExceptionOnMissingColumns1() throws Exception {
        BehavioralStrategy.createBehavioralStrategy(
                ImmutableTable.<Integer, Integer, Double>builder()
                        .put(1, 1, 1.0)
                        .put(2, 1, 0.5)
                        .put(2, 2, 0.5)
                        .build());
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldThrowExceptionOnMissingColumns2() throws Exception {
        BehavioralStrategy.createBehavioralStrategy(
                ImmutableTable.<Integer, Integer, Double>builder()
                        .put(1, 1, 0.5)
                        .put(1, 2, 0.5)
                        .put(2, 1, 1.0)
                        .build());
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldThrowExceptionIfSomeRowIsNotProperPmf1() throws Exception {
        BehavioralStrategy.createBehavioralStrategy(
                ImmutableTable.<Integer, Integer, Double>builder()
                        .put(1, 1, 0.5).build());
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldThrowExceptionIfSomeRowIsNotProperPmf2() throws Exception {
        BehavioralStrategy.createBehavioralStrategy(
                ImmutableTable.<Integer, Integer, Double>builder()
                        .put(1, 1, 0.5)
                        .put(1, 2, 0.5001)
                        .build());
    }

    @Test(expected = IllegalArgumentException.class)
    public void factoryMethodShouldThrowExceptionIfSomeRowIsNotProperPmf3() throws Exception {
        BehavioralStrategy.createBehavioralStrategy(
                ImmutableTable.<Integer, Integer, Double>builder()
                        .put(1, 1, 0.5)
                        .put(1, 2, 0.5)
                        .put(2, 1, 0.5)
                        .put(2, 2, 0.5001)
                        .build());
    }

    @Test(expected = IllegalArgumentException.class)
    public void shouldThrowExceptionForUnknownInformation() throws Exception {
        strategy.expectedPlay(-1);
    }

    @Test
    public void shouldReturnCorrectExpectedPlays() throws Exception {
        assertEquals(ImmutableList.of(new Pair<>(1, 0.1), new Pair<>(2, 0.9)),
                strategy.expectedPlay(1).getPmf());
        assertEquals(ImmutableList.of(new Pair<>(1, 0.2), new Pair<>(2, 0.8)),
                strategy.expectedPlay(2).getPmf());
    }

    @Test
    public void shouldReturnCorrectPlays() throws Exception {
        assertTrue(ImmutableList.of(1, 2).contains(strategy.play(1)));
        assertTrue(ImmutableList.of(1, 2).contains(strategy.play(2)));
    }

}