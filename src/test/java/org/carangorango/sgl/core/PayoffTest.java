package org.carangorango.sgl.core;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class PayoffTest {

    @Test
    public void shouldAllowNegativePayoffs() {
        Payoff payoff = new Payoff(-1.0, -2.0);
        assertEquals(Double.valueOf(-1.0), payoff.getSenderPayoff());
        assertEquals(Double.valueOf(-2.0), payoff.getReceiverPayoff());
    }

    @Test
    public void shouldAllowSettingPayoffs() {
        Payoff payoff = new Payoff(-1.0, -2.0);
        assertEquals(Double.valueOf(-1.0), payoff.getSenderPayoff());
        assertEquals(Double.valueOf(-2.0), payoff.getReceiverPayoff());
        payoff.setSenderPayoff(-3.0);
        payoff.setReceiverPayoff(-4.0);
        assertEquals(Double.valueOf(-3.0), payoff.getSenderPayoff());
        assertEquals(Double.valueOf(-4.0), payoff.getReceiverPayoff());
    }

}