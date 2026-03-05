import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

MARINE = "#2c5f8a"
PLUM   = "#7d233e"

df = pd.read_csv("data/cleaned_credit_applications.csv")
df["dob"] = pd.to_datetime(df["applicant_info.date_of_birth"], errors="coerce")
today = pd.Timestamp("2026-03-05")
df["age"] = (today - df["dob"]).dt.days / 365.25

def age_group(a):
    if a < 30:    return "<30"
    elif a <= 50: return "30-50"
    else:         return "50+"

df["age_group"] = df["age"].apply(age_group)

def cramers_v(a, b):
    ct = pd.crosstab(a, b)
    chi2 = chi2_contingency(ct)[0]
    n = ct.to_numpy().sum()
    phi2 = chi2 / n
    r, k = ct.shape
    phi2_corr = max(0, phi2 - (k - 1) * (r - 1) / (n - 1))
    r_corr = r - (r - 1) ** 2 / (n - 1)
    k_corr = k - (k - 1) ** 2 / (n - 1)
    denom = min(k_corr - 1, r_corr - 1)
    return np.sqrt(phi2_corr / denom) if denom > 0 else 0

labels = ["Gender vs Age", "ZIP vs Age", "ZIP vs Gender"]
values = [
    cramers_v(df["applicant_info.gender"], df["age_group"]),
    cramers_v(df["applicant_info.zip_code"], df["age_group"]),
    cramers_v(df["applicant_info.zip_code"], df["applicant_info.gender"]),
]

STRONG = 0.5
colors = [PLUM if v >= STRONG else MARINE for v in values]

fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor("white")

bars = ax.barh(labels, values, color=colors, height=0.45, zorder=3)

ax.axvline(STRONG, color="#f4a623", linestyle="--", linewidth=2, zorder=4)
ax.text(STRONG + 0.01, 2.45, "Strong\nAssociation (>0.5)",
        color="#f4a623", fontsize=10, fontweight="bold", va="top")

for bar, val in zip(bars, values):
    ax.text(
        val + 0.01, bar.get_y() + bar.get_height() / 2,
        f"V = {val:.3f}",
        va="center", ha="left", fontsize=12, fontweight="bold", color="black",
    )

ax.set_xlim(0, max(values) * 1.3)
ax.set_xlabel("Cramér's V (Association Strength)", fontsize=11)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_axisbelow(True)
ax.xaxis.grid(True, linestyle="-", linewidth=0.5, color="#dddddd", zorder=0)
ax.tick_params(axis="y", labelsize=12)
ax.tick_params(axis="x", labelsize=10)

plt.tight_layout()
out = "presentation/cramers_v_chart.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Saved {out}")
