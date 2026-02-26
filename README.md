# DEGO Project - Team 14

## Executive Summary


## Team Members

| Role | Name | Student ID |
|------|------|------------|
| Data Engineer | Lenn Louis Schneidewind | 67548 |
| Data Scientist | Fatima Zubair | 70319 |
| Governance Officer | Eduarda Dionísio | 56503 |
| Product Lead | Leon Werner Schmidt | 71644 |

## Project Description
Credit scoring bias analysis for DEGO course.

## Data Quality Findings


## Bias Detection & Fairness
# Gender bias – disparate impact

We first normalize `applicant_info.gender` into a cleaned `gender_clean` field with the categories `Male` and `Female` (mapping `M`→`Male` and `F`→`Female`, keeping other values as is). Records with missing or invalid gender remain in the dataset but are excluded when we need a clear binary comparison.

- Approval rate (Male): **65.7%**
- Approval rate (Female): **50.6%**
- Disparate impact ratio (Female vs Male): **0.77**

The disparate impact ratio is defined as the approval rate of the unprivileged group divided by the approval rate of the privileged group.[file:1] Using females as the unprivileged group and males as the privileged group, our DI of 0.77 is below the standard 0.80 “four‑fifths rule” threshold, suggesting potential disparate impact against female applicants that requires governance attention.

We also compute demographic parity difference (female approval rate minus male approval rate), which is **−15.1 percentage points**, reinforcing that female applicants are approved at a materially lower rate. In the notebook, we recommend a two‑proportion z‑test to statistically assess whether this difference is likely due to random variation or reflects a systematic pattern.

From a fairness standpoint, gender should not be used as a model feature, and these metrics (disparate impact and demographic parity difference) should be monitored over time to detect any worsening of gender disparities.[file:1]

# Age‑based approval patterns

To analyze age, we convert `applicant_info.date_of_birth` to a proper datetime and compute approximate age at application. Invalid or missing dates are set to `NaT`, and the corresponding ages are `NaN`; these records are excluded from age‑band comparisons but remain a documented data‑quality limitation.

We group applicants into three age bands:

- **<30**
- **30–50**
- **50+**

Observed approval rates:

- <30: **39.7%**
- 30–50: **62.3%**
- 50+: **61.9%**

These patterns show that younger applicants are much less likely to be approved than older ones for the same product. Treating the <30 group as unprivileged and the 30–50 group as privileged, the resulting disparate impact ratio is well below 0.8, pointing to potential age‑related disparities.[file:1] We recommend complementing this with a simple multivariate analysis (e.g., logistic regression including age plus income, credit history months, and debt‑to‑income) to check whether the penalty for younger applicants persists after controlling for financial risk factors.

# Proxy discrimination – ZIP code as a proxy for gender

We then investigate whether `zip_code` can act as a proxy for gender. Aggregating applications by ZIP and gender shows that several ZIP codes in our sample are effectively associated with a single gender (for example, ZIPs where all applications are male, or all are female).

This means that even if the explicit gender field is removed from the model, a classifier using ZIP could still infer gender with high confidence. In other words, ZIP behaves as a proxy for gender, and using it as a feature can reproduce gender disparities while appearing neutral.[file:1] For this reason, we recommend treating ZIP as a high‑risk feature in the model: its use should be justified, constrained (e.g., coarsened to regions), or monitored with additional fairness checks.


## Privacy Assessment


## Governance Recommendations


## Repository Structure
```
dego-project-team14/
├── README.md
├── data/
│   └── raw_credit_applications.json
├── notebooks/
│   ├── 01-data-quality.ipynb
│   ├── 02-bias-analysis.ipynb
│   └── 03-privacy-demo.ipynb
├── src/
│   └── fairness_utils.py
└── presentation/
    └── final deliverables
```
---

## How to Run


## Individual Contributions
