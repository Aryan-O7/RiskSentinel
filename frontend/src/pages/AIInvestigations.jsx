import { useMemo, useState } from "react";
import {
  AlertTriangle,
  BrainCircuit,
  CheckCircle2,
  Eye,
  Search,
  ShieldAlert,
  Sparkles,
  XCircle,
} from "lucide-react";

function AIInvestigations({
  transactions,
  onSelectTransaction,
  selectedTransaction,
  investigation,
  investigating,
  onRunInvestigation,
  onReview,
}) {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("ALL");

  const investigations = useMemo(() => {
    return transactions
      .filter((transaction) => {
        const matchesRisk =
          filter === "ALL" ||
          transaction.risk_level === filter;

        const query = search.trim().toLowerCase();

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

        return matchesRisk && matchesSearch;
      })
      .sort(
        (a, b) =>
          Number(b.risk_score) -
          Number(a.risk_score)
      );
  }, [transactions, search, filter]);

  const highRiskCount = transactions.filter(
    (t) => t.risk_level === "HIGH"
  ).length;

  const investigatedCount = transactions.filter(
    (t) =>
      t.review_decision ||
      t.risk_reasons
  ).length;

  return (
    <div className="page-container">

      {/* HEADER */}

      <div className="page-top investigations-page-top">

        <div>
          <div className="eyebrow">
            AI-ASSISTED RISK OPERATIONS
          </div>

          <h2>AI Investigations</h2>

          <p>
            Investigate suspicious transactions and
            review AI-generated risk assessments.
          </p>
        </div>

        <div className="investigation-header-stats">

          <div>
            <span>HIGH RISK</span>
            <strong>{highRiskCount}</strong>
          </div>

          <div>
            <span>CASES</span>
            <strong>{investigatedCount}</strong>
          </div>

        </div>

      </div>


      {/* TOOLBAR */}

      <div className="investigations-toolbar">

        <div className="transaction-search">

          <Search size={16} />

          <input
            placeholder="Search transaction..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
          />

        </div>

        <select
          value={filter}
          onChange={(e) =>
            setFilter(e.target.value)
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

      </div>


      {/* MAIN GRID */}

      <div className="investigations-grid">

        {/* CASE LIST */}

        <div className="panel investigation-list-panel">

          <div className="panel-header">

            <div>
              <h3>Investigation Queue</h3>

              <p>
                Highest-risk cases appear first
              </p>
            </div>

            <BrainCircuit size={18} />

          </div>


          <div className="case-list">

            {investigations.map(
              (transaction) => { return (

              <button
                key={transaction.id}
                className={`case-item ${
                  selectedTransaction?.id ===
                  transaction.id
                    ? "selected"
                    : ""
                }`}
                onClick={() =>
                  onSelectTransaction(
                    transaction.id
                  )
                }
              >

                <div className="case-icon">

                  <ShieldAlert size={17} />

                </div>

                <div className="case-main">

                  <div className="case-title">

                    <strong>
                      Transaction #
                      {transaction.id}
                    </strong>

                    <span
                      className={`risk-badge ${transaction.risk_level.toLowerCase()}`}
                    >
                      {transaction.risk_level}
                    </span>

                  </div>

                  <div className="case-meta">

                    <span>
                      Rs.
                      {Number(
                        transaction.amount
                      ).toLocaleString(
                        "en-IN"
                      )}
                    </span>

                    <span>
                      Risk{" "}
                      {transaction.risk_score}/100
                    </span>

                  </div>

                </div>

              </button>

            ); })}


            {investigations.length === 0 && (
              <div className="empty-page">
                No investigations found.
              </div>
            )}

          </div>

        </div>


        {/* INVESTIGATION DETAIL */}

        <div className="panel investigation-detail-panel">

          {!selectedTransaction ? (

            <div className="empty-investigation">

              <BrainCircuit size={38} />

              <h2>
                Select an Investigation
              </h2>

              <p>
                Choose a transaction from the queue
                to inspect its risk assessment.
              </p>

            </div>

          ) : (

            <>

              {/* HEADER */}

              <div className="investigation-detail-header">

                <div>
                  <div className="small-label">
                    INVESTIGATION
                  </div>

                  <h2>
                    Transaction #
                    {selectedTransaction.id}
                  </h2>
                </div>

                <span
                  className={`risk-badge ${selectedTransaction.risk_level.toLowerCase()}`}
                >
                  {selectedTransaction.risk_level}
                </span>

              </div>


              {/* RISK SCORE */}

              <div className="investigation-section">

                <div className="section-heading">
                  Risk Assessment
                </div>

                <div className="investigation-risk-row">

                  <div>

                    <div className="investigation-score-large">
                      {
                        selectedTransaction.risk_score
                      }

                      <span>
                        /100
                      </span>
                    </div>

                    <div className="investigation-score-subtitle">
                      Model-generated risk score
                    </div>

                  </div>

                  <div className="investigation-action">

                    <span>
                      Recommended Action
                    </span>

                    <strong>
                      {
                        selectedTransaction.recommended_action
                      }
                    </strong>

                  </div>

                </div>

                <div className="risk-gradient-bar">

                  <div
                    className="risk-marker"
                    style={{
                      left: `${selectedTransaction.risk_score}%`,
                    }}
                  />

                </div>

              </div>


              {/* FACTORS */}

              <div className="investigation-section">

                <div className="section-heading">

                  Risk Factors

                  <span className="count-badge">
                    {
                      selectedTransaction
                        .risk_reasons?.length || 0
                    }
                  </span>

                </div>

                <div className="investigation-factors">

                  {(
                    selectedTransaction
                      .risk_reasons || []
                  ).map(
                    (reason, index) => { return (

                    <div
                      key={index}
                      className="investigation-factor"
                    >

                      <AlertTriangle size={15} />

                      <span>
                        {reason}
                      </span>

                    </div>

                  ); })}

                </div>

              </div>


              {/* AI */}

              <div className="investigation-section ai-investigation-section">

                <div className="section-heading">

                  <Sparkles size={15} />

                  AI Investigation

                  <span className="beta-badge">
                    BETA
                  </span>

                </div>

                <p className="ai-description">
                  Generate a structured investigation
                  based on the existing ML risk signals.
                </p>

                <button
                  className="ai-button"
                  disabled={investigating}
                  onClick={() =>
                    onRunInvestigation(
                      selectedTransaction.id
                    )
                  }
                >

                  <Sparkles size={16} />

                  {investigating
                    ? "Investigating..."
                    : "Run AI Investigation"}

                </button>

                {investigation && (
                  <div className="investigation-ai-result">
                    <pre>
                      {investigation}
                    </pre>
                  </div>
                )}

              </div>


              {/* REVIEW */}

              <div className="investigation-section">

                <div className="section-heading">
                  Human Review
                </div>

                <div className="investigation-review-buttons">

                  <button
                    className="review-button allow"
                    onClick={() =>
                      onReview(
                        selectedTransaction.id,
                        "ALLOW"
                      )
                    }
                  >
                    <CheckCircle2 size={15} />
                    ALLOW
                  </button>

                  <button
                    className="review-button review"
                    onClick={() =>
                      onReview(
                        selectedTransaction.id,
                        "REVIEW"
                      )
                    }
                  >
                    <Eye size={15} />
                    REVIEW
                  </button>

                  <button
                    className="review-button block"
                    onClick={() =>
                      onReview(
                        selectedTransaction.id,
                        "BLOCK"
                      )
                    }
                  >
                    <XCircle size={15} />
                    BLOCK
                  </button>

                </div>

                <div className="investigation-decision">

                  Current Decision:

                  <strong>
                    {" "}
                    {selectedTransaction.review_decision ||
                      "PENDING"}
                  </strong>

                </div>

              </div>

            </>

          )}

        </div>

      </div>

    </div>
  );
}

export default AIInvestigations;
