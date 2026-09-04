import { useMemo, useState } from "react";
import {
  AlertTriangle,
  Bell,
  CheckCircle2,
  ChevronRight,
  Clock3,
  ShieldAlert,
  XCircle,
} from "lucide-react";

function Alerts({
  transactions,
  onSelectTransaction,
}) {
  const [filter, setFilter] = useState("ALL");

  const alerts = useMemo(() => {
    return transactions
      .filter((transaction) => {
        const isHighRisk =
          transaction.risk_level === "HIGH";

        const isMediumRisk =
          transaction.risk_level === "MEDIUM";

        const isPending =
          !transaction.review_decision;

        /*
         * Only surface transactions that
         * need attention.
         */
        const needsAttention =
          isHighRisk ||
          (isMediumRisk && isPending);

        if (!needsAttention) {
          return false;
        }

        if (filter === "ALL") {
          return true;
        }

        if (filter === "UNRESOLVED") {
          return !transaction.review_decision;
        }

        if (filter === "HIGH") {
          return transaction.risk_level === "HIGH";
        }

        if (filter === "MEDIUM") {
          return transaction.risk_level === "MEDIUM";
        }

        return true;
      })
      .sort(
        (a, b) =>
          Number(b.risk_score) -
          Number(a.risk_score)
      );
  }, [transactions, filter]);


  const criticalCount = alerts.filter(
    (transaction) =>
      Number(transaction.risk_score) >= 90
  ).length;

  const highCount = alerts.filter(
    (transaction) =>
      transaction.risk_level === "HIGH"
  ).length;

  const mediumCount = alerts.filter(
    (transaction) =>
      transaction.risk_level === "MEDIUM"
  ).length;

  const unresolvedCount =
    transactions.filter(
      (transaction) =>
        !transaction.review_decision &&
        (
          transaction.risk_level === "HIGH" ||
          transaction.risk_level === "MEDIUM"
        )
    ).length;


  return (
    <div className="page-container">

      {/* HEADER */}

      <div className="page-top alerts-header">

        <div>

          <div className="eyebrow">
            RISK OPERATIONS
          </div>

          <h2>Alerts</h2>

          <p>
            Review high-priority transactions and
            unresolved risk events.
          </p>

        </div>

        <div className="alert-header-icon">
          <Bell size={22} />
          <span>{unresolvedCount}</span>
        </div>

      </div>


      {/* SUMMARY */}

      <section className="alert-summary-grid">

        <AlertSummary
          icon={<XCircle size={20} />}
          title="CRITICAL"
          value={criticalCount}
          description="Risk score ≥ 90"
          type="critical"
        />

        <AlertSummary
          icon={<ShieldAlert size={20} />}
          title="HIGH RISK"
          value={highCount}
          description="High-risk transactions"
          type="high"
        />

        <AlertSummary
          icon={<AlertTriangle size={20} />}
          title="MEDIUM"
          value={mediumCount}
          description="Requires monitoring"
          type="medium"
        />

        <AlertSummary
          icon={<Clock3 size={20} />}
          title="UNRESOLVED"
          value={unresolvedCount}
          description="Awaiting review"
          type="pending"
        />

      </section>


      {/* FILTERS */}

      <div className="alerts-toolbar">

        <div>

          <h3>
            Active Alerts
          </h3>

          <p>
            Prioritized by risk score
          </p>

        </div>

        <div className="alert-filters">

          <button
            className={
              filter === "ALL"
                ? "alert-filter active"
                : "alert-filter"
            }
            onClick={() =>
              setFilter("ALL")
            }
          >
            All
          </button>

          <button
            className={
              filter === "UNRESOLVED"
                ? "alert-filter active"
                : "alert-filter"
            }
            onClick={() =>
              setFilter("UNRESOLVED")
            }
          >
            Unresolved
          </button>

          <button
            className={
              filter === "HIGH"
                ? "alert-filter active"
                : "alert-filter"
            }
            onClick={() =>
              setFilter("HIGH")
            }
          >
            High
          </button>

          <button
            className={
              filter === "MEDIUM"
                ? "alert-filter active"
                : "alert-filter"
            }
            onClick={() =>
              setFilter("MEDIUM")
            }
          >
            Medium
          </button>

        </div>

      </div>


      {/* ALERT LIST */}

      <div className="alerts-list">

        {alerts.map((transaction) => {

          const isCritical =
            Number(transaction.risk_score) >= 90;

          return (
            <button
              key={transaction.id}
              className="alert-item"
              onClick={() =>
                onSelectTransaction(
                  transaction.id
                )
              }
            >

              <div
                className={`alert-severity ${
                  isCritical
                    ? "critical"
                    : transaction.risk_level.toLowerCase()
                }`}
              >
                {isCritical ? (
                  <XCircle size={21} />
                ) : transaction.risk_level ===
                  "HIGH" ? (
                  <ShieldAlert size={21} />
                ) : (
                  <AlertTriangle size={21} />
                )}
              </div>


              <div className="alert-content">

                <div className="alert-title-row">

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


                <div className="alert-description">

                  Rs.
                  {Number(
                    transaction.amount
                  ).toLocaleString("en-IN")}

                  <span className="separator">
                    •
                  </span>

                  {transaction.payment_method}

                  <span className="separator">
                    •
                  </span>

                  Risk Score{" "}
                  {transaction.risk_score}/100

                </div>


                <div className="alert-meta">

                  <span>
                    {transaction.review_decision
                      ? `Decision: ${transaction.review_decision}`
                      : "Awaiting human review"}
                  </span>

                  <span>
                    {getRelativeTime(
                      transaction.created_at
                    )}
                  </span>

                </div>

              </div>


              <ChevronRight
                size={17}
                className="alert-arrow"
              />

            </button>
          );
        })}


        {alerts.length === 0 && (

          <div className="empty-alerts">

            <div className="empty-alert-icon">
              <CheckCircle2 size={24} />
            </div>

            <h3>
              No active alerts
            </h3>

            <p>
              There are currently no transactions
              requiring attention.
            </p>

          </div>

        )}

      </div>

    </div>
  );
}


/* =========================================
   COMPONENT
========================================= */

function AlertSummary({
  icon,
  title,
  value,
  description,
  type,
}) {
  return (
    <div className="alert-summary-card">

      <div className={`alert-summary-icon ${type}`}>
        {icon}
      </div>

      <div>

        <span>
          {title}
        </span>

        <strong>
          {value}
        </strong>

        <small>
          {description}
        </small>

      </div>

    </div>
  );
}


/* =========================================
   RELATIVE TIME
========================================= */

function getRelativeTime(dateValue) {

  if (!dateValue) {
    return "—";
  }

  const date = new Date(dateValue);

  const diffMinutes = Math.floor(
    (Date.now() - date.getTime()) /
      60000
  );

  if (diffMinutes < 1) {
    return "Just now";
  }

  if (diffMinutes < 60) {
    return `${diffMinutes} min ago`;
  }

  const hours = Math.floor(
    diffMinutes / 60
  );

  if (hours < 24) {
    return `${hours} hr ago`;
  }

  return `${Math.floor(hours / 24)} d ago`;
}


export default Alerts;
