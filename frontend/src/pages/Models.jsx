import { useEffect, useState } from "react";
import axios from "axios";
import {
  Activity,
  BarChart3,
  BrainCircuit,
  CheckCircle2,
  GitCompare,
  Target,
  TrendingUp,
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000";

function Models() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadMetrics = async () => {
      try {
        const response = await axios.get(
          `${API_URL}/api/v1/reports/model-performance`
        );

        setMetrics(response.data.data);
      } catch (err) {
        console.error(err);
        setError("Unable to load model metrics.");
      } finally {
        setLoading(false);
      }
    };

    loadMetrics();
  }, []);

  const metric = (value) => {
    if (loading) return "...";
    if (!metrics) return "—";

    return `${(value * 100).toFixed(1)}%`;
  };

  return (
    <div className="page-container">

      {/* HEADER */}

      <div className="page-top">

        <div>
          <div className="eyebrow">
            MACHINE LEARNING
          </div>

          <h2>Models</h2>

          <p>
            Monitor model performance and the
            decision engine powering RiskSentinel.
          </p>
        </div>

        <div className="model-status-pill">
          <CheckCircle2 size={15} />
          Production Candidate
        </div>

      </div>


      {error && (
        <div className="error-banner">
          {error}
        </div>
      )}


      {/* ACTIVE MODEL */}

      <section className="panel active-model-panel">

        <div className="panel-header">

          <div>
            <h3>Active Risk Model</h3>

            <p>
              Model currently powering transaction
              risk scoring
            </p>
          </div>

          <BrainCircuit size={20} />

        </div>


        <div className="active-model-content">

          <div className="model-identity">

            <div className="model-icon">
              <BrainCircuit size={24} />
            </div>

            <div>
              <h3>
                {metrics?.model ||
                  "XGBoost Risk Model"}
              </h3>

              <span>
                Binary payment-risk classifier
              </span>
            </div>

          </div>


          <div className="model-meta">

            <div>
              <span>
                Test Samples
              </span>

              <strong>
                {loading
                  ? "..."
                  : metrics
                    ? metrics.test_samples.toLocaleString()
                    : "—"}
              </strong>
            </div>


            <div>
              <span>
                Decision Threshold
              </span>

              <strong>
                {loading
                  ? "..."
                  : metrics
                    ? `${(
                        metrics.threshold * 100
                      ).toFixed(0)}%`
                    : "—"}
              </strong>
            </div>


            <div>
              <span>
                Status
              </span>

              <strong className="green-text">
                Active
              </strong>
            </div>

          </div>

        </div>

      </section>


      {/* PERFORMANCE */}

      <section className="model-metrics-grid">

        <ModelMetric
          label="PRECISION"
          value={
            metrics
              ? metric(metrics.precision)
              : loading
                ? "..."
                : "—"
          }
          description="Correctness of risk flags"
          icon={<Target size={18} />}
          type="blue"
        />

        <ModelMetric
          label="RECALL"
          value={
            metrics
              ? metric(metrics.recall)
              : loading
                ? "..."
                : "—"
          }
          description="Risky transactions detected"
          icon={<Activity size={18} />}
          type="purple"
        />

        <ModelMetric
          label="F1 SCORE"
          value={
            metrics
              ? metric(metrics.f1_score)
              : loading
                ? "..."
                : "—"
          }
          description="Precision / recall balance"
          icon={<BarChart3 size={18} />}
          type="green"
        />

        <ModelMetric
          label="ROC-AUC"
          value={
            metrics
              ? metric(metrics.roc_auc)
              : loading
                ? "..."
                : "—"
          }
          description="Overall ranking performance"
          icon={<TrendingUp size={18} />}
          type="orange"
        />

      </section>


      {/* MODEL COMPARISON */}

      <section className="panel model-comparison-panel">

        <div className="panel-header">

          <div>
            <h3>Model Comparison</h3>

            <p>
              Baseline versus selected model
            </p>
          </div>

          <GitCompare size={19} />

        </div>


        <div className="comparison-table">

          <div className="comparison-row comparison-header">
            <span>Model</span>
            <span>Precision</span>
            <span>Recall</span>
            <span>F1</span>
            <span>Status</span>
          </div>


          <div className="comparison-row">

            <span>
              Logistic Regression
            </span>

            <span>
              Baseline
            </span>

            <span>
              Baseline
            </span>

            <span>
              Baseline
            </span>

            <span className="baseline-badge">
              Baseline
            </span>

          </div>


          <div className="comparison-row selected-model-row">

            <div className="selected-model-name">

              <BrainCircuit size={15} />

              <strong>
                XGBoost
              </strong>

            </div>

            <span>
              {metrics
                ? metric(metrics.precision)
                : "—"}
            </span>

            <span>
              {metrics
                ? metric(metrics.recall)
                : "—"}
            </span>

            <span>
              {metrics
                ? metric(metrics.f1_score)
                : "—"}
            </span>

            <span className="active-model-badge">
              Selected
            </span>

          </div>

        </div>

      </section>


      {/* CONFUSION MATRIX */}

      <section className="panel confusion-panel">

        <div className="panel-header">

          <div>
            <h3>Classification Results</h3>

            <p>
              Final held-out test set
            </p>
          </div>

          <BarChart3 size={19} />

        </div>


        <div className="confusion-grid">

          <ConfusionBox
            label="True Negatives"
            value={
              metrics
                ? metrics.true_negatives
                : "—"
            }
          />

          <ConfusionBox
            label="False Positives"
            value={
              metrics
                ? metrics.false_positives
                : "—"
            }
            danger
          />

          <ConfusionBox
            label="False Negatives"
            value={
              metrics
                ? metrics.false_negatives
                : "—"
            }
            danger
          />

          <ConfusionBox
            label="True Positives"
            value={
              metrics
                ? metrics.true_positives
                : "—"
            }
          />

        </div>

      </section>


      {/* BUSINESS COST */}

      <section className="model-bottom-grid">

        <div className="panel model-cost-panel">

          <div className="panel-header">

            <div>
              <h3>
                False-Positive Cost
              </h3>

              <p>
                Estimated legitimate-customer impact
              </p>
            </div>

          </div>


          <div className="cost-value">

            Rs.
            {metrics
              ? metrics.false_positive_cost.toLocaleString(
                  "en-IN"
                )
              : "—"}

          </div>

          <span className="cost-description">
            Estimated cost from false-positive
            predictions.
          </span>

        </div>


        <div className="panel model-cost-panel">

          <div className="panel-header">

            <div>
              <h3>
                False-Negative Cost
              </h3>

              <p>
                Estimated missed-risk impact
              </p>
            </div>

          </div>


          <div className="cost-value danger-cost">

            Rs.
            {metrics
              ? metrics.false_negative_cost.toLocaleString(
                  "en-IN"
                )
              : "—"}

          </div>

          <span className="cost-description">
            Estimated cost from risky transactions
            missed by the model.
          </span>

        </div>

      </section>


      {/* FOOTER NOTE */}

      <div className="model-note">

        <BrainCircuit size={15} />

        <span>
          RiskSentinel uses XGBoost for risk
          scoring and a separate AI investigation
          layer for explanation and analysis.
        </span>

      </div>

    </div>
  );
}


/* =========================================
   COMPONENTS
========================================= */

function ModelMetric({
  label,
  value,
  description,
  icon,
  type,
}) {
  return (
    <div className="model-metric">

      <div className={`model-metric-icon ${type}`}>
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


function ConfusionBox({
  label,
  value,
  danger = false,
}) {
  return (
    <div className="confusion-box">

      <span>
        {label}
      </span>

      <strong
        className={
          danger
            ? "danger-number"
            : ""
        }
      >
        {value}
      </strong>

    </div>
  );
}

export default Models;
