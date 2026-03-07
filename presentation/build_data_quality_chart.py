from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_loading import load_raw_data


MARINE = "#356a99"
TEXT = "#20213a"
GRID = "#d6d6d6"
BG = "#f3f3f3"


def count_true_flags(series: pd.Series) -> int:
    return int(series.astype(str).str.strip().str.lower().isin(["true", "1", "yes"]).sum())


def main() -> None:
    raw = load_raw_data(ROOT / "data" / "raw_credit_applications.json")
    clean = pd.read_csv(ROOT / "data" / "cleaned_credit_applications.csv")

    duplicate_ids_removed = int(len(raw) - len(clean))
    gender_recoded = int(raw["applicant_info.gender"].isin(["F", "M"]).sum())
    date_standardized = int(len(clean))
    income_normalized = int(len(clean))
    income_recovered = count_true_flags(clean["income_recovered_from_salary"])
    invalid_or_reviewed = (
        2  # negative credit history months
        + 1  # non-positive income
        + 4  # invalid emails
        + count_true_flags(clean["dti_review_flag"])
        + count_true_flags(clean["savings_review_flag"])
    )

    labels = [
        "Date format\nstandardization",
        "Income normalization\n(string -> numeric)",
        "Gender recoding\n(4 variants -> 2)",
        "Invalid/reviewed values\n(credit, email, DTI, savings)",
        "Income recovered\nfrom annual_salary",
        "Duplicate IDs",
    ]
    values = [
        date_standardized,
        income_normalized,
        gender_recoded,
        invalid_or_reviewed,
        income_recovered,
        duplicate_ids_removed,
    ]

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    bars = ax.barh(labels, values, color=MARINE, height=0.5, zorder=3)
    ax.invert_yaxis()

    for bar, value in zip(bars, values):
        ax.text(
            value + 3,
            bar.get_y() + bar.get_height() / 2,
            f"{value} records",
            va="center",
            ha="left",
            fontsize=20,
            fontweight="bold",
            color=TEXT,
        )

    ax.set_xlim(0, 620)
    ax.set_xlabel("Records Affected", fontsize=18, color="#555555", labelpad=12)
    ax.xaxis.grid(True, linestyle="-", linewidth=1, color=GRID, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize=16, colors="#555555")
    ax.tick_params(axis="y", labelsize=18, colors="#555555", pad=8, length=8, width=2)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_color("#bdbdbd")
    ax.spines["left"].set_linewidth(2)

    fig.text(
        0.12,
        0.02,
        "Additional plausibility checks found 1 invalid DTI and 1 negative savings value; "
        "both were flagged for review and set to NaN, while 5 incomes were recovered from "
        "annual_salary with provenance tracking.",
        ha="left",
        va="bottom",
        fontsize=13,
        color=TEXT,
        wrap=True,
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.18)

    out = ROOT / "presentation" / "data_quality_chart_updated.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
