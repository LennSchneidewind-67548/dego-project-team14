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


### Gender bias – disparate impact

The gender bias analysis normalizes the raw gender field into consistent Male and Female categories, excluding ambiguous values from binary comparisons, and then compares approval rates across these groups. Female applicants exhibit a substantially lower loan approval rate (approximately 51% versus 66% for males), a disparate impact ratio of about 0.77 (below the 0.80 four‑fifths rule), and a demographic parity gap of roughly −15 percentage points, indicating potential disparate impact against women that warrants mitigation and ongoing monitoring.

### Age-based approval patterns

The age bias analysis groups applicants into three age bands: <30, 30–50, and 50+, and compares approval rates across these segments. Applicants under 30 have a markedly lower approval rate (around 40% versus about 62% for both 30–50 and 50+), leading to a disparate impact ratio (younger vs. 30–50 group) well below the 0.80 four‑fifths rule threshold, which signals a potential age‑related disparity that should be addressed through appropriate governance and monitoring.

Age-related bias analysis relies on a cleaned age variable derived from applicant_info.date_of_birth, which is converted to a proper datetime type and used to compute approximate applicant ages. Invalid or missing dates are mapped to NaT (and thus NaN ages), resulting in about 32% of records being excluded from age‑group approval rate calculations; this substantial proportion of missing age information is documented as a data‑quality limitation, as it can obscure or distort evidence of age‑related bias if not explicitly acknowledged.

### Proxy discrimination – ZIP code as a proxy for gender

The ZIP code bias analysis shows that ZIP behaves as a strong proxy for gender rather than a neutral geographic feature. In the filtered sample (ZIPs with at least 5 applications), none of the ZIP codes contained both male and female applicants; all 15 ZIP codes were effectively single‑gender, with a “purity” of 1.0 (for example, ZIP 10004 has 6 male and 0 female applications). As a result, a model using ZIP as an input could infer gender with very high confidence and reproduce gender disparities even if the explicit gender variable were removed, so ZIP should be treated as a high‑risk feature whose use requires strong justification, possible coarsening (e.g., to broader regions), and close monitoring for indirect discrimination.


## Governance Recommendations
### Governance Overview
This section evaluates the dataset and credit scoring model from a governance and regulatory compliance perspective.
The main objetive is to identify and analyse the PII (Personal Identifiable Information), assess GDPR compliance, classify the system under the EU AI Act and propose governance controls.

### Identification of the Data
Identification of Personal Data (PII) Under the Article 4 of the GDPR, personal data is means “any informations relating to an identified or identifiable natural person (the data subject)”, directly or indirectly. These identifiers has one or more factors related with physical, cultural, economic or social identity of a (natural) person.  Based on this definition, the dataset used for the credit score analysis contains some attributes that are considered as Personal Identifiable Information. 

Direct identifiers enable to identify an individual immediately such as:
- full_name - that directly reveals the identity of the individual.
- email - a unique contact identifier linked to a specific person.
- ssn (social security number) - a unique national identification number that unequivocally identifies an individual in a whole national system.
These fields present a high identification risk and require strict protection of the data, including acess, control and lawful processing, according to Art. 6 of GDPR.

Indirect identifiers includes attributes that may not identify a person directly or indepently, just combined with other data. In this case, the attributes are quasi-identifiers that significantly increases (re-)identification risk when combined with other attributes such as demographic data. For example:
- ip_adress
- date_of_birth
- zip_code
Even tough these fields are not always uniquely identifying on their own, they relate to identifiable individuals when processed in combination, under the scope of GDPR.

### Pseudonymization Measures
Pseudonymization refers to the processing of personal data in such a way that it can no longer be attributed to a specific data subject without the use of additional information. Pseudonymization reduces the risk of (re-)identification while maintaining data utility for analytical purposes. In this case, sensitive identifiers such as the Social Security Number (SSN) are pseudonymized using a encrypted hashing function (e.g., SHA-256). The original SSN values are replaced with hashed representations, thereby preventing direct identification while preserving uniqueness for analytical consistency. Also, this is a one-way measure, it means that, it is not possible to reverse the hash back to the ssn without the original value.

### GDPR Provisions
The use of personal data in credit scoring must be assessed based on the key GDPR provisions:
- The Article 5 (Principles Relating of Processing of Personal Data) establishes core data protection principle - data minimization. This implies that only data strictly necessary for the credit risk assessment are going to be processed ( e.g., ssn should not be retained beyond identity verification purposes and direct identifiers such as name may not be relevant (and required) for model training. Also, the Article 5 limits the storage of tha data only for as long as necessary (e.g., duration of data storage or periodic review of stored datasets).
- The Article 6 (Lawfulness of Processing) means that processing personal data (for credit scoring) relies on contractural necessity and legitimate interest, requiring a elavuate of the application prior to entering into a contract and demonstrating that the organization’s interests do not overrida the fundamental rights and freedoms of the data subject, respectively. In our case, analysing the credit score is a legimate interest and is a contractual necessity.
- The Article 17 (Right to Erasure or Right to “be forgotten”) indicate that, under certain conditions, users can request to delete their personal data (backups included). In our project, no erasure mechanism was demonstrated in the pipeline.

### EU AI Act Reference
Under Annex III of the EU AI Act, AI systems used for credit scoring and evaluation of creditworthiness are classified as High-Risk AI systems. This classification imposes substantial compliance obligations on providers and deployers, e.g., a robust data governance and quality control, human oversight measures a documented risk management system or transparency and user information requirements. The fairness metrics computed in 02-data-scientist.ipynb (Disparate Impact ratio and Demographic Parity) are directly relevant. Under the EU AI Act, high-risk systems must demonstrate they do not produce discriminatory outcomes across protected groups (gender, age). Those findings should be reviewed as part of any conformity assessment.

### Proposed Governance Controls
In the case of NovaCred, since it works high-risk personal data and its processing for a credit application, these are the suggested governance controls to ensure regulatory complicance, accountability and ethical use: 
- Audit Trail: Every decision model should be automatically logged with a timestamp, the input features that were used and the output decision (if it was rejected or not). This allows NovaCred to explain any decisions, for customers or for auditory services, creating a traceable history.
- Human oversight: In borderline cases (e.g., applicants with credit score right at the approval threshold) should be manually reviewed instead of receiving a fully automated decision. This is required, by EU AI Act and GDPR (Article 22), to protect individuals from purely algorithmic decisions that significantly affects them.
- Consent and Transparency: Applicants must be clearly informed that an algorithm will evaluate their application and give explicit consent, before processing their data through an automated system. This is only lawful, under certain conditions, including the data subject’s consent.
- Retention and Data Lifecyle Policy: NovaCred must define a maximum retention period (e.g., 5 years), after which all PII fields must be deleted or fully anonymized. This is required by the Storage Limitation Principle (Article 5) that, as previously said, prohibits keeping personal information longer than necessary for its original purpose.

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
