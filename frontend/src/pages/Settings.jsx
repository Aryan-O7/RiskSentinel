import { useState } from "react";
import {
  Bell,
  BrainCircuit,
  CheckCircle2,
  Database,
  Lock,
  Save,
  Settings as SettingsIcon,
  Shield,
  SlidersHorizontal,
} from "lucide-react";

function Settings() {
  const [mediumThreshold, setMediumThreshold] =
    useState(35);

  const [highThreshold, setHighThreshold] =
    useState(70);

  const [aiEnabled, setAiEnabled] =
    useState(true);

  const [alertsEnabled, setAlertsEnabled] =
    useState(true);

  const [saved, setSaved] =
    useState(false);

  const saveSettings = () => {
    localStorage.setItem(
      "risksentinel_settings",
      JSON.stringify({
        mediumThreshold,
        highThreshold,
        aiEnabled,
        alertsEnabled,
      })
    );

    setSaved(true);

    setTimeout(() => {
      setSaved(false);
    }, 2000);
  };

  return (
    <div className="page-container">

      {/* Header */}

      <div className="page-top">

        <div>

          <div className="eyebrow">
            SYSTEM CONFIGURATION
          </div>

          <h2>Settings</h2>

          <p>
            Configure RiskSentinel risk and
            application preferences.
          </p>

        </div>

        <button
          className="settings-save-button"
          onClick={saveSettings}
        >
          <Save size={16} />

          {saved
            ? "Saved"
            : "Save Changes"}
        </button>

      </div>


      <div className="settings-grid">

        {/* Risk configuration */}

        <section className="panel settings-section">

          <div className="settings-section-header">

            <div className="settings-icon blue">
              <SlidersHorizontal size={19} />
            </div>

            <div>

              <h3>
                Risk Configuration
              </h3>

              <p>
                Configure the application's risk
                classification boundaries.
              </p>

            </div>

          </div>


          <div className="settings-body">

            <div className="setting-row">

              <div>

                <strong>
                  Medium Risk Threshold
                </strong>

                <span>
                  Scores above this value enter
                  medium-risk territory.
                </span>

              </div>

              <div className="threshold-control">

                <input
                  type="number"
                  min="1"
                  max={highThreshold - 1}
                  value={mediumThreshold}
                  onChange={(e) =>
                    setMediumThreshold(
                      Number(e.target.value)
                    )
                  }
                />

                <span>
                  /100
                </span>

              </div>

            </div>


            <div className="setting-row">

              <div>

                <strong>
                  High Risk Threshold
                </strong>

                <span>
                  Scores at or above this value
                  require high-risk handling.
                </span>

              </div>

              <div className="threshold-control">

                <input
                  type="number"
                  min={mediumThreshold + 1}
                  max="100"
                  value={highThreshold}
                  onChange={(e) =>
                    setHighThreshold(
                      Number(e.target.value)
                    )
                  }
                />

                <span>
                  /100
                </span>

              </div>

            </div>


            <div className="threshold-preview">

              <div>
                <span>
                  Current classification
                </span>
              </div>

              <div className="threshold-preview-values">

                <span className="preview-low">
                  LOW
                  <small>
                    &lt; {mediumThreshold}
                  </small>
                </span>

                <span className="preview-medium">
                  MEDIUM
                  <small>
                    {mediumThreshold}–
                    {highThreshold - 1}
                  </small>
                </span>

                <span className="preview-high">
                  HIGH
                  <small>
                    ≥ {highThreshold}
                  </small>
                </span>

              </div>

            </div>

          </div>

        </section>


        {/* Model configuration */}

        <section className="panel settings-section">

          <div className="settings-section-header">

            <div className="settings-icon purple">
              <BrainCircuit size={19} />
            </div>

            <div>

              <h3>
                Model Configuration
              </h3>

              <p>
                Current machine-learning and AI
                configuration.
              </p>

            </div>

          </div>


          <div className="settings-body">

            <div className="setting-row">

              <div>

                <strong>
                  Active Model
                </strong>

                <span>
                  Model used for payment risk scoring.
                </span>

              </div>

              <span className="setting-value-badge">
                XGBoost
              </span>

            </div>


            <div className="setting-row">

              <div>

                <strong>
                  Model Status
                </strong>

                <span>
                  Current model deployment state.
                </span>

              </div>

              <span className="status-value">

                <CheckCircle2 size={14} />

                Active

              </span>

            </div>


            <div className="setting-row toggle-row">

              <div>

                <strong>
                  AI Investigation
                </strong>

                <span>
                  Enable LLM-assisted investigation.
                </span>

              </div>

              <button
                className={`toggle ${
                  aiEnabled
                    ? "enabled"
                    : ""
                }`}
                onClick={() =>
                  setAiEnabled(
                    !aiEnabled
                  )
                }
              >
                <span />
              </button>

            </div>

          </div>

        </section>


        {/* Alerts */}

        <section className="panel settings-section">

          <div className="settings-section-header">

            <div className="settings-icon orange">
              <Bell size={19} />
            </div>

            <div>

              <h3>
                Alert Preferences
              </h3>

              <p>
                Configure risk-alert behavior.
              </p>

            </div>

          </div>


          <div className="settings-body">

            <div className="setting-row toggle-row">

              <div>

                <strong>
                  Risk Alerts
                </strong>

                <span>
                  Display high-risk transactions in
                  the Alerts module.
                </span>

              </div>

              <button
                className={`toggle ${
                  alertsEnabled
                    ? "enabled"
                    : ""
                }`}
                onClick={() =>
                  setAlertsEnabled(
                    !alertsEnabled
                  )
                }
              >
                <span />
              </button>

            </div>


            <div className="setting-row">

              <div>

                <strong>
                  Critical Risk
                </strong>

                <span>
                  Critical alerts are generated for
                  scores of 90 or above.
                </span>

              </div>

              <span className="critical-value">
                ≥ 90
              </span>

            </div>


            <div className="setting-row">

              <div>

                <strong>
                  Human Review
                </strong>

                <span>
                  Review workflow is always available.
                </span>

              </div>

              <span className="status-value">
                <CheckCircle2 size={14} />
                Enabled
              </span>

            </div>

          </div>

        </section>


        {/* System */}

        <section className="panel settings-section">

          <div className="settings-section-header">

            <div className="settings-icon green">
              <SettingsIcon size={19} />
            </div>

            <div>

              <h3>
                System Status
              </h3>

              <p>
                Current application connectivity.
              </p>

            </div>

          </div>


          <div className="settings-body">

            <SystemStatus
              icon={<Shield size={16} />}
              label="Risk Engine"
              status="Operational"
            />

            <SystemStatus
              icon={<Database size={16} />}
              label="Database"
              status="Connected"
            />

            <SystemStatus
              icon={<Lock size={16} />}
              label="Environment"
              status="Protected"
            />

          </div>

        </section>

      </div>


      <div className="settings-note">

        <Shield size={15} />

        <span>
          Risk thresholds shown here are application
          configuration values. Production deployment
          will move these settings to the server-side
          configuration layer.
        </span>

      </div>

    </div>
  );
}


/* =========================================
   COMPONENT
========================================= */

function SystemStatus({
  icon,
  label,
  status,
}) {
  return (
    <div className="system-setting-row">

      <div className="system-setting-label">

        {icon}

        <strong>
          {label}
        </strong>

      </div>

      <span className="status-value">
        <CheckCircle2 size={14} />
        {status}
      </span>

    </div>
  );
}

export default Settings;
