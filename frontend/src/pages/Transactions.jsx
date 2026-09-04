import { useMemo, useState } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Search,
} from "lucide-react";

function Transactions({
  transactions,
  onSelectTransaction,
}) {
  const [search, setSearch] = useState("");
  const [riskFilter, setRiskFilter] = useState("ALL");
  const [methodFilter, setMethodFilter] = useState("ALL");
  const [decisionFilter, setDecisionFilter] = useState("ALL");

  const filteredTransactions = useMemo(() => {
    const query = search.trim().toLowerCase();

    return transactions.filter((transaction) => {
      const matchesSearch =
        !query ||
        [
          transaction.id,
          transaction.amount,
          transaction.payment_method,
          transaction.risk_level,
          transaction.review_decision,
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase()
          .includes(query);

      const matchesRisk =
        riskFilter === "ALL" ||
        transaction.risk_level === riskFilter;

      const matchesMethod =
        methodFilter === "ALL" ||
        transaction.payment_method === methodFilter;

      const decision =
        transaction.review_decision || "PENDING";

      const matchesDecision =
        decisionFilter === "ALL" ||
        decision === decisionFilter;

      return (
        matchesSearch &&
        matchesRisk &&
        matchesMethod &&
        matchesDecision
      );
    });
  }, [
    transactions,
    search,
    riskFilter,
    methodFilter,
    decisionFilter,
  ]);

  return (
    <div className="page-container">

      <div className="page-top">

        <div>
          <h2>Transactions</h2>
          <p>
            Search and review payment transactions
          </p>
        </div>

      </div>

      <div className="filters-panel">

        <div className="transaction-search">
          <Search size={17} />

          <input
            placeholder="Search transactions..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
          />
        </div>

        <select
          value={riskFilter}
          onChange={(e) =>
            setRiskFilter(e.target.value)
          }
        >
          <option value="ALL">
            All Risk Levels
          </option>
          <option value="HIGH">
            High Risk
          </option>
          <option value="MEDIUM">
            Medium Risk
          </option>
          <option value="LOW">
            Low Risk
          </option>
        </select>

        <select
          value={methodFilter}
          onChange={(e) =>
            setMethodFilter(e.target.value)
          }
        >
          <option value="ALL">
            All Methods
          </option>
          <option value="UPI">UPI</option>
          <option value="CARD">CARD</option>
          <option value="NETBANKING">
            NETBANKING
          </option>
          <option value="WALLET">
            WALLET
          </option>
        </select>

        <select
          value={decisionFilter}
          onChange={(e) =>
            setDecisionFilter(e.target.value)
          }
        >
          <option value="ALL">
            All Decisions
          </option>
          <option value="PENDING">
            Pending
          </option>
          <option value="ALLOW">
            Allow
          </option>
          <option value="REVIEW">
            Review
          </option>
          <option value="BLOCK">
            Block
          </option>
        </select>

      </div>

      <div className="panel transactions-page-panel">

        <div className="transactions-count">
          {filteredTransactions.length} transaction{filteredTransactions.length !== 1 ? "s" : ""}
        </div>

        <div className="table-wrapper">

          <table>

            <thead>
              <tr>
                <th>Transaction</th>
                <th>Amount</th>
                <th>Method</th>
                <th>Risk Score</th>
                <th>Risk Level</th>
                <th>Decision</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>

              {filteredTransactions.map((transaction) => {
                return (
                <tr
                  key={transaction.id}
                  onClick={() => onSelectTransaction(transaction.id)}
                  className="clickable-row"
                >
                  <td>
                    <strong>#{transaction.id}</strong>
                  </td>
                  <td>
                    Rs.
                    {Number(transaction.amount).toLocaleString("en-IN")}
                  </td>
                  <td>
                    <span className={`method-badge ${transaction.payment_method.toLowerCase()}`}>
                      {transaction.payment_method}
                    </span>
                  </td>
                  <td>
                    <div className="table-score">
                      <strong>{transaction.risk_score}</strong>
                      <span>/100</span>
                    </div>
                  </td>
                  <td>
                    <span className={`risk-badge ${transaction.risk_level.toLowerCase()}`}>
                      {transaction.risk_level}
                    </span>
                  </td>
                  <td>
                    <span className="decision-badge">
                      {transaction.review_decision || "PENDING"}
                    </span>
                  </td>
                  <td>
                    <ChevronRight size={16} />
                  </td>
                </tr>
                );
              })}

            </tbody>

          </table>

        </div>

        {filteredTransactions.length === 0 && (
          <div className="empty-page">
            No transactions match your filters.
          </div>
        )}

        <div className="table-footer">

          <span>
            Showing {filteredTransactions.length}
          </span>

          <div className="pagination">
            <button>
              <ChevronLeft size={16} />
            </button>

            <button className="page-active">
              1
            </button>

            <button>
              <ChevronRight size={16} />
            </button>
          </div>

        </div>

      </div>

    </div>
  );
}

export default Transactions;
