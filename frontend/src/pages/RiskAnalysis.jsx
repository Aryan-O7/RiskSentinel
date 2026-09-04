import { useMemo } from "react";
import {
  AlertTriangle,
  BarChart3,
  ShieldAlert,
  ShieldCheck,
  Activity,
} from "lucide-react";

function RiskAnalysis({ transactions }) {
  const stats = useMemo(() => {
    const total = transactions.length;

    const high = transactions.filter(
      (t) => t.risk_level === "HIGH"
    ).length;

    const medium = transactions.filter(
      (t) => t.risk_level === "MEDIUM"
    ).length;

    const low = transactions.filter(
      (t) => t.risk_level === "LOW"
    ).length;

    const scores = transactions.map(
      (t) => Number(t.risk_score) || 0
    );

    const averageScore =
      scores.length > 0
        ? scores.reduce(
            (sum, score) => sum + score,
            0
          ) / scores.length
        : 0;

    const highestScore =
      scores.length > 0
        ? Math.max(...scores)
        : 0;

    return {
      total,
      high,
      medium,
      low,
      averageScore,
      highestScore,
    };
  }, [transactions]);

  const total = stats.total || 1;

  const highPercent =
    (stats.high / total) * 100;

  const mediumPercent =
    (stats.medium / total) * 100;

  const lowPercent =
    (stats.low / total) * 100;

  const highRiskTransactions =
    transactions
      .filter((t) => t.risk_level === "HIGH")
      .sort(
        (a, b) =>
          b.risk_score - a.risk_score
      )
      .slice(0, 8);

  return (
    <div className="page-container">

      {/* Header */}

      <div className="page-top">

        <div>
          <div className="eyebrow">
            RISK INTELLIGENCE
          </div>

          <h2>Risk Analysis</h2>

          <p>
            Monitor transaction risk patterns and
            identify high-risk activity.
          </p>
        </div>

      </div>


      {/* Summary */}

      <section className="risk-summary-grid">

        <AnalysisCard
          title="TOTAL TRANSACTIONS"
          value={stats.total}
          subtitle="Analyzed transactions"
          icon={<Activity size={19} />}
          type="blue"
        />

        <AnalysisCard
          title="HIGH RISK"
          value={stats.high}
          subtitle="Requires attention"
          icon={<ShieldAlert size={19} />}
          type="red"
        />

        <AnalysisCard
          title="MEDIUM RISK"
          value={stats.medium}
          subtitle="Monitor closely"
          icon={<AlertTriangle size={19} />}
          type="orange"
        />

        <AnalysisCard
          title="LOW RISK"
          value={stats.low}
          subtitle="Low immediate concern"
          icon={<ShieldCheck size={19} />}
          type="green"
        />

      </section>


      {/* Overview */}

      <section className="analysis-grid">

        <div className="panel analysis-panel">

          <div className="panel-header">

            <div>
              <h3>Risk Distribution</h3>

              <p>
                Distribution of assessed transactions
              </p>
            </div>

            <BarChart3 size={18} />

          </div>


          <div className="risk-distribution">

            <div
              className="large-donut"
              style={{
                background: `conic-gradient(
                  #16a34a 0 ${lowPercent}%,
                  #f59e0b ${lowPercent}% ${
                    lowPercent + mediumPercent
                  }%,
                  #ef4444 ${
                    lowPercent + mediumPercent
                  }% 100%
                )`,
              }}
            >

              <div className="large-donut-center">

                <strong>
                  {stats.total}
                </strong>

                <span>
                  Total
                </span>

              </div>

            </div>


            <div className="distribution-details">

              <DistributionRow
                label="High Risk"
                value={stats.high}
                percentage={highPercent}
                type="high"
              />

              <DistributionRow
                label="Medium Risk"
                value={stats.medium}
                percentage={mediumPercent}
                type="medium"
              />

              <DistributionRow
                label="Low Risk"
                value={stats.low}
                percentage={lowPercent}
                type="low"
              />

            </div>

          </div>

        </div>


        {/* Score statistics */}

        <div className="panel analysis-panel">

          <div className="panel-header">

            <div>
              <h3>Risk Score Overview</h3>

              <p>
                Current transaction risk statistics
              </p>
            </div>

          </div>


          <div className="score-overview">

            <div className="score-stat">

              <span>
                Average Risk Score
              </span>

              <strong>
                {stats.averageScore.toFixed(1)}
              </strong>

              <div className="overview-bar">
                <div
                  style={{
                    width: `${stats.averageScore}%`,
                  }}
                />
              </div>

            </div>


            <div className="score-stat">

              <span>
                Highest Risk Score
              </span>

              <strong className="danger-number">
                {stats.highestScore}
              </strong>

              <div className="overview-bar danger">
                <div
                  style={{
                    width: `${stats.highestScore}%`,
                  }}
                />
              </div>

            </div>


            <div className="score-stat">

              <span>
                High-Risk Rate
              </span>

              <strong>
                {highPercent.toFixed(1)}%
              </strong>

              <div className="overview-bar warning">
                <div
                  style={{
                    width: `${highPercent}%`,
                  }}
                />
              </div>

            </div>

          </div>

        </div>

      </section>


      {/* High risk transactions */}

      <section className="panel high-risk-panel">

        <div className="panel-header">

          <div>
            <h3>
              Highest-Risk Transactions
            </h3>

            <p>
              Transactions currently requiring the
              most attention
            </p>
          </div>

          <span className="risk-count">
            {highRiskTransactions.length}
          </span>

        </div>


        <div className="table-wrapper">

          <table>

            <thead>

              <tr>
                <th>Transaction</th>
                <th>Amount</th>
                <th>Method</th>
                <th>Risk Score</th>
                <th>Level</th>
                <th>Decision</th>
              </tr>

            </thead>

            <tbody>

              {highRiskTransactions.map(
                (transaction) => {
                  return (
                <tr key={transaction.id}>

                  <td>
                    <strong>
                      #{transaction.id}
                    </strong>
                  </td>

                  <td>
                    Rs.
                    {Number(
                      transaction.amount
                    ).toLocaleString("en-IN")}
                  </td>

                  <td>
                    {transaction.payment_method}
                  </td>

                  <td>

                    <div className="analysis-score">

                      <strong>
                        {transaction.risk_score}
                      </strong>

                      <div className="mini-score-bar">
                        <div
                          className="mini-score-fill high"
                          style={{
                            width: `${transaction.risk_score}%`,
                          }}
                        />
                      </div>

                    </div>

                  </td>

                  <td>
                    <span className="risk-badge high">
                      HIGH
                    </span>
                  </td>

                  <td>
                    <span className="decision-badge">
                      {transaction.review_decision ||
                        "PENDING"}
                    </span>
                  </td>

                </tr>
                );
              })}

            </tbody>

          </table>

        </div>


        {highRiskTransactions.length === 0 && (
          <div className="empty-page">
            No high-risk transactions found.
          </div>
        )}

      </section>


      {/* Model section */}

      <section className="panel model-placeholder">

        <div className="model-placeholder-icon">
          <BarChart3 size={22} />
        </div>

        <div>

          <h3>
            Model Performance
          </h3>

          <p>
            Precision, recall, F1 score, ROC-AUC and
            threshold analysis will be connected here
            from the final evaluation pipeline.
          </p>

        </div>

      </section>

    </div>
  );
}


/* =========================================
   COMPONENTS
========================================= */

function AnalysisCard({
  title,
  value,
  subtitle,
  icon,
  type,
}) {
  return (
    <div className="analysis-card">

      <div className={`analysis-icon ${type}`}>
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
          {subtitle}
        </small>

      </div>

    </div>
  );
}


function DistributionRow({
  label,
  value,
  percentage,
  type,
}) {
  return (
    <div className="distribution-row">

      <div className="distribution-row-label">

        <span className={`legend-dot ${type}`} />

        <span>
          {label}
        </span>

      </div>

      <strong>
        {value}
      </strong>

      <span>
        {percentage.toFixed(1)}%
      </span>

    </div>
  );
}

export default RiskAnalysis;
