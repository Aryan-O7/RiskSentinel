import os
import sys


# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------

BACKEND_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

PROJECT_ROOT = os.path.dirname(
    BACKEND_DIR
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


# --------------------------------------------------
# Import risk engine
# --------------------------------------------------

from ml.risk_engine import (
    assess_transaction
)


def assess_risk(
    transaction: dict
) -> dict:
    """
    Send a transaction to the RiskSentinel
    risk engine and return the assessment.
    """

    result = assess_transaction(
        transaction
    )

    return result
