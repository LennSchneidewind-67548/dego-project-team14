# DEGO Project - Team 14

## Executive Summary

This report presents the findings of a data governance audit conducted on NovaCred's credit application dataset (502 records). Acting as a Data Governance Task Force, we identified and remediated data quality issues across four dimensions, detected statistically significant bias against female and younger applicants, and assessed the system's compliance with GDPR and the EU AI Act.

**Key findings:**
- **Data quality**: 6 categories of issues identified and remediated: Duplicate records (2), inconsistent data types (income stored as string), 4 gender coding variants, inconsistent date formats, invalid values (negative credit history, non-positive income, invalid emails), and missing/incomplete fields across 13 columns. Final dataset retention rate: 99.6%.
- **Bias**: The gender disparate impact ratio is **0.77** (below the 0.80 four-fifths threshold), confirmed as statistically significant (p = 0.0007). A logistic regression controlling for financial covariates shows gender remains a significant predictor of approval. Applicants under 30 face a DI of **0.63** against the 30–50 group. ZIP code acts as a strong gender proxy (Cramer's V = 0.63).
- **Governance gaps**: 7 PII fields stored without protection, no consent tracking mechanism, no data retention policy, no erasure mechanism, and no audit trail for automated decisions. Credit scoring is classified as high-risk under the EU AI Act (Annex III, 5b), requiring conformity assessment before deployment.

## Team Members

| Role | Name | Student ID |
|------|------|------------|
| Data Engineer | Lenn Louis Schneidewind | 67548 |
| Data Scientist | Fatima Zubair | 70319 |
| Governance Officer | Eduarda Dionisio | 56503 |
| Product Lead | Leon Werner Schmidt | 71644 |

## Project Description
NovaCred is a fintech startup that uses machine learning to make credit decisions. Following a regulatory inquiry about potential discrimination in their lending practices, our team was hired to audit the data for quality issues, detect bias patterns in historical decisions, propose governance controls, and demonstrate compliance with GDPR and AI Act requirements.

## Data Quality Findings

The data quality analysis (`01-data-quality.ipynb`) audited the raw dataset of 502 credit applications across four quality dimensions. All issues were quantified and remediated in code, resulting in a cleaned dataset of 500 records (99.6% retention rate).

### Completeness
- **13 out of 21 columns** contained missing values after flattening the nested JSON.
- `notes` (99.6% missing) and `loan_purpose` (90.0% missing) had the highest missingness but are non-critical optional fields.
- `processing_timestamp` was missing for 87.7% of records.
- `financials.annual_salary` was identified as a mislabeled duplicate of `financials.annual_income` the 5 records with `annual_salary` values were exactly the 5 records missing `annual_income`. These were merged, recovering all income data.
- After standardizing missing value representations (empty strings, whitespace), 14 additional missing values were identified.
- **Critical fields** (income, loan decision, debt-to-income) had **0% missingness** all records are usable for core analysis.

### Consistency
- **Data type mismatch**: `financials.annual_income` was stored as `object` (string) instead of numeric. Converted to `float64`.
- **Gender coding**: 4 distinct representations found (`Male`: 195, `Female`: 193, `F`: 58, `M`: 53, plus 3 missing). Standardized all to `Male`/`Female`.
- **Date formats**: `processing_timestamp` and `applicant_info.date_of_birth` were stored as strings. Converted to `datetime64` with 0 conversion failures.
- **Spending categories**: 15 unique categories with 0 whitespace or encoding inconsistencies.

### Validity
- **Negative credit history months**: 2 records (0.4%) had negative values. Imputed with median (48.0 months).
- **Non-positive income**: 1 record (0.2%) had an invalid income value. Imputed with mean ($82,735).
- **Future dates of birth**: 0 records — all DOBs were valid.
- **Invalid ages**: 0 records outside the 18–120 range.
- **Invalid email formats**: 4 records (0.8%) had malformed email addresses. Set to NaN.
- **Spending amounts**: All 827 nested spending entries were valid (0 non-numeric, 0 negative, 0 zero).
- All imputed values are flagged in dedicated columns (`income_imputed`, `credit_history_imputed`) for transparency.

### Accuracy
- **0 exact duplicate rows** found.
- **2 duplicate application IDs** detected (4 rows sharing 2 IDs). Removed 2 duplicate records, keeping the first occurrence of each.
- Final dataset: **500 unique records** across 24 columns.

## Bias Detection & Fairness

The bias analysis (`02-bias-analysis.ipynb`) investigates disparate impact across gender and age, proxy discrimination via ZIP code, interaction effects, and rejection reason patterns.

### Gender bias — disparate impact

Gender values were standardized in the data quality pipeline (`M`/`F` mapped to `Male`/`Female`). Records with missing or invalid gender are excluded from binary comparisons.

- Approval rate (Male): **66.0%**
- Approval rate (Female): **50.6%**
- Disparate impact ratio (Female vs Male): **0.767**
- Demographic parity difference (Female - Male): **-15.4 percentage points**

A DI ratio of 0.767 is below the 0.80 four-fifths-rule threshold, indicating potential disparate impact against female applicants. A chi-square test confirms this is statistically significant (chi-sq = 11.51, p = 0.0007). Among approved loans, average interest rates are similar across genders, but females receive lower average approved amounts (46,669 vs 48,963), suggesting disparity extends beyond the approval decision.

### Confounder-controlled analysis

A logistic regression controlling for income, credit history months, debt-to-income ratio, and savings balance shows that **gender remains a significant predictor of approval** (coefficient = -0.339). This indicates the gender gap is not fully explained by financial differences and points to direct or indirect discrimination in the lending process.

### Age-based approval patterns

Applicants are grouped into three age bands based on date of birth (reference year 2024). Only 4 records (0.8%) have missing age after cleaning.

| Age Group | Approval Rate | DI vs 30-50 |
|-----------|--------------|-------------|
| <30 | 41.0% | 0.629 |
| 30-50 | 65.2% | (reference) |
| 50+ | 58.1% | 1.121 |

The <30 group faces a DI of 0.629 against the 30-50 reference group — well below the 0.80 threshold. A chi-square test confirms statistical significance (chi-sq = 20.07, p < 0.0001). Among approved loans, younger applicants receive smaller loan amounts (43,896 vs 48,461 for 30-50).

### Age x Gender interaction

| Age Group | Female | Male | Gap (M - F) |
|-----------|--------|------|-------------|
| <30 | 30.6% | 52.7% | 22.1 pp |
| 30-50 | 58.9% | 71.1% | 12.2 pp |
| 50+ | 52.2% | 64.1% | 11.9 pp |

Women under 30 face a double disadvantage with the lowest approval rate in the dataset (30.6%). The gender gap is largest for the <30 group (22.1 pp), indicating that fairness interventions should target specific subgroups rather than applying uniform corrections.

### Proxy discrimination — ZIP code

Using Cramer's V to measure association between categorical variables:

| Variable Pair | Cramer's V | Interpretation |
|---------------|-----------|----------------|
| ZIP vs Gender | **0.627** | Strong association |
| ZIP vs Age Group | 0.12 | Weak association |
| Gender vs Age Group | ~0.00 | No association |

ZIP code is strongly correlated with gender (V = 0.627), meaning a model using ZIP could reproduce gender disparities even if the gender field is removed. ZIP should be removed or coarsened (e.g., to broader regions) before model training.

### Rejection reason patterns
- `algorithm_risk_score` is the dominant rejection reason across all groups.
- Rejection reasons do **not** differ significantly by gender (chi-sq = 2.58, p = 0.46).
- Rejection reasons **do** differ significantly by age group (chi-sq = 13.09, p = 0.04).
- Opaque algorithm-based rejections are a governance concern under GDPR Art. 22, which requires meaningful information about automated decision-making logic.

## Governance Recommendations

### Governance Overview
This section evaluates the dataset and credit scoring model from a governance and regulatory compliance perspective. The main objective is to identify and analyse PII (Personal Identifiable Information), assess GDPR compliance, classify the system under the EU AI Act, and propose governance controls.

### Identification of Personal Data (PII)

Under Article 4 of the GDPR, personal data means "any information relating to an identified or identifiable natural person." The dataset contains the following PII:

**Direct identifiers** (high re-identification risk):
- `full_name` — directly reveals the identity of the individual.
- `email` — a unique contact identifier linked to a specific person.
- `ssn` (Social Security Number) — a unique national identification number that unequivocally identifies an individual.

These fields require strict protection including access control and lawful processing under Art. 6 GDPR.

**Quasi-identifiers** (re-identification risk when combined):
- `ip_address`
- `date_of_birth`
- `zip_code`

These relate to identifiable individuals when processed in combination, falling under the scope of GDPR.

**Sensitive behavioral data:**
- `spending_behavior` — reveals patterns about financial habits and lifestyle, which can be used to infer protected characteristics (e.g., religion, health status). Under GDPR, behavioral data carrying inferential risk should be treated with the same caution as traditional PII.

| Field | PII Type | Risk Level |
|---|---|---|
| `full_name` | Direct identifier | High |
| `email` | Direct identifier | High |
| `ssn` | Sensitive identifier | Critical |
| `ip_address` | Quasi-identifier | Medium |
| `date_of_birth` | Quasi-identifier | Medium |
| `zip_code` | Quasi-identifier | Low |
| `spending_behavior` | Sensitive behavioral data | Medium-High |

### Pseudonymization Measures
Pseudonymization reduces the risk of re-identification while maintaining data utility. The SSN field is pseudonymized using SHA-256 hashing — original values are replaced with irreversible hashed representations, preventing direct identification while preserving uniqueness for analytical consistency. The original SSN column is then dropped from the dataset. See `03-privacy-demo.ipynb` for the full demonstration.

### GDPR Provisions
The use of personal data in credit scoring must be assessed against key GDPR provisions:

- **Article 5 (Data Minimisation & Storage Limitation)**: Only data strictly necessary for credit risk assessment should be processed. SSN should not be retained beyond identity verification; direct identifiers like `full_name` may not be required for model training. Storage must be limited to what is necessary — no retention policy is currently defined.
- **Article 6 (Lawfulness of Processing)**: Processing for credit scoring relies on contractual necessity and legitimate interest, requiring that the organization's interests do not override the data subject's fundamental rights.
- **Article 17 (Right to Erasure)**: Under certain conditions, users can request deletion of their personal data. No erasure mechanism was demonstrated in the current pipeline.
- **Article 22 (Automated Decision-Making)**: Directly restricts purely automated decision-making that produces significant legal effects — which credit scoring clearly does. NovaCred must either obtain explicit consent, rely on contractual necessity, or implement suitable safeguards. The current dataset contains **no field tracking whether consent was collected** — this is a compliance gap that must be addressed before deployment.

### EU AI Act Reference
Under Annex III, point 5(b) of the EU AI Act, AI systems used for credit scoring are classified as **High-Risk AI systems**. This imposes compliance obligations including robust data governance and quality control, human oversight measures, a documented risk management system, and transparency requirements. The fairness metrics computed in `02-bias-analysis.ipynb` (Disparate Impact ratio, Demographic Parity difference) are directly relevant — high-risk systems must demonstrate they do not produce discriminatory outcomes across protected groups. These findings should be reviewed as part of any conformity assessment.

### Proposed Governance Controls

1. **Audit Trail**: Every model decision should be automatically logged with a timestamp, the input features used, and the output decision. This allows NovaCred to explain any decisions to customers or auditing services, creating a traceable history.
2. **Human Oversight**: Borderline cases (e.g., applicants near the approval threshold) should be flagged for manual review instead of receiving a fully automated decision, as required by the EU AI Act and GDPR Art. 22.
3. **Consent and Transparency**: Applicants must be clearly informed that an algorithm will evaluate their application and give explicit consent. The current dataset contains no consent tracking field — this compliance gap must be addressed before deployment.
4. **Retention and Data Lifecycle Policy**: NovaCred must define a maximum retention period (e.g., 5 years), after which all PII fields must be deleted or fully anonymized, as required by the Storage Limitation Principle (Art. 5).

## Repository Structure
```
dego-project-team14/
├── README.md                          # Project overview & findings summary
├── data/
│   ├── raw_credit_applications.json   # Original dataset (502 records)
│   └── cleaned_credit_applications.csv # Cleaned dataset (500 records)
├── notebooks/
│   ├── 01-data-quality.ipynb          # Data quality audit & remediation
│   ├── 02-bias-analysis.ipynb         # Bias detection & fairness analysis
│   └── 03-privacy-demo.ipynb          # PII identification & pseudonymization
├── src/
│   └── __init__.py
└── presentation/
    ├── DEGO_Group_14_Final_Report.pptx
    └── Project_Tracking.md
```
---

## How to Run

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scipy fairlearn scikit-learn
```

### Execution Order
Run the notebooks sequentially — each builds on the output of the previous one:

1. **`01-data-quality.ipynb`** — Loads `raw_credit_applications.json`, performs quality audit, exports `cleaned_credit_applications.csv`
2. **`02-bias-analysis.ipynb`** — Loads the cleaned CSV, computes fairness metrics and bias analysis
3. **`03-privacy-demo.ipynb`** — Loads the cleaned CSV, identifies PII, demonstrates pseudonymization

## Individual Contributions

| Team Member | Role | Key Contributions |
|---|---|---|
| **Lenn Schneidewind** | Data Engineer | Data loading and JSON flattening pipeline, data quality analysis across all four dimensions (completeness, consistency, validity, accuracy), data cleaning and imputation strategy, export of cleaned dataset for downstream analysis |
| **Fatima Zubair** | Data Scientist | Gender and age bias analysis with disparate impact ratios, chi-square significance tests, Fairlearn MetricFrame integration, Cramer's V proxy correlation analysis, age x gender interaction effects, logistic regression confounder analysis, rejection reason analysis |
| **Eduarda Dionisio** | Governance Officer | PII identification and classification, SHA-256 pseudonymization demonstration, GDPR article mapping (Art. 5, 6, 17, 22), EU AI Act high-risk classification, governance controls proposal, privacy notebook development |
| **Leon Schmidt** | Product Lead | Repository setup and management, README documentation, project tracking and coordination, PR reviews and branch merges, presentation preparation, code review and bug fixes across all notebooks |
