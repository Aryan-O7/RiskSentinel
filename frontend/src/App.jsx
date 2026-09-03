import { useEffect, useState } from "react";
import axios from "axios";
import "./styles.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [transactions, setTransactions] = useState([]);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [investigation, setInvestigation] = useState("");
  const [investigating, setInvestigating] = useState(false);

  const fetchTransactions = async () => {
    try {
      setLoading(true);

      const response = await axios.get(
        `${API_URL}/api/v1/transactions`
      );

      setTransactions(response.data.data || []);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Unable to connect to RiskSentinel API.");
    } finally {
      setLoading(false);
    }
  };

  const fetchTransactionDetails = async (id) => {
    try {
      const response = await axios.get(
        `${API_URL}/api/v1/transactions/${id}`
      );

      setSelectedTransaction(response.data.data);
    } catch (err) {
      console.error(err);
      setError("Unable to load transaction details.");
    }
  };

  const submitReview = async (id, decision) => {
    try {
      await axios.post(
        `${API_URL}/api/v1/transactions/${id}/review`,
        null,
        {
          params: {
            decision: decision
          }
        }
      );

      await fetchTransactionDetails(id);
      await fetchTransactions();

    } catch (err) {
      console.error(err);
      setError("Unable to save review decision.");
    }
  };

  const runInvestigation = async (id) => {
    try {
      setInvestigating(true);
      setInvestigation("");

      const response = await axios.post(
        `${API_URL}/api/v1/transactions/${id}/investigate`
      );

      setInvestigation(
        response.data.investigation
      );

    } catch (err) {
      console.error(err);
      setError(
        "Unable to generate AI investigation."
      );
    } finally {
      setInvestigating(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const highRisk = transactions.filter(
    (t) => t.risk_level === "HIGH"
  ).length;

  const mediumRisk = transactions.filter(
    (t) => t.risk_level === "MEDIUM"
  ).length;

  const lowRisk = transactions.filter(
    (t) => t.risk_level === "LOW"
  ).length;

  return (
    <div className="app">

      {/* Header */}
      <header className="topbar">

        <div className="brand">

          <div className="brand-mark">
            R
          </div>

          <div>
            <h1>RiskSentinel</h1>
            <p>Payment Risk Intelligence</p>
          </div>

        </div>

        <div className="system-status">
          <span className="status-dot"></span>
          System Operational
          <button
            className="refresh-button"
            style={{marginLeft: '15px'}}
            onClick={fetchTransactions}
          >
            Refresh
          </button>
        </div>

      </header>

      {/* Statistics */}
      <section className="stats">

        <div className="stat-card">
          <div className="stat-label">
            TOTAL TRANSACTIONS
          </div>

          <div className="stat-value">
            {transactions.length}
          </div>

          <div className="stat-subtext">
            Processed by RiskSentinel
          </div>
        </div>


        <div className="stat-card">
          <div className="stat-label">
            HIGH RISK
          </div>

          <div className="stat-value">
            {highRisk}
          </div>

          <div className="stat-subtext">
            Requires attention
          </div>
        </div>


        <div className="stat-card">
          <div className="stat-label">
            MEDIUM RISK
          </div>

          <div className="stat-value">
            {mediumRisk}
          </div>

          <div className="stat-subtext">
            Monitor closely
          </div>
        </div>


        <div className="stat-card">
          <div className="stat-label">
            LOW RISK
          </div>

          <div className="stat-value">
            {lowRisk}
          </div>

          <div className="stat-subtext">
            No immediate concern
          </div>
        </div>

      </section>

      {/* Main content */}
      <section className="content-grid">

        {/* Transaction table */}
        <div className="panel">

          <div className="panel-header">
            <div>
              <h2>Recent Transactions</h2>
              <p>Latest payment risk assessments</p>
            </div>
          </div>

          {loading && (
            <div className="message">
              Loading transactions...
            </div>
          )}

          {error && (
            <div className="error">
              {error}
            </div>
          )}

          {!loading &&
            !error &&
            transactions.length === 0 && (
              <div className="message">
                No transactions found.
              </div>
            )}

          {!loading &&
            !error &&
            transactions.length > 0 && (

            <div className="table-wrapper">

              <table>

                <thead>
                  <tr>
                    <th>Transaction</th>
                    <th>Amount</th>
                    <th>Method</th>
                    <th>Risk Score</th>
                    <th>Status</th>
                    <th>Decision</th>
                  </tr>
                </thead>

                <tbody>

                  {transactions.map(
                    (transaction) => (

                    <tr
                      key={transaction.id}
                      className="clickable-row"
                      onClick={() =>
                        fetchTransactionDetails(transaction.id)
                      }
                    >

                      <td>
                        <strong>
                          #{transaction.id}
                        </strong>
                      </td>

                      <td>
                        ₹
                        {transaction.amount.toLocaleString(
                          "en-IN"
                        )}
                      </td>

                      <td>
                        {transaction.payment_method}
                      </td>

                      <td>
                        <div className="score-cell">
                          <strong>
                            {transaction.risk_score}
                          </strong>
                          <span>/100</span>
                        </div>
                      </td>

                      <td>
                        <span
                          className={`badge ${transaction.risk_level.toLowerCase()}`}
                        >
                          {transaction.risk_level}
                        </span>
                      </td>

                      <td>
                        {transaction.review_decision
                          ? transaction.review_decision
                          : "PENDING"}
                      </td>

                    </tr>
                  ))}
                </tbody>

              </table>

            </div>
          )}

        </div>


        {/* Investigation panel */}
        <div className="panel investigation-panel">

          {!selectedTransaction ? (

            <div className="empty-investigation">
              <h2>Risk Investigation</h2>
              <p>
                Select a transaction to investigate its
                risk profile.
              </p>
            </div>

          ) : (

            <div>

              <div className="investigation-header">

                <div>
                  <span className="small-label">
                    TRANSACTION
                  </span>

                  <h2>
                    #{selectedTransaction.id}
                  </h2>
                </div>

                <button
                  className="close-button"
                  onClick={() =>
                    setSelectedTransaction(null)
                  }
                >
                  ×
                </button>

              </div>


              {/* Risk score */}
              <div className="risk-section">

                <span className="small-label">
                  RISK SCORE
                </span>

                <div className="risk-score-row">

                  <div className="risk-score">
                    {selectedTransaction.risk_score}
                    <span>/100</span>
                  </div>

                  <span
                    className={`badge ${selectedTransaction.risk_level.toLowerCase()}`}
                  >
                    {selectedTransaction.risk_level}
                  </span>

                </div>

                <div className="risk-bar">

                  <div
                    className="risk-bar-fill"
                    style={{
                      width: `${selectedTransaction.risk_score}%`,
                      backgroundColor: selectedTransaction.risk_level === 'HIGH' ? '#d92d20' : selectedTransaction.risk_level === 'MEDIUM' ? '#f79009' : '#12b76a'
                    }}
                  />

                </div>

              </div>


              {/* Details */}
              <div className="details-grid">

                <div>
                  <span>Amount</span>
                  <strong>
                    ₹
                    {selectedTransaction.amount.toLocaleString(
                      "en-IN"
                    )}
                  </strong>
                </div>

                <div>
                  <span>Payment Method</span>
                  <strong>
                    {selectedTransaction.payment_method}
                  </strong>
                </div>

                <div>
                  <span>Account Age</span>
                  <strong>
                    {selectedTransaction.account_age_days}
                    {" "}days
                  </strong>
                </div>

                <div>
                  <span>Failed Attempts</span>
                  <strong>
                    {selectedTransaction.failed_attempts}
                  </strong>
                </div>

                <div>
                  <span>Device Changed</span>
                  <strong>
                    {selectedTransaction.device_changed
                      ? "YES"
                      : "NO"}
                  </strong>
                </div>

                <div>
                  <span>Location Changed</span>
                  <strong>
                    {selectedTransaction.location_changed
                      ? "YES"
                      : "NO"}
                  </strong>
                </div>

                <div>
                  <span>IP Risk</span>
                  <strong>
                    {selectedTransaction.ip_risk_score}
                  </strong>
                </div>

                <div>
                  <span>Previous Chargebacks</span>
                  <strong>
                    {selectedTransaction.previous_chargebacks}
                  </strong>
                </div>

              </div>


              {/* Recommendation */}
              <div className="risk-reasons">

                <span className="small-label">
                  RISK FACTORS
                </span>

                <div className="reason-list">

                  {selectedTransaction.risk_reasons?.map(
                    (reason, index) => (
                      <div
                        className="reason-item"
                        key={index}
                      >
                        <span className="reason-icon">
                          ✓
                        </span>

                        <span>
                          {reason}
                        </span>
                      </div>
                    )
                  )}

                </div>

              </div>

              <div className="ai-section">

                <span className="small-label">
                  AI INVESTIGATION
                </span>

                <button
                  className="ai-button"
                  onClick={() =>
                    runInvestigation(
                      selectedTransaction.id
                    )
                  }
                  disabled={investigating}
                >
                  {investigating
                    ? "Investigating..."
                    : "Run AI Investigation"}
                </button>

                {investigation && (
                  <div className="ai-result">
                    <pre>
                      {investigation}
                    </pre>
                  </div>
                )}

              </div>
              
              <div className="recommendation">

                <span className="small-label">
                  AI RECOMMENDATION
                </span>

                <strong>
                  {selectedTransaction.recommended_action}
                </strong>

              </div>

              <div className="review-section">

                <span className="small-label">
                  HUMAN REVIEW
                </span>

                <div className="review-buttons">

                  <button
                    className="review-button allow"
                    onClick={() =>
                      submitReview(
                        selectedTransaction.id,
                        "ALLOW"
                      )
                    }
                  >
                    ALLOW
                  </button>

                  <button
                    className="review-button review"
                    onClick={() =>
                      submitReview(
                        selectedTransaction.id,
                        "REVIEW"
                      )
                    }
                  >
                    REVIEW
                  </button>

                  <button
                    className="review-button block"
                    onClick={() =>
                      submitReview(
                        selectedTransaction.id,
                        "BLOCK"
                      )
                    }
                  >
                    BLOCK
                  </button>

                </div>

                {selectedTransaction.review_decision && (
                  <p className="review-status">
                    Decision:{" "}
                    <strong>
                      {selectedTransaction.review_decision}
                    </strong>
                  </p>
                )}

              </div>

            </div>
          )}

        </div>

      </section>

    </div>
  );
}

export default App;
