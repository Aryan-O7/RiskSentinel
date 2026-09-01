import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("threshold_results.csv")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# --- Plot 1: Precision / Recall / F1 ---
axes[0].plot(df["Threshold"], df["Precision"], marker="o", label="Precision")
axes[0].plot(df["Threshold"], df["Recall"], marker="o", label="Recall")
axes[0].plot(df["Threshold"], df["F1"], marker="o", label="F1")
axes[0].set_xlabel("Decision Threshold")
axes[0].set_ylabel("Score")
axes[0].set_title("Precision / Recall / F1 vs Threshold")
axes[0].legend()
axes[0].grid(True)

# --- Plot 2: Business Cost ---
axes[1].plot(df["Threshold"], df["FP_Cost"], marker="s", label="FP Cost", color="orange")
axes[1].plot(df["Threshold"], df["FN_Cost"], marker="s", label="FN Cost", color="red")
axes[1].plot(df["Threshold"], df["Total_Cost"], marker="o", label="Total Cost", color="purple", linewidth=2)

# Mark the optimal threshold
best_idx = df["Total_Cost"].idxmin()
best_threshold = df.loc[best_idx, "Threshold"]
axes[1].axvline(x=best_threshold, color="green", linestyle="--", label=f"Optimal ({best_threshold})")

axes[1].set_xlabel("Decision Threshold")
axes[1].set_ylabel("Estimated Cost (Rs.)")
axes[1].set_title("Business Cost vs Threshold")
axes[1].legend()
axes[1].grid(True)

plt.suptitle("RiskSentinel - Threshold Optimization (Optimized XGBoost)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("data/threshold_analysis.png", dpi=100, bbox_inches="tight")
plt.close()

print("Chart saved: data/threshold_analysis.png")
print(f"Optimal threshold by total cost: {best_threshold}")
