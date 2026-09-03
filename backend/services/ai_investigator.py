import os
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not configured."
    )

client = OpenAI(api_key=api_key)


def investigate_transaction(
    transaction: dict,
    risk_result: dict
) -> str:
    """
    Generate a structured AI investigation
    based only on the transaction and the
    existing ML risk assessment.
    """

    prompt = f"""
You are a payment-risk investigation assistant.

Your job is to explain an existing machine-learning
risk assessment. Do NOT invent transaction facts.
Do NOT change the ML risk score.

Transaction:
{transaction}

ML Risk Assessment:
{risk_result}

Provide a concise investigation with exactly
these sections:

1. Severity
2. Key Findings
3. Assessment
4. Recommended Action
5. Confidence

Rules:
- Base every statement on the supplied data.
- Do not claim fraud is confirmed.
- Distinguish between a risk signal and proof of fraud.
- Recommended Action must be one of:
  ALLOW, MONITOR, MANUAL_REVIEW, BLOCK.
- Prefer MANUAL_REVIEW when the signals are concerning
  but the evidence does not establish fraud.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text
