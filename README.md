# RiskSentinel
**AI-Powered Payment Risk Management & Fraud Detection**

RiskSentinel is a fintech risk-management application that helps merchants identify potentially fraudulent payment transactions before they result in financial loss.

The system combines machine learning, customer behavior analysis, AI investigation, and human review to produce a real-time risk assessment for each transaction.

## 🚀 Project Overview
RiskSentinel analyzes transaction-level and customer-level signals such as:
- Transaction amount
- Account age
- Transaction velocity
- Failed payment attempts
- Device changes
- Location changes
- IP risk score
- Previous chargebacks
- Payment method
- Customer spending history
- Previous high-risk and blocked activity

An XGBoost model generates a fraud probability, which is converted into a risk score and recommendation.
The system also provides an AI Investigator that explains the existing risk assessment and helps reviewers understand why a transaction was flagged.

## ✨ Key Features
### 📊 Dashboard
A centralized fintech-style dashboard for monitoring payment activity, risk levels, alerts, and investigations.

### 💳 Transaction Monitoring
Search, filter, and inspect transactions by:
- Risk level
- Payment method
- Review decision
- Transaction details

### 🧠 AI Risk Scoring
The XGBoost model evaluates transaction and customer-history features and produces:
- Risk probability
- Risk score (0–100)
- Risk level
- Recommended action
- Risk reasons

### 👤 Customer History
RiskSentinel keeps track of customer behavior, including:
- Previous transaction count
- Historical average transaction amount
- Amount compared with historical behavior
- Previous high-risk transactions
- Previous blocked transactions
- Recent transaction velocity

### 🤖 AI Investigation
The AI Investigator provides an explanation of the model assessment and recommends an action for human reviewers.

### 🚨 Alerts
Automatically surfaces high-risk and pending-review transactions.

### 📈 Reports & Model Performance
Displays live transaction statistics and model evaluation metrics such as:
- Precision
- Recall
- F1 score
- ROC-AUC
- False positives
- False negatives
- Estimated business cost

### ✅ Human Review
Reviewers can mark transactions as:
- ALLOW
- REVIEW
- BLOCK

## 🏗️ Architecture
```text
React Frontend 
      │ 
      ▼ 
FastAPI Backend 
      │ 
 ├────┴────────┐ 
 ▼             ▼ 
XGBoost Model  AI Investigator 
 │             │ 
 └────┬────────┘ 
      ▼ 
PostgreSQL / Supabase 
 ┌────┴────────┐ 
 ▼             ▼ 
customers   transactions
```

## 🛠️ Tech Stack
**Frontend**
- React
- Vite
- Axios
- Lucide React
- CSS

**Backend**
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL

**Machine Learning**
- XGBoost
- Scikit-learn
- Pandas
- NumPy
- Joblib

**AI**
- OpenAI API

**Database**
- Supabase PostgreSQL

## 💻 Run Locally
Deployment is currently not required.
The complete application can be run locally using the ports below.

### 1. Clone the repository
```bash
git clone https://github.com/Aryan-O7/RiskSentinel.git 
cd RiskSentinel
```

### 2. Backend Setup
Create and activate a virtual environment.

**Windows**
```cmd
python -m venv venv 
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv 
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_URL=your_supabase_postgresql_connection_string 
OPENAI_API_KEY=your_openai_api_key 
FRONTEND_URL=http://localhost:5173
```

**Important**: Never commit `.env` to GitHub. Use `.env.example` as the template.

### 4. Prepare the Database
The application uses PostgreSQL through Supabase.
Create the database tables with:
```bash
python -c "from backend.database import Base, engine; import backend.models; Base.metadata.create_all(bind=engine); print('Tables created successfully')"
```
You should have at least `customers` and `transactions` in your Supabase Table Editor.

### 5. Run the Backend
From the project root:
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
- Backend: http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/health
- FastAPI documentation: http://127.0.0.1:8000/docs

### 6. Run the Frontend
Open a second terminal.
```bash
cd frontend 
npm install 
npm run dev
```
Vite will normally start the frontend at http://localhost:5173. Open that address in your browser.

## 🔌 Local Ports
| Service | Local URL |
|---------|-----------|
| React + Vite Frontend | http://localhost:5173 |
| FastAPI Backend | http://127.0.0.1:8000 |
| FastAPI Swagger Docs | http://127.0.0.1:8000/docs |
| Backend Health Check | http://127.0.0.1:8000/health |

**Frontend → Backend**
The React application should use `http://127.0.0.1:8000` as the local API base URL.
If the API URL is stored in a frontend environment variable, use:
`VITE_API_URL=http://127.0.0.1:8000`

## 🧪 Recommended Demo Flow
For a project demonstration, use this sequence:
1. Open Dashboard
2. Create / select customer
3. Create a new transaction
4. System reads customer history
5. XGBoost calculates risk
6. Risk score and reasons are displayed
7. Open AI Investigation
8. Review AI explanation
9. Allow / Review / Block
10. Verify transaction is saved in Supabase

## 🤖 Machine Learning Pipeline
The training dataset is synthetic and is stored in:
`data/transactions.csv`

The ML workflow is:
`Synthetic Transactions` → `Customer History Features` → `Train XGBoost` → `Evaluate Precision / Recall / F1 / ROC-AUC` → `Threshold Analysis` → `Final Risk Model`

- The trained model is stored in: `ml/saved_models/xgboost_risk_model.pkl`
- Metrics are stored in: `ml/saved_models/metrics.json`

## 📁 Project Structure
```text
RiskSentinel/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services/
│       ├── risk_service.py
│       ├── ai_investigator.py
│       └── customer_history.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── styles.css
│   │   └── pages/
│   │       ├── Transactions.jsx
│   │       ├── RiskAnalysis.jsx
│   │       ├── AIInvestigations.jsx
│   │       ├── Alerts.jsx
│   │       ├── Reports.jsx
│   │       ├── Models.jsx
│   │       ├── Settings.jsx
│   │       └── NewTransaction.jsx
├── ml/
│   ├── generate_data.py
│   ├── train.py
│   ├── train_xgboost.py
│   ├── threshold_analysis.py
│   ├── final_evaluation.py
│   ├── risk_engine.py
│   └── saved_models/
├── data/
│   └── transactions.csv
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔐 Security
Never commit secrets to GitHub. Keep these values private:
- `DATABASE_URL`
- `OPENAI_API_KEY`
- Supabase password

Use environment variables instead.
Example:
```env
DATABASE_URL=... 
OPENAI_API_KEY=... 
FRONTEND_URL=http://localhost:5173
```

## 🎯 Risk Levels
RiskSentinel converts model probability into application actions.
- **LOW** → ALLOW
- **MEDIUM** → MONITOR
- **HIGH** → MANUAL_REVIEW

The final model threshold should be selected using the project's threshold-analysis and business-cost evaluation rather than assuming that one fixed threshold is universally optimal.

## 📌 Current Project Status
**Completed**
- Dashboard
- Transactions
- Risk Analysis
- AI Investigations
- Reports
- Alerts
- Models
- Settings
- Customer creation
- Customer history
- XGBoost risk model
- AI investigation layer
- Supabase PostgreSQL integration
- Local end-to-end workflow

**Current Deployment Status**
The project is designed to run locally for demonstration.
- Frontend → `localhost:5173`
- Backend → `127.0.0.1:8000`
- Database → Supabase PostgreSQL

Cloud deployment can be added later without changing the core application architecture.

## 👨‍💻 Author
**Aryan**
GitHub: [https://github.com/Aryan-O7/RiskSentinel](https://github.com/Aryan-O7/RiskSentinel)