import json
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

METRICS_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "saved_models",
    "metrics.json"
)


def get_model_metrics() -> dict:
    """
    Read the latest evaluated model metrics.
    """

    if not os.path.exists(METRICS_PATH):
        raise FileNotFoundError(
            "Model metrics have not been generated yet."
        )

    with open(
        METRICS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)
