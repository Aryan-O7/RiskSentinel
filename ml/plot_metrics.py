import matplotlib.pyplot as plt

metrics = {
    "Precision": 0.36,
    "Recall": 0.74,
    "F1": 0.48,
    "ROC-AUC": 0.83
}

plt.figure(figsize=(8, 5))

plt.bar(
    metrics.keys(),
    metrics.values(),
    color=['#4C72B0', '#DD8452', '#55A868', '#C44E52']
)

plt.ylim(0, 1)

plt.ylabel("Score")
plt.title("RiskSentinel Final Model Performance")

# Add value labels on top of bars
for i, v in enumerate(metrics.values()):
    plt.text(i, v + 0.02, str(v), ha='center')

plt.tight_layout()
plt.savefig('ml/performance_chart.png')
print("Chart saved to ml/performance_chart.png")
