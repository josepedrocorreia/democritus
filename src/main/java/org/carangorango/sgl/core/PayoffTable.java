package org.carangorango.sgl.core;

import com.google.common.collect.ArrayTable;
import com.google.common.collect.Table;

import java.util.List;
import java.util.Set;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.collect.Lists.newArrayList;

public class PayoffTable<S, A> {

    private Table<S, A, Payoff> payoffTable;

    public PayoffTable(Table<S, A, Payoff> payoffTable) {
        checkArgument(payoffTable != null, "Payoff table cannot be null");
        checkArgument(payoffTable.size() > 0, "Payoff table cannot be empty");
        this.payoffTable = payoffTable;
    }

    public Payoff get(S state, A action) {
        checkArgument(payoffTable.containsRow(state), "Unknown state %s", state);
        checkArgument(payoffTable.containsColumn(action), "Unknown action %s", action);
        return payoffTable.get(state, action);
    }

    public static <R, C> PayoffTable<R, C> createPureCoordinationTable(Set<R> rows, Set<C> columns, double[][] payoffs) {
        return createTable(rows, columns, payoffs, payoffs);
    }

    public static <R, C> PayoffTable<R, C> createTable(Set<R> rows, Set<C> columns, double[][] senderPayoffs, double[][] receiverPayoffs) {
        checkArgument(rows != null && columns != null && senderPayoffs != null && receiverPayoffs != null,
                "Arguments cannot be null");
        checkArgument(rows.size() > 0 && columns.size() > 0,
                "Rows and columns must both have at least one element");
        checkArgument(senderPayoffs.length == rows.size() && receiverPayoffs.length == rows.size());
        checkArgument(senderPayoffs[0].length == columns.size() && receiverPayoffs[0].length == columns.size());
        Table<R, C, Payoff> table = ArrayTable.create(rows, columns);
        List<R> rowsList = newArrayList(rows);
        List<C> columnsList = newArrayList(columns);
        for (int i = 0; i < rows.size(); i++) {
            for (int j = 0; j < columns.size(); j++) {
                table.put(rowsList.get(i), columnsList.get(j), new Payoff(senderPayoffs[i][j], receiverPayoffs[i][j]));
            }
        }
        return new PayoffTable<>(table);
    }

}
