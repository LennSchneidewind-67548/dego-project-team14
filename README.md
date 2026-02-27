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

### Gender bias – disparate impact

The gender bias analysis normalizes the raw gender field into consistent Male and Female categories, excluding ambiguous values from binary comparisons, and then compares approval rates across these groups. Female applicants exhibit a substantially lower loan approval rate (approximately 51% versus 66% for males), a disparate impact ratio of about 0.77 (below the 0.80 four‑fifths rule), and a demographic parity gap of roughly −15 percentage points, indicating potential disparate impact against women that warrants mitigation and ongoing monitoring.

### Age-based approval patterns

The age bias analysis groups applicants into three age bands: <30, 30–50, and 50+, and compares approval rates across these segments. Applicants under 30 have a markedly lower approval rate (around 40% versus about 62% for both 30–50 and 50+), leading to a disparate impact ratio (younger vs. 30–50 group) well below the 0.80 four‑fifths rule threshold, which signals a potential age‑related disparity that should be addressed through appropriate governance and monitoring.

Age-related bias analysis relies on a cleaned age variable derived from applicant_info.date_of_birth, which is converted to a proper datetime type and used to compute approximate applicant ages. Invalid or missing dates are mapped to NaT (and thus NaN ages), resulting in about 32% of records being excluded from age‑group approval rate calculations; this substantial proportion of missing age information is documented as a data‑quality limitation, as it can obscure or distort evidence of age‑related bias if not explicitly acknowledged.

### Proxy discrimination – ZIP code as a proxy for gender

The ZIP code bias analysis shows that ZIP behaves as a strong proxy for gender rather than a neutral geographic feature. In the filtered sample (ZIPs with at least 5 applications), none of the ZIP codes contained both male and female applicants; all 15 ZIP codes were effectively single‑gender, with a “purity” of 1.0 (for example, ZIP 10004 has 6 male and 0 female applications). As a result, a model using ZIP as an input could infer gender with very high confidence and reproduce gender disparities even if the explicit gender variable were removed, so ZIP should be treated as a high‑risk feature whose use requires strong justification, possible coarsening (e.g., to broader regions), and close monitoring for indirect discrimination.


## Governance Recommendations
#Proposed Governance Controls
In the case of NovaCred, since it works high-risk personal data and its processing for a credit application, these are the suggested governance controls to ensure regulatory complicance, accountability and ethical use: 

- Audit Trail: Every decision model should be automatically logged with a timestamp, the input features that were used and the output decision (if it was rejected or not). This allows NovaCred to explain any decisions, for customers or for auditory services, creating a traceable history.
- Human oversight: In borderline cases (e.g., applicants with credit score right at the approval threshold) should be manually reviewed instead of receiving a fully automated decision. This is required, by EU AI Act and GDPR (Article 22), to protect individuals from purely algorithmic decisions that significantly affects them.
- Consent and Transparency: Applicants must be clearly informed that an algorithm will evaluate their application and give explicit consent, before processing their data through an automated system. This is only lawful, under certain conditions, including the data subject’s consent.
- Retention and Data Lifecyle Policy: NovaCred must define a maximum retention period (e.g., 5 years), after which all PII fields must be deleted or fully anonymized. This is required by the Storage Limitation Principle (Article 5) that, as previously said, prohibits keeping personal information longer than necessary for its original purpose.

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
