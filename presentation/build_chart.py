import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/cleaned_credit_applications.csv")

rates = df.groupby("applicant_info.gender")["decision.loan_approved"].mean() * 100
male_rate = rates["Male"]
female_rate = rates["Female"]
dir_ratio = female_rate / male_rate
threshold_line = male_rate * 0.8

fig, ax = plt.subplots(figsize=(7, 6))
fig.patch.set_facecolor("white")

bars = ax.bar(
    ["Male", "Female"],
    [male_rate, female_rate],
    color=["#2c5f8a", "#7d233e"],
    width=0.5,
    zorder=3,
)

ax.axhline(threshold_line, color="#f4a623", linestyle="--", linewidth=2, zorder=4)
ax.text(
    1.55, threshold_line + 0.8,
    "4/5 Rule\nThreshold",
    color="#f4a623", fontsize=11, fontweight="bold", va="bottom", ha="left",
)

for bar, val in zip(bars, [male_rate, female_rate]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        val + 0.8,
        f"{val:.1f}%",
        ha="center", va="bottom", fontsize=14, fontweight="bold", color="black",
    )

ax.set_ylim(0, 80)
ax.set_ylabel("Approval Rate (%)", fontsize=12)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Male", "Female"], fontsize=13)
ax.yaxis.set_tick_params(labelsize=11)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_axisbelow(True)
ax.yaxis.grid(True, linestyle="-", linewidth=0.5, color="#dddddd", zorder=0)

plt.tight_layout()
plt.savefig("presentation/disparate_impact_gender.png", dpi=150, bbox_inches="tight")
print("Saved disparate_impact_gender.png")
