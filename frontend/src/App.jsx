import React, { useState, useEffect, useMemo } from "react";
import axios from "axios";
import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bell,
  BrainCircuit,
  CheckCircle2,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  CircleHelp,
  Copy,
  CreditCard,
  Database,
  Eye,
  FileText,
  LayoutDashboard,
  Menu,
  Moon,
  Plus,
  Search,
  Settings as SettingsIcon,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  Sun,
  X,
  XCircle,
} from "lucide-react";
import Transactions from "./pages/Transactions";
import RiskAnalysis from "./pages/RiskAnalysis";
import AIInvestigations from "./pages/AIInvestigations";
import Alerts from "./pages/Alerts";
import Reports from "./pages/Reports";
import Models from "./pages/Models";
import Settings from "./pages/Settings";
import NewTransaction from "./pages/NewTransaction";

import "./styles.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [transactions, setTransactions] = useState([]);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [investigation, setInvestigation] = useState("");
  const [loading, setLoading] = useState(true);
  const [investigating, setInvestigating] = useState(false);
  const [showNewTransaction, setShowNewTransaction] = useState(false);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [theme, setTheme] = useState("light");
  const [activePage, setActivePage] = useState("Dashboard");

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
      setInvestigation("");
      setActivePage((prev) => 
        (prev === "Transactions" || prev === "Alerts") ? "AI Investigations" : prev
      );
    } catch (err) {
      console.error(err);
      setError("Unable to load transaction details.");
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

  const submitReview = async (id, decision) => {
    try {
      await axios.post(
        `${API_URL}/api/v1/transactions/${id}/review`,
        null,
        {
          params: {
            decision,
          },
        }
      );

      await fetchTransactionDetails(id);
      await fetchTransactions();
    } catch (err) {
      console.error(err);
      setError(
        "Unable to save review decision."
      );
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const filteredTransactions = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return transactions;
    }

    return transactions.filter((transaction) =>
      [
        transaction.id,
        transaction.payment_method,
        transaction.risk_level,
        transaction.recommended_action,
        transaction.review_decision,
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase()
        .includes(query)
    );
  }, [transactions, search]);

  const highRisk = transactions.filter(
    (t) => t.risk_level === "HIGH"
  ).length;

  const mediumRisk = transactions.filter(
    (t) => t.risk_level === "MEDIUM"
  ).length;

  const lowRisk = transactions.filter(
    (t) => t.risk_level === "LOW"
  ).length;

  const total = transactions.length || 1;

  const highPercentage = (
    (highRisk / total) *
    100
  ).toFixed(1);

  const mediumPercentage = (
    (mediumRisk / total) *
    100
  ).toFixed(1);

  const lowPercentage = (
    (lowRisk / total) *
    100
  ).toFixed(1);

  return (
    <div className={`app ${theme}`}>

      {/* ================= SIDEBAR ================= */}

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-shield">
            <Shield size={24} />
          </div>

          <div>
            <div className="brand-name">
              Risk<span>Sentinel</span>
            </div>

            <div className="brand-subtitle">
              Payment Risk Intelligence
            </div>
          </div>
        </div>

        <nav className="sidebar-nav">

          <button
            className={`nav-item ${
              activePage === "Dashboard" ? "active" : ""
            }`}
            onClick={() => setActivePage("Dashboard")}
          >
            <LayoutDashboard size={18} />
            Dashboard
          </button>

          <button
            className={`nav-item ${
              activePage === "Transactions" ? "active" : ""
            }`}
            onClick={() => setActivePage("Transactions")}
          >
            <CreditCard size={18} />
            Transactions
          </button>

          <button
            className={`nav-item ${
              activePage === "Risk Analysis" ? "active" : ""
            }`}
            onClick={() => setActivePage("Risk Analysis")}
          >
            <ShieldAlert size={18} />
            Risk Analysis
          </button>

          <button
            className={`nav-item ${
              activePage === "AI Investigations" ? "active" : ""
            }`}
            onClick={() => setActivePage("AI Investigations")}
          >
            <BrainCircuit size={18} />
            AI Investigations
          </button>

          <button
            className={`nav-item ${
              activePage === "Reports" ? "active" : ""
            }`}
            onClick={() => setActivePage("Reports")}
          >
            <BarChart3 size={18} />
            Reports
          </button>

          <button
            className={`nav-item ${
              activePage === "Alerts" ? "active" : ""
            }`}
            onClick={() => setActivePage("Alerts")}
          >
            <Bell size={18} />
            Alerts

            {highRisk > 0 && (
              <span className="nav-badge">
                {highRisk}
              </span>
            )}
          </button>

          <button
            className={`nav-item ${
              activePage === "Models" ? "active" : ""
            }`}
            onClick={() => setActivePage("Models")}
          >
            <Activity size={18} />
            Models
          </button>

          <button
            className={`nav-item ${
              activePage === "Settings" ? "active" : ""
            }`}
            onClick={() => setActivePage("Settings")}
          >
            <SettingsIcon size={18} />
            Settings
          </button>

        </nav>

        <div className="sidebar-bottom">

          <div className="status-card">

            <div className="status-title">
              <span className="status-dot" />
              System Status
            </div>

            <div className="status-main">
              <CheckCircle2 size={14} />
              All systems operational
            </div>

            <div className="status-time">
              Live risk monitoring
            </div>

          </div>

          <div className="analyst-card">

            <div className="avatar">
              AD
            </div>

            <div className="analyst-info">
              <strong>Analyst</strong>
              <span>Risk Analyst</span>
            </div>

            <ChevronDown size={16} />

          </div>

          <div className="sidebar-footer">
            <div>© 2026 RiskSentinel</div>
            <div>All rights reserved.</div>
            <div>v1.0.0</div>
          </div>

        </div>

      </aside>


      {/* ================= MAIN ================= */}

      <main className="main">

        {/* Top bar */}

        <header className="topbar">

          <div className="page-heading">

            <div className="mobile-menu">
              <Menu size={20} />
            </div>

            <div>
              <h1>{activePage}</h1>

              <p>
                {activePage === "Dashboard"
                  ? "Real-time overview of payment risk and fraud detection"
                  : `Manage ${activePage.toLowerCase()}`
                }
              </p>
            </div>

          </div>

          <div className="topbar-actions">

            <div className="search-box">

              <Search size={17} />

              <input
                type="text"
                placeholder="Search transaction ID, amount, customer..."
                value={search}
                onChange={(e) =>
                  setSearch(e.target.value)
                }
              />

            </div>

            <div className="system-pill">

              <span className="status-dot" />

              <div>
                <strong>
                  System Operational
                </strong>

                <small>
                  All systems normal
                </small>
              </div>

            </div>

            <button className="icon-button">
              <Bell size={18} />

              {highRisk > 0 && (
                <span className="notification-dot">
                  {highRisk}
                </span>
              )}
            </button>

            <button
              className="icon-button"
              onClick={() =>
                setTheme(
                  theme === "light"
                    ? "dark"
                    : "light"
                )
              }
            >
              {theme === "light" ? (
                <Moon size={18} />
              ) : (
                <Sun size={18} />
              )}
            </button>

            <button
              className="new-transaction-button"
              onClick={fetchTransactions}
            >
              <Plus size={17} />
              Refresh Data
            </button>

            <button
              className="new-transaction-button"
              onClick={() => setShowNewTransaction(true)}
            >
              <Plus size={17} />
              New Transaction
            </button>

          </div>

        </header>


        {/* KPI CARDS */}

        {showNewTransaction ? (
          <NewTransaction
            onBack={() => setShowNewTransaction(false)}
          />
        ) : activePage === "Settings" ? (
          <Settings />
        ) : activePage === "Models" ? (
          <Models />
        ) : activePage === "Reports" ? (
          <Reports transactions={transactions} />
        ) : activePage === "Alerts" ? (
          <Alerts
            transactions={transactions}
            onSelectTransaction={fetchTransactionDetails}
          />
        ) : activePage === "AI Investigations" ? (
          <AIInvestigations
            transactions={transactions}
            onSelectTransaction={fetchTransactionDetails}
            selectedTransaction={selectedTransaction}
            investigation={investigation}
            investigating={investigating}
            onRunInvestigation={runInvestigation}
            onReview={submitReview}
          />
        ) : activePage === "Risk Analysis" ? (
          <RiskAnalysis transactions={transactions} />
        ) : activePage === "Transactions" ? (
          <Transactions
            transactions={transactions}
            onSelectTransaction={fetchTransactionDetails}
          />
        ) : activePage !== "Dashboard" ? (

          <div className="coming-soon-panel">

            <div className="coming-soon-icon">
              <Shield size={28} />
            </div>

            <h2>
              {activePage}
            </h2>

            <p>
              This module is part of the RiskSentinel
              roadmap and will be connected next.
            </p>

            <button
              className="back-dashboard-button"
              onClick={() =>
                setActivePage("Dashboard")
              }
            >
              Back to Dashboard
            </button>

          </div>

        ) : (
          <>
        <section
          className="kpi-grid"
          style={{ animation: "fadeSlideIn 0.35s ease" }}
        >

          <KpiCard
            title="TOTAL TRANSACTIONS"
            value={transactions.length}
            subtitle="Processed by RiskSentinel"
            icon={<Database size={21} />}
            type="total"
          />

          <KpiCard
            title="HIGH RISK"
            value={highRisk}
            subtitle="Requires attention"
            icon={<ShieldAlert size={21} />}
            type="high"
          />

          <KpiCard
            title="MEDIUM RISK"
            value={mediumRisk}
            subtitle="Monitor closely"
            icon={<Eye size={21} />}
            type="medium"
          />

          <KpiCard
            title="LOW RISK"
            value={lowRisk}
            subtitle="No immediate concern"
            icon={<ShieldCheck size={21} />}
            type="low"
          />

        </section>


        {/* MAIN GRID */}

        <section
          className="dashboard-grid"
          style={{ animation: "fadeSlideIn 0.45s ease" }}
        >

          {/* TRANSACTIONS */}

          <div className="panel transactions-panel">

            <div className="panel-header">

              <div>
                <h2>Recent Transactions</h2>

                <p>
                  Latest payment risk assessments
                </p>
              </div>

              <button className="view-all-button">
                View All
                <ChevronRight size={16} />
              </button>

            </div>


            {error && (
              <div className="error-banner">
                {error}
              </div>
            )}


            {loading ? (
              <div className="loading-state">
                Loading transactions...
              </div>
            ) : (

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
                      <th>Time</th>
                    </tr>
                  </thead>

                  <tbody>

                    {filteredTransactions.map(
                      (transaction) => {
                        return (
                      <tr
                        key={transaction.id}
                        className={`clickable-row ${
                          selectedTransaction?.id ===
                          transaction.id
                            ? "selected-row"
                            : ""
                        }`}
                        onClick={() =>
                          fetchTransactionDetails(
                            transaction.id
                          )
                        }
                      >

                        <td>

                          <div className="transaction-id">

                            <strong>
                              #{transaction.id}
                            </strong>

                            <Copy
                              size={13}
                              onClick={(e) => {
                                e.stopPropagation();

                                navigator.clipboard?.writeText(
                                  String(
                                    transaction.id
                                  )
                                );
                              }}
                            />

                          </div>

                        </td>


                        <td>
                          Rs.
                          {Number(
                            transaction.amount
                          ).toLocaleString(
                            "en-IN"
                          )}
                        </td>


                        <td>

                          <span
                            className={`method-badge ${transaction.payment_method.toLowerCase()}`}
                          >
                            {
                              transaction.payment_method
                            }
                          </span>

                        </td>


                        <td>

                          <div className="table-score">

                            <div>
                              <strong>
                                {
                                  transaction.risk_score
                                }
                              </strong>

                              <span>/100</span>
                            </div>

                            <div className="mini-score-bar">
                              <div
                                className={`mini-score-fill ${transaction.risk_level.toLowerCase()}`}
                                style={{
                                  width: `${transaction.risk_score}%`,
                                }}
                              />
                            </div>

                          </div>

                        </td>


                        <td>

                          <RiskBadge
                            level={
                              transaction.risk_level
                            }
                          />

                        </td>


                        <td>

                          <span
                            className={`decision-badge ${
                              transaction.review_decision
                                ? transaction.review_decision.toLowerCase()
                                : "pending"
                            }`}
                          >
                            {transaction.review_decision ||
                              "PENDING"}
                          </span>

                        </td>


                        <td className="time-cell">
                          {getRelativeTime(
                            transaction.created_at
                          )}
                        </td>

                      </tr>

                    );
                    })}

                  </tbody>

                </table>

              </div>

            )}


            <div className="table-footer">

              <span>
                Showing{" "}
                {filteredTransactions.length} of{" "}
                {transactions.length} transactions
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


          {/* INVESTIGATION */}

          <div className="panel investigation-panel">

            {!selectedTransaction ? (

              <div className="empty-investigation">

                <Shield size={36} />

                <h2>
                  Risk Investigation
                </h2>

                <p>
                  Select a transaction to view
                  its risk profile.
                </p>

              </div>

            ) : (

              <>

                <div className="investigation-title">

                  <div>
                    <h2>
                      Investigation: Transaction #
                      {selectedTransaction.id}
                    </h2>
                  </div>

                  <button
                    className="close-button"
                    onClick={() =>
                      setSelectedTransaction(null)
                    }
                  >
                    <X size={18} />
                  </button>

                </div>


                {/* SCORE */}

                <div className="investigation-card">

                  <div className="risk-heading">

                    <span>
                      RISK SCORE
                    </span>

                    <RiskBadge
                      level={
                        selectedTransaction.risk_level
                      }
                    />

                  </div>

                  <div className="big-score">

                    {selectedTransaction.risk_score}

                    <small>
                      /100
                    </small>

                  </div>

                  <div className="risk-gradient-bar">

                    <div
                      className="risk-marker"
                      style={{
                        left: `${selectedTransaction.risk_score}%`,
                      }}
                    />

                  </div>

                  <div className="risk-scale">
                    <span>0</span>
                    <span>25</span>
                    <span>50</span>
                    <span>75</span>
                    <span>100</span>
                  </div>

                </div>


                {/* DETAILS */}

                <div className="investigation-card">

                  <div className="section-heading">
                    Transaction Details
                  </div>

                  <div className="detail-grid">

                    <Detail
                      label="Amount"
                      value={`Rs.${Number(
                        selectedTransaction.amount
                      ).toLocaleString("en-IN")}`}
                    />

                    <Detail
                      label="Method"
                      value={
                        selectedTransaction.payment_method
                      }
                    />

                    <Detail
                      label="Account Age"
                      value={`${selectedTransaction.account_age_days} days`}
                    />

                    <Detail
                      label="Device Changed"
                      value={
                        selectedTransaction.device_changed
                          ? "Yes"
                          : "No"
                      }
                      danger={
                        selectedTransaction.device_changed
                      }
                    />

                    <Detail
                      label="Location Changed"
                      value={
                        selectedTransaction.location_changed
                          ? "Yes"
                          : "No"
                      }
                      danger={
                        selectedTransaction.location_changed
                      }
                    />

                    <Detail
                      label="IP Risk"
                      value={
                        selectedTransaction.ip_risk_score
                      }
                    />

                  </div>

                </div>


                {/* RISK FACTORS */}

                <div className="investigation-card">

                  <div className="section-heading">

                    Risk Factors

                    <span className="count-badge">
                      {
                        selectedTransaction
                          .risk_reasons?.length || 0
                      }
                    </span>

                  </div>

                  <div className="risk-factor-list">

                    {(
                      selectedTransaction
                        .risk_reasons || []
                    ).map(
                      (reason, index) => {
                        return (

                      <div
                        key={index}
                        className="risk-factor"
                      >

                        <AlertTriangle
                          size={15}
                        />

                        <span>
                          {reason}
                        </span>

                      </div>

                    );
                    })}

                  </div>

                </div>


                {/* AI INVESTIGATION */}

                <div className="investigation-card">

                  <div className="section-heading ai-title">

                    AI Investigation

                    <span className="beta-badge">
                      BETA
                    </span>

                  </div>

                  <button
                    className="ai-button"
                    onClick={() =>
                      runInvestigation(
                        selectedTransaction.id
                      )
                    }
                    disabled={investigating}
                  >
                    {investigating ? (
                      <>
                        <span className="ai-spinner" />
                        Investigating...
                      </>
                    ) : (
                      <>
                        <Sparkles size={17} />
                        Run AI Investigation
                      </>
                    )}
                  </button>

                  {investigation && (

                    <div className="ai-result">
                      <pre>
                        {investigation}
                      </pre>
                    </div>

                  )}

                </div>


                {/* HUMAN REVIEW */}

                <div className="investigation-card">

                  <div className="section-heading">
                    Human Review
                  </div>

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
                      <CheckCircle2 size={16} />
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
                      <Eye size={16} />
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
                      <XCircle size={16} />
                      BLOCK
                    </button>

                  </div>


                  <div className="decision-footer">

                    <div>
                      <strong>
                        Decision:{" "}
                        {selectedTransaction.review_decision ||
                          "PENDING"}
                      </strong>

                      <span>
                        {selectedTransaction.review_decision
                          ? "Decision recorded"
                          : "No decision taken yet"}
                      </span>
                    </div>

                    <FileText size={17} />

                  </div>

                </div>

              </>

            )}

          </div>

        </section>


        {/* ANALYTICS */}

        <section
          className="analytics-grid"
          style={{ animation: "fadeSlideIn 0.55s ease" }}
        >

          <div className="panel analytics-card">

            <div className="panel-header compact">

              <div>
                <h3>
                  Risk Level Distribution
                </h3>
              </div>

            </div>

            <div className="distribution">

              <div
                className="donut"
                style={{
                  background: `conic-gradient(
                    #16a34a 0 ${lowPercentage}%,
                    #f59e0b ${lowPercentage}% ${(
                      Number(lowPercentage) +
                      Number(mediumPercentage)
                    ).toFixed(1)}%,
                    #ef4444 ${(
                      Number(lowPercentage) +
                      Number(mediumPercentage)
                    ).toFixed(1)}% 100%
                  )`,
                }}
              >
                <div className="donut-center">
                  {transactions.length}
                  <span>Total</span>
                </div>
              </div>

              <div className="distribution-list">

                <DistributionItem
                  label="High Risk"
                  value={highRisk}
                  percentage={highPercentage}
                  type="high"
                />

                <DistributionItem
                  label="Medium Risk"
                  value={mediumRisk}
                  percentage={mediumPercentage}
                  type="medium"
                />

                <DistributionItem
                  label="Low Risk"
                  value={lowRisk}
                  percentage={lowPercentage}
                  type="low"
                />

              </div>

            </div>

          </div>


          <div className="panel analytics-card">

            <div className="panel-header compact">

              <div>
                <h3>
                  Model Performance
                </h3>

                <p>
                  Test set metrics
                </p>
              </div>

              <BarChart3 size={18} />

            </div>

            <div className="metrics-grid">

              <Metric
                label="Precision"
                value="—"
              />

              <Metric
                label="Recall"
                value="—"
              />

              <Metric
                label="F1 Score"
                value="—"
              />

              <Metric
                label="ROC-AUC"
                value="—"
              />

            </div>

            <div className="metrics-note">
              Connect your final evaluation results
              from <code>final_evaluation.py</code>
              here.
            </div>

          </div>

        </section>
        </>
        )}

      </main>

    </div>
  );
}


/* ==================================================
   COMPONENTS
================================================== */

function KpiCard({
  title,
  value,
  subtitle,
  icon,
  type,
}) {
  return (
    <div className={`kpi-card ${type}`}>

      <div className={`kpi-icon ${type}`}>
        {icon}
      </div>

      <div className="kpi-content">

        <span className="kpi-title">
          {title}
        </span>

        <strong className="kpi-value">
          {value.toLocaleString()}
        </strong>

        <span className="kpi-subtitle">
          {subtitle}
        </span>

      </div>

    </div>
  );
}


function RiskBadge({ level }) {
  return (
    <span
      className={`risk-badge ${level.toLowerCase()}`}
    >
      {level}
    </span>
  );
}


function Detail({
  label,
  value,
  danger,
}) {
  return (
    <div className="detail-item">

      <span>{label}</span>

      <strong className={danger ? "danger-text" : ""}>
        {value}
      </strong>

    </div>
  );
}


function DistributionItem({
  label,
  value,
  percentage,
  type,
}) {
  return (
    <div className="distribution-item">

      <div className="distribution-label">

        <span className={`legend-dot ${type}`} />

        <span>{label}</span>

      </div>

      <strong>
        {value}
      </strong>

      <span>
        {percentage}%
      </span>

    </div>
  );
}


function Metric({
  label,
  value,
}) {
  return (
    <div className="metric">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>
  );
}


function getRelativeTime(dateValue) {
  if (!dateValue) {
    return "—";
  }

  const date = new Date(dateValue);
  const diff =
    Math.floor(
      (Date.now() - date.getTime()) / 60000
    );

  if (diff < 1) {
    return "Just now";
  }

  if (diff < 60) {
    return `${diff} min ago`;
  }

  const hours = Math.floor(diff / 60);

  if (hours < 24) {
    return `${hours} hr ago`;
  }

  return `${Math.floor(hours / 24)} d ago`;
}


export default App;
