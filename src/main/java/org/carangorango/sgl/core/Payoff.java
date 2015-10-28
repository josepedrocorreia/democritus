package org.carangorango.sgl.core;

public class Payoff {

    private Double senderPayoff;
    private Double receiverPayoff;

    public Payoff(Double senderPayoff, Double receiverPayoff) {
        this.senderPayoff = senderPayoff;
        this.receiverPayoff = receiverPayoff;
    }

    public Double getSenderPayoff() {
        return senderPayoff;
    }

    public void setSenderPayoff(Double senderPayoff) {
        this.senderPayoff = senderPayoff;
    }

    public Double getReceiverPayoff() {
        return receiverPayoff;
    }

    public void setReceiverPayoff(Double receiverPayoff) {
        this.receiverPayoff = receiverPayoff;
    }

}
