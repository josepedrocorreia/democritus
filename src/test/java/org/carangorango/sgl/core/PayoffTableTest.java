package org.carangorango.sgl.core;

import com.google.common.collect.ArrayTable;
import com.google.common.collect.ImmutableSet;
import com.google.common.collect.ImmutableTable;
import org.junit.BeforeClass;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class PayoffTableTest {

    private static PayoffTable<Integer, Integer> matrix1;

    @BeforeClass
    public static void createSymmetricPayoffMatrices() {
        matrix1 = new PayoffTable<>(
                ImmutableTable.<Integer, Integer, Payoff>builder()
                        .put(1, 1, new Payoff(1.0, 1.0))
                        .put(1, 2, new Payoff(2.0, 2.0))
                        .put(2, 1, new Payoff(3.0, 3.0))
                        .put(2, 2, new Payoff(4.0, 4.0)).build());
    }

    @Test(expected = IllegalArgumentException.class)
    public void shouldThrowExceptionOnNullPayoffTable() {
        new PayoffTable<Integer, Integer>(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void shouldThrowExceptionOnEmptyPayoffTable() {
        new PayoffTable<>(ImmutableTable.<Integer, Integer, Payoff>builder().build());
    }

    @Test(expected = IllegalArgumentException.class)
    public void shouldThrowExceptionOnPayoffTableWithoutRows() {
        new PayoffTable<Integer, Integer>(
                ArrayTable.create(ImmutableSet.of(), ImmutableSet.of(1)));
    }

    @Test(expected = IllegalArgumentException.class)
    public void shouldThrowExceptionOnPayoffTableWithoutColumns() {
        new PayoffTable<Integer, Integer>(
                ArrayTable.create(ImmutableSet.of(1), ImmutableSet.of()));
    }

    @Test(expected = IllegalArgumentException.class)
    public void shouldThrowExceptionWhenStateIsUnknown() {
        matrix1.get(-1, 1);
    }

    @Test(expected = IllegalArgumentException.class)
    public void shouldThrowExceptionWhenActionIsUnknown() {
        matrix1.get(1, -1);
    }

    @Test
    public void shouldReturnCorrectSymmetricPayoffValues() {
        assertEquals(Double.valueOf(1.0), matrix1.get(1, 1).getSenderPayoff());
        assertEquals(Double.valueOf(1.0), matrix1.get(1, 1).getReceiverPayoff());
        assertEquals(Double.valueOf(2.0), matrix1.get(1, 2).getSenderPayoff());
        assertEquals(Double.valueOf(2.0), matrix1.get(1, 2).getReceiverPayoff());
        assertEquals(Double.valueOf(3.0), matrix1.get(2, 1).getSenderPayoff());
        assertEquals(Double.valueOf(3.0), matrix1.get(2, 1).getReceiverPayoff());
        assertEquals(Double.valueOf(4.0), matrix1.get(2, 2).getSenderPayoff());
        assertEquals(Double.valueOf(4.0), matrix1.get(2, 2).getReceiverPayoff());
    }

}