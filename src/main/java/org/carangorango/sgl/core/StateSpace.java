package org.carangorango.sgl.core;

import org.apache.commons.math3.fraction.Fraction;

import java.util.HashMap;
import java.util.Set;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;

public class StateSpace<S> {

    private HashMap<S, Fraction> priorProbabilities = new HashMap<>();

    public Set<S> getStates() {
        return this.priorProbabilities.keySet();
    }

    public Fraction getPriorProbability(S state) {
        return priorProbabilities.get(state);
    }

    public Fraction setPriorProbability(S state, Fraction priorProbability) {
        return priorProbabilities.put(state, priorProbability);
    }

    public static <S> StateSpace<S> createUniform(Set<S> states) {
        checkNotNull(states);
        checkArgument(states.size() > 0, "Set of states must be non-empty");
        Fraction statePriorProbability = new Fraction(1, states.size());
        StateSpace<S> uniformStateSpace = new StateSpace<>();
        for (S state : states) {
            uniformStateSpace.setPriorProbability(state, statePriorProbability);
        }
        return uniformStateSpace;
    }

}
