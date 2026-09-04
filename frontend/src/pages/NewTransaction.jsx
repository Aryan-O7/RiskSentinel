import { useState } from "react";
import axios from "axios";
import {
  ArrowLeft,
  CheckCircle2,
  ShieldAlert,
  Sparkles,
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000";

function NewTransaction({ onBack }) {

  const [form, setForm] = useState({
    customer_id: "",
    name: "",
    email: "",
    account_age_days: 30,

    amount: "",
    transactions_last_24h: 1,
    avg_transaction_amount: "",
    failed_attempts: 0,
    device_changed: 0,
    location_changed: 0,
    ip_risk_score: 0.1,
    previous_chargebacks: 0,
    transaction_hour: 12,
    payment_method: "UPI",
  });

  const [submitting, setSubmitting] =
    useState(false);

  const [result, setResult] =
    useState(null);

  const [error, setError] =
    useState("");

  const updateField = (field, value) => {
    setForm((previous) => ({
      ...previous,
      [field]: value,
    }));
  };

  const submitTransaction = async (e) => {

    e.preventDefault();

    setSubmitting(true);
    setError("");
    setResult(null);

    try {

      const payload = {

        customer: {
          customer_id:
            form.customer_id,

          name:
            form.name,

          email:
            form.email || null,

          account_age_days:
            Number(form.account_age_days),
        },

        amount:
          Number(form.amount),

        transactions_last_24h:
          Number(
            form.transactions_last_24h
          ),

        avg_transaction_amount:
          Number(
            form.avg_transaction_amount
          ),

        failed_attempts:
          Number(
            form.failed_attempts
          ),

        device_changed:
          Number(
            form.device_changed
          ),

        location_changed:
          Number(
            form.location_changed
          ),

        ip_risk_score:
          Number(
            form.ip_risk_score
          ),

        previous_chargebacks:
          Number(
            form.previous_chargebacks
          ),

        transaction_hour:
          Number(
            form.transaction_hour
          ),

        payment_method:
          form.payment_method,
      };

      const response =
        await axios.post(
          `${API_URL}/api/v1/transactions/new`,
          payload
        );

      setResult(
        response.data
      );

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
        "Unable to assess transaction."
      );

    } finally {

      setSubmitting(false);

    }
  };

  return (
    <div className="page-container">

      <div className="page-top new-transaction-header">

        <div>

          <button
            className="back-button"
            onClick={onBack}
          >
            <ArrowLeft size={15} />
            Back
          </button>

          <div className="eyebrow">
            RISK ASSESSMENT
          </div>

          <h2>
            New Transaction
          </h2>

          <p>
            Add a customer and assess a payment
            transaction with RiskSentinel.
          </p>

        </div>

      </div>


      {result ? (

        <div className="assessment-result">

          <div className="result-icon">
            {result.transaction.risk_level ===
            "HIGH" ? (
              <ShieldAlert size={30} />
            ) : (
              <CheckCircle2 size={30} />
            )}
          </div>

          <span className="small-label">
            RISK ASSESSMENT COMPLETE
          </span>

          <div className="result-score">

            {result.transaction.risk_score}

            <span>/100</span>

          </div>

          <span
            className={`risk-badge ${result.transaction.risk_level.toLowerCase()}`}
          >
            {result.transaction.risk_level}
          </span>

          <p>
            Recommended Action:
          </p>

          <strong>
            {result.transaction.recommended_action}
          </strong>

          <div className="result-reasons">

            {result.transaction.reasons.map((reason, index) => {
                return (
                <div key={index}>
                  <ShieldAlert size={14} />
                  {reason}
                </div>
              );
            })}

          </div>

          <div className="customer-history-card">

            <div className="section-heading">
              Customer History
            </div>

            <div className="customer-history-grid">

              <HistoryItem
                label="Previous Transactions"
                value={
                  result.customer_history
                    ?.previous_transaction_count ?? 0
                }
              />

              <HistoryItem
                label="Historical Avg. Amount"
                value={
                  `Rs.${Number(
                    result.customer_history
                      ?.historical_average_amount || 0
                  ).toLocaleString("en-IN")}`
                }
              />

              <HistoryItem
                label="Previous High-Risk"
                value={
                  result.customer_history
                    ?.previous_high_risk_count ?? 0
                }
              />

              <HistoryItem
                label="Previously Blocked"
                value={
                  result.customer_history
                    ?.previous_blocked_count ?? 0
                }
              />

            </div>

          </div>

          <button
            className="new-assessment-button"
            onClick={() => {
              setResult(null);
              setForm((previous) => ({
                ...previous,
                amount: "",
              }));
            }}
          >
            Assess Another Transaction
          </button>

        </div>

      ) : (

        <form
          className="transaction-form"
          onSubmit={submitTransaction}
        >

          {/* CUSTOMER */}

          <section className="form-card">

            <div className="form-heading">

              <div>
                <h3>
                  Customer Information
                </h3>

                <p>
                  Identify the customer associated
                  with this payment.
                </p>
              </div>

            </div>


            <div className="form-grid">

              <FormInput
                label="Customer ID"
                value={form.customer_id}
                onChange={(value) =>
                  updateField(
                    "customer_id",
                    value
                  )
                }
                required
                placeholder="CUST-1001"
              />

              <FormInput
                label="Customer Name"
                value={form.name}
                onChange={(value) =>
                  updateField(
                    "name",
                    value
                  )
                }
                required
                placeholder="Customer name"
              />

              <FormInput
                label="Email"
                value={form.email}
                onChange={(value) =>
                  updateField(
                    "email",
                    value
                  )
                }
                placeholder="customer@example.com"
              />

              <FormInput
                label="Account Age (days)"
                type="number"
                value={form.account_age_days}
                onChange={(value) =>
                  updateField(
                    "account_age_days",
                    value
                  )
                }
                required
              />

            </div>

          </section>


          {/* TRANSACTION */}

          <section className="form-card">

            <div className="form-heading">

              <div>
                <h3>
                  Transaction Information
                </h3>

                <p>
                  Provide the transaction and
                  behavioral signals.
                </p>
              </div>

            </div>


            <div className="form-grid">

              <FormInput
                label="Transaction Amount"
                type="number"
                value={form.amount}
                onChange={(value) =>
                  updateField(
                    "amount",
                    value
                  )
                }
                required
                placeholder="18500"
              />

              <FormInput
                label="Average Transaction Amount"
                type="number"
                value={
                  form.avg_transaction_amount
                }
                onChange={(value) =>
                  updateField(
                    "avg_transaction_amount",
                    value
                  )
                }
                required
                placeholder="1200"
              />

              <FormInput
                label="Transactions Last 24h"
                type="number"
                value={
                  form.transactions_last_24h
                }
                onChange={(value) =>
                  updateField(
                    "transactions_last_24h",
                    value
                  )
                }
              />

              <FormInput
                label="Failed Attempts"
                type="number"
                value={
                  form.failed_attempts
                }
                onChange={(value) =>
                  updateField(
                    "failed_attempts",
                    value
                  )
                }
              />

              <FormSelect
                label="Payment Method"
                value={
                  form.payment_method
                }
                options={[
                  "UPI",
                  "CARD",
                  "NETBANKING",
                  "WALLET",
                ]}
                onChange={(value) =>
                  updateField(
                    "payment_method",
                    value
                  )
                }
              />

              <FormInput
                label="Transaction Hour"
                type="number"
                value={
                  form.transaction_hour
                }
                onChange={(value) =>
                  updateField(
                    "transaction_hour",
                    value
                  )
                }
              />

              <FormSelect
                label="Device Changed"
                value={
                  String(
                    form.device_changed
                  )
                }
                options={[
                  "0",
                  "1",
                ]}
                onChange={(value) =>
                  updateField(
                    "device_changed",
                    value
                  )
                }
              />

              <FormSelect
                label="Location Changed"
                value={
                  String(
                    form.location_changed
                  )
                }
                options={[
                  "0",
                  "1",
                ]}
                onChange={(value) =>
                  updateField(
                    "location_changed",
                    value
                  )
                }
              />

              <FormInput
                label="IP Risk Score"
                type="number"
                step="0.01"
                value={
                  form.ip_risk_score
                }
                onChange={(value) =>
                  updateField(
                    "ip_risk_score",
                    value
                  )
                }
              />

              <FormInput
                label="Previous Chargebacks"
                type="number"
                value={
                  form.previous_chargebacks
                }
                onChange={(value) =>
                  updateField(
                    "previous_chargebacks",
                    value
                  )
                }
              />

            </div>

          </section>


          {error && (

            <div className="form-error">
              <ShieldAlert size={15} />
              {error}
            </div>

          )}


          <button
            type="submit"
            className="assess-button"
            disabled={submitting}
          >

            <Sparkles size={17} />

            {submitting
              ? "Assessing Transaction..."
              : "Assess Transaction"}

          </button>

        </form>

      )}

    </div>
  );
}


/* =========================================
   FORM COMPONENTS
========================================= */

function FormInput({
  label,
  value,
  onChange,
  type = "text",
  required = false,
  placeholder = "",
  step,
}) {
  return (
    <label className="form-field">

      <span>
        {label}
        {required && (
          <b> *</b>
        )}
      </span>

      <input
        type={type}
        value={value}
        required={required}
        placeholder={placeholder}
        step={step}
        onChange={(e) =>
          onChange(e.target.value)
        }
      />

    </label>
  );
}


function FormSelect({
  label,
  value,
  options,
  onChange,
}) {
  return (
    <label className="form-field">

      <span>
        {label}
      </span>

      <select
        value={value}
        onChange={(e) =>
          onChange(e.target.value)
        }
      >

        {options.map((option) => {
            return (
            <option
              key={option}
              value={option}
            >
              {option}
            </option>
          );
        })}

      </select>

    </label>
  );
}

export default NewTransaction;
function HistoryItem({
  label,
  value,
}) {
  return (
    <div className="history-item">

      <span>{label}</span>

      <strong>{value}</strong>

    </div>
  );
}
