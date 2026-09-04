import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import {
  BarChart3,
  Download,
  FileText,
  ShieldAlert,
  ShieldCheck,
  TrendingUp,
  AlertTriangle,
  Activity,
} from "lucide-react";

function Reports({ transactions }) {
  const [metrics, setMetrics] = useState(null);
  const [metricsLoading, setMetricsLoading] = useState(true);
  const [metricsError, setMetricsError] = useState("");

  useEffect(() => {
    const loadMetrics = async () => {
      try {
        setMetricsLoading(true);
        const response = await axios.get(
          "http://127.0.0.1:8000/api/v1/reports/model-performance"
        );
        setMetrics(response.data.data);
        setMetricsError("");
      } catch (error) {
        console.error(error);
        setMetricsError("Unable to load model metrics.");
      } finally {
        setMetricsLoading(false);
      }
    };
    loadMetrics();
  }, []);

  const report = useMemo(() => {

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

    const reviewed = transactions.filter(
      (t) => t.review_decision
    ).length;

    const pending = transactions.filter(
      (t) => !t.review_decision
    ).length;

    const blocked = transactions.filter(
      (t) => t.review_decision === "BLOCK"
    ).length;

    const allowed = transactions.filter(
      (t) => t.review_decision === "ALLOW"
    ).length;

    const manuallyReviewed = transactions.filter(
      (t) => t.review_decision === "REVIEW"
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

    return {
      total,
      high,
      medium,
      low,
      reviewed,
      pending,
      blocked,
      allowed,
      manuallyReviewed,
      averageScore,
    };

  }, [transactions]);


  const highRate =
    report.total > 0
      ? (
          (report.high / report.total) *
          100
        ).toFixed(1)
      : "0.0";


  const reviewRate =
    report.total > 0
      ? (
          (report.reviewed / report.total) *
          100
        ).toFixed(1)
      : "0.0";


  return (
    <div className="page-container">

      {/* =====================================
          HEADER
      ====================================== */}

      <div className="page-top reports-header">

        <div>

          <div className="eyebrow">
            RISK INTELLIGENCE
          </div>

          <h2>Reports</h2>

          <p>
            Performance, risk distribution and
            operational impact of RiskSentinel.
          </p>

        </div>

        <button
          className="report-export-button"
          onClick={() => {
            window.print();
          }}
        >
          <Download size={16} />
          Export Report
        </button>

      </div>


      {/* =====================================
          MODEL PERFORMANCE
      ====================================== */}

      <section className="report-section">

        <div className="report-section-heading">

          <div>
            <h3>
              Model Performance
            </h3>

            <p>
              Final held-out test set metrics
            </p>
          </div>

          <BarChart3 size={19} />

        </div>


        <div className="report-metrics-grid">

          <ReportMetric
            label="PRECISION"
            value={
              metricsLoading
                ? "..."
                : metrics
                  ? `${(
                      metrics.precision * 100
                    ).toFixed(1)}%`
                  : "—"
            }
            description="Flagged transactions that were actually risky"
            type="blue"
          />

          <ReportMetric
            label="RECALL"
            value={
              metricsLoading
                ? "..."
                : metrics
                  ? `${(
                      metrics.recall * 100
                    ).toFixed(1)}%`
                  : "—"
            }
            description="Risky transactions successfully detected"
            type="purple"
          />

          <ReportMetric
            label="F1 SCORE"
            value={
              metricsLoading
                ? "..."
                : metrics
                  ? `${(
                      metrics.f1_score * 100
                    ).toFixed(1)}%`
                  : "—"
            }
            description="Balance between precision and recall"
            type="green"
          />

          <ReportMetric
            label="ROC-AUC"
            value={
              metricsLoading
                ? "..."
                : metrics
                  ? `${(
                      metrics.roc_auc * 100
                    ).toFixed(1)}%`
                  : "—"
            }
            description="Overall ranking performance"
            type="orange"
          />

        </div>

        <div className="report-info">

          <Activity size={15} />

          <span>
            Metrics generated from the latest
            held-out model evaluation.
            Model:{" "}
            <strong>
              {metrics?.model || "Loading..."}
            </strong>
          </span>

        </div>

      </section>


      {/* =====================================
          TRANSACTION OVERVIEW
      ====================================== */}

      <section className="report-section">

        <div className="report-section-heading">

          <div>

            <h3>
              Transaction Overview
            </h3>

            <p>
              Current transaction distribution
            </p>

          </div>

        </div>


        <div className="report-overview-grid">

          <OverviewCard
            icon={<FileText size={18} />}
            label="TOTAL"
            value={report.total}
            description="All assessed transactions"
            type="blue"
          />

          <OverviewCard
            icon={<ShieldAlert size={18} />}
            label="HIGH RISK"
            value={report.high}
            description={`${highRate}% of transactions`}
            type="red"
          />

          <OverviewCard
            icon={<AlertTriangle size={18} />}
            label="MEDIUM RISK"
            value={report.medium}
            description="Requires monitoring"
            type="orange"
          />

          <OverviewCard
            icon={<ShieldCheck size={18} />}
            label="LOW RISK"
            value={report.low}
            description="Low immediate concern"
            type="green"
          />

        </div>

      </section>


      {/* =====================================
          BUSINESS IMPACT
      ====================================== */}

      <section className="report-grid">

        <div className="report-section">

          <div className="report-section-heading">

            <div>

              <h3>
                Review Activity
              </h3>

              <p>
                Human review decisions
              </p>

            </div>

          </div>


          <div className="review-stats">

            <ReviewStat
              label="Reviewed"
              value={report.reviewed}
            />

            <ReviewStat
              label="Pending"
              value={report.pending}
            />

            <ReviewStat
              label="Allowed"
              value={report.allowed}
            />

            <ReviewStat
              label="Blocked"
              value={report.blocked}
            />

          </div>


          <div className="review-progress">

            <div className="review-progress-header">
              <span>
                Review Completion
              </span>

              <strong>
                {reviewRate}%
              </strong>
            </div>

            <div className="progress-track">

              <div
                style={{
                  width: `${reviewRate}%`,
                }}
              />

            </div>

          </div>

        </div>


        <div className="report-section">

          <div className="report-section-heading">

            <div>

              <h3>
                Risk Score Summary
              </h3>

              <p>
                Current operational statistics
              </p>

            </div>

            <TrendingUp size={19} />

          </div>


          <div className="risk-report-stat">

            <span>
              Average Risk Score
            </span>

            <strong>
              {report.averageScore.toFixed(1)}
              <small>/100</small>
            </strong>

          </div>


          <div className="risk-report-stat">

            <span>
              High-Risk Rate
            </span>

            <strong>
              {highRate}%
            </strong>

          </div>


          <div className="risk-report-stat">

            <span>
              Manual Reviews
            </span>

            <strong>
              {report.manuallyReviewed}
            </strong>

          </div>

        </div>

      </section>


      {/* =====================================
          BUSINESS COST
      ====================================== */}

      <section className="report-section">

        <div className="report-section-heading">

          <div>

            <h3>
              Business Impact
            </h3>

            <p>
              Error-cost framework used for prototype
              evaluation
            </p>

          </div>

        </div>


        <div className="business-impact-grid">

          <BusinessMetric
            label="False Positives"
            value={
              metrics
                ? metrics.false_positives.toLocaleString()
                : "—"
            }
            description="Legitimate transactions incorrectly flagged"
          />

          <BusinessMetric
            label="False Negatives"
            value={
              metrics
                ? metrics.false_negatives.toLocaleString()
                : "—"
            }
            description="Risky transactions missed by the model"
          />

          <BusinessMetric
            label="FP Cost"
            value={
              metrics
                ? `Rs.${metrics.false_positive_cost.toLocaleString(
                    "en-IN"
                  )}`
                : "—"
            }
            description="Estimated cost of false positives"
          />

          <BusinessMetric
            label="FN Cost"
            value={
              metrics
                ? `Rs.${metrics.false_negative_cost.toLocaleString(
                    "en-IN"
                  )}`
                : "—"
            }
            description="Estimated cost of false negatives"
          />

        </div>

        <div className="cost-note">

          Prototype cost assumptions are currently
          maintained in the ML evaluation pipeline.

        </div>

      </section>


      {/* =====================================
          THRESHOLD
      ====================================== */}

      <section className="report-section threshold-report">

        <div className="report-section-heading">

          <div>

            <h3>
              Risk Decision Threshold
            </h3>

            <p>
              Operating point selected from threshold
              analysis
            </p>

          </div>

          <ShieldAlert size={19} />

        </div>


        <div className="threshold-display">

          <div>

            <span>
              SELECTED THRESHOLD
            </span>

            <strong>
              {metrics
                ? `${(
                    metrics.threshold * 100
                  ).toFixed(0)}%`
                : "—"}
            </strong>

          </div>

          <div className="threshold-explanation">

            <p>
              The final threshold will be populated
              from the validated threshold-analysis
              results.
            </p>

          </div>

        </div>

      </section>


      {/* =====================================
          REPORT FOOTER
      ====================================== */}

      <div className="report-footer">

        <FileText size={15} />

        <span>
          RiskSentinel automated report ·
          Generated from current application data
        </span>

      </div>

    </div>
  );
}


/* =========================================
   COMPONENTS
========================================= */

function ReportMetric({
  label,
  value,
  description,
  type,
}) {
  return (
    <div className="report-metric">

      <div className={`report-metric-icon ${type}`}>
        <BarChart3 size={17} />
      </div>

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

      <small>
        {description}
      </small>

    </div>
  );
}


function OverviewCard({
  icon,
  label,
  value,
  description,
  type,
}) {
  return (
    <div className="overview-card">

      <div className={`overview-icon ${type}`}>
        {icon}
      </div>

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

      <small>
        {description}
      </small>

    </div>
  );
}


function ReviewStat({
  label,
  value,
}) {
  return (
    <div className="review-stat">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>
  );
}


function BusinessMetric({
  label,
  value,
  description,
}) {
  return (
    <div className="business-metric">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

      <small>
        {description}
      </small>

    </div>
  );
}

export default Reports;
