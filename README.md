# RiskSentinel

AI-powered payment fraud detection and risk scoring.

## Problem

Merchants need to identify suspicious payments while
reducing false positives against legitimate customers.

## Architecture

Transaction
→ FastAPI
→ XGBoost
→ Risk Engine
→ AI Investigation
→ Human Review
→ PostgreSQL / SQLite

## Features

- Transaction risk scoring
- Fraud detection
- Risk-factor explanations
- AI investigation
- Human review workflow
- Transaction history
- Business-cost analysis

## Evaluation

Precision: 0.3610
Recall: 0.7352
F1: 0.4842
ROC-AUC: 0.8288

## Tech Stack

Python
FastAPI
XGBoost
SQLite (Easily Swappable to PostgreSQL)
React
OpenAI API