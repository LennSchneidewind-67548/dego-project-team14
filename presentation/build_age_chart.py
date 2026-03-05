import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

MARINE = "#2c5f8a"
PLUM   = "#7d233e"
GRAY   = "#1A1A2E"   # third colour for additional groupings

df = pd.read_csv("data/cleaned_credit_applications.csv")
df["dob"] = pd.to_datetime(df["applicant_info.date_of_birth"], errors="coerce")
today = pd.Timestamp("2026-03-05")
df["age"] = (today - df["dob"]).dt.days / 365.25

def age_group(a):
    if a < 30:   return "<30"
    elif a <= 50: return "30-50"
    else:         return "50+"

df["age_group"] = df["age"].apply(age_group)

ORDER   = ["<30", "30-50", "50+"]
overall = df.groupby("age_group")["decision.loan_approved"].mean() * 100
overall = overall.reindex(ORDER)

cross = (
    df.groupby(["age_group", "applicant_info.gender"])["decision.loan_approved"]
    .mean() * 100
).unstack()
cross = cross.reindex(ORDER)

ref_rate   = overall.max()
threshold  = ref_rate * 0.8
di_ratio   = overall.min() / ref_rate
worst_val  = cross["Female"].min()
worst_lbl  = ORDER[int(np.argmin(cross["Female"].values))]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
fig.patch.set_facecolor("white")

# ── Left panel: Age group overall ──────────────────────────────────────
colors_left = []
for group, v in zip(ORDER, overall):
    if group == "50+":
        colors_left.append(GRAY)
    elif v < threshold:
        colors_left.append(PLUM)
    else:
        colors_left.append(MARINE)
bars1 = ax1.bar(ORDER, overall, color=colors_left, width=0.5, zorder=3)

ax1.axhline(threshold, color="#f4a623", linestyle="--", linewidth=2, zorder=4)
ax1.text(2.32, threshold + 0.5, "4/5 Rule", color="#f4a623",
         fontsize=10, fontweight="bold", va="bottom")

for bar, val in zip(bars1, overall):
    ax1.text(bar.get_x() + bar.get_width() / 2, val + 0.8,
             f"{val:.1f}%", ha="center", va="bottom",
             fontsize=12, fontweight="bold", color="black")

ax1.set_ylim(0, 80)
ax1.set_ylabel("Approval Rate (%)", fontsize=11)
ax1.set_title(
    f"Age Group Approval Rate\n(DI <30 vs 30-50: {di_ratio:.3f})",
    fontsize=11
)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.set_axisbelow(True)
ax1.yaxis.grid(True, linestyle="-", linewidth=0.5, color="#dddddd", zorder=0)
ax1.tick_params(axis="x", labelsize=12)
ax1.tick_params(axis="y", labelsize=10)

# ── Right panel: Age × Gender grouped bars ────────────────────────────
x      = np.arange(len(ORDER))
width  = 0.35

bars_f = ax2.bar(x - width / 2, cross["Female"], width, color=PLUM,  label="Female", zorder=3)
bars_m = ax2.bar(x + width / 2, cross["Male"],   width, color=MARINE, label="Male",  zorder=3)

for bar, val in zip(bars_f, cross["Female"]):
    ax2.text(bar.get_x() + bar.get_width() / 2, val + 0.8,
             f"{val:.0f}%", ha="center", va="bottom",
             fontsize=10, fontweight="bold", color="black")

for bar, val in zip(bars_m, cross["Male"]):
    ax2.text(bar.get_x() + bar.get_width() / 2, val + 0.8,
             f"{val:.0f}%", ha="center", va="bottom",
             fontsize=10, fontweight="bold", color="black")

ax2.set_ylim(0, 85)
ax2.set_xticks(x)
ax2.set_xticklabels(ORDER, fontsize=12)
ax2.tick_params(axis="y", labelsize=10)
ax2.set_title(
    f"Age \u00d7 Gender Interaction\n(Worst: Young Female = {worst_val:.1f}%)",
    fontsize=11
)
ax2.legend(loc="upper right", fontsize=10)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.set_axisbelow(True)
ax2.yaxis.grid(True, linestyle="-", linewidth=0.5, color="#dddddd", zorder=0)

plt.tight_layout()
out = "presentation/age_bias_chart.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Saved {out}")
