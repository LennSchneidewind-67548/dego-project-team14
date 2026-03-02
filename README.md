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

We normalize `applicant_info.gender` into a cleaned `gender_clean` field with the categories `Male` and `Female` (mapping `M`→`Male` and `F`→`Female`, keeping other values as is). Records with missing or invalid gender remain in the dataset but are excluded when we need a clear binary comparison.

- Approval rate (Male): **65.7%**
- Approval rate (Female): **50.6%**
- Disparate impact ratio (Female vs Male): **0.77**
- Demographic parity difference (Female − Male): **−15.1 percentage points**

A disparate impact ratio of 0.77 (female approval rate divided by male approval rate) is below the 0.80 four‑fifths‑rule threshold, indicating potential disparate impact against female applicants that requires governance attention.[file:1] The demographic parity gap of roughly −15 percentage points reinforces that women are materially less likely to be approved than men. Among approved loans, average interest rates and approved amounts are similar for male and female borrowers, so the main fairness concern is the **probability of approval**, not pricing differences among those who are approved.

### Age‑based approval patterns

To analyze age, we convert `applicant_info.date_of_birth` to a proper datetime and compute approximate age at application. Invalid or missing dates are set to `NaT`, and the corresponding ages are `NaN`; these records are excluded from age‑band comparisons but are documented as a data‑quality limitation (about **32%** of records), since missing age can hide or distort evidence of age‑related bias.[file:1]

We group applicants into three age bands with the following approval rates:

- **<30**: **39.7%**
- **30–50**: **62.3%**
- **50+**: **61.9%**

Treating applicants **<30** as the unprivileged group, the disparate impact ratios for <30 vs 30–50 and <30 vs 50+ are both well below 0.8, signalling a strong age‑related disparity that warrants governance attention.[file:1] In contrast, 30–50 and 50+ have very similar approval rates. For approved loans only, average interest rates and approved amounts are broadly comparable across age bands, so—as with gender—the key issue is who gets approved rather than how approved customers are treated. We recommend complementing this with multivariate analysis (e.g., including age, income, credit‑history months, and debt‑to‑income) to test whether the penalty for younger applicants persists after controlling for financial risk factors.

### Proxy discrimination – ZIP code as a proxy for gender

We investigate whether `zip_code` can act as a proxy for gender. Aggregating applications by ZIP and `gender_clean` shows that, in the filtered sample of ZIPs with at least 5 applications, **none** of the ZIP codes contain both male and female applicants; all 15 ZIPs are effectively single‑gender, with a “purity” of 1.0 (for example, ZIP 10004 has 6 male and 0 female applications). This means that even if the explicit gender field is removed from the model, a classifier using ZIP could still infer gender with very high confidence and reproduce gender disparities while appearing neutral.[file:1]

For this reason, ZIP should be treated as a **high‑risk feature**: its use should be strongly justified, potentially coarsened (e.g., to broader regions), and monitored with additional fairness checks to prevent indirect discrimination.


## Governance Recommendations
### Governance Overview
This section evaluates the dataset and credit scoring model from a governance and regulatory compliance perspective.
The main objective is to identify and analyse the PII (Personal Identifiable Information), assess GDPR compliance, classify the system under the EU AI Act and propose governance controls.

### Identification of the Data
Identification of Personal Data (PII) Under the Article 4 of the GDPR, personal data means “any information relating to an identified or identifiable natural person (the data subject)”, directly or indirectly. These identifiers have one or more factors related with physical, cultural, economic or social identity of a (natural) person.  Based on this definition, the dataset used for the credit score analysis contains some attributes that are considered as Personal Identifiable Information. 

Direct identifiers enable to identify an individual immediately such as:
- full_name - that directly reveals the identity of the individual.
- email - a unique contact identifier linked to a specific person.
- ssn (social security number) - a unique national identification number that unequivocally identifies an individual in a whole national system.
These fields present a high identification risk and require strict protection of the data, including access, control and lawful processing, according to Art. 6 of GDPR.

Indirect identifiers includes attributes that may not identify a person directly or independently, just combined with other data. In this case, the attributes are quasi-identifiers that significantly increases (re-)identification risk when combined with other attributes such as demographic data. For example:
- ip_address
- date_of_birth
- zip_code
Even though these fields are not always uniquely identifying on their own, they relate to identifiable individuals when processed in combination, under the scope of GDPR.

### Pseudonymization Measures
Pseudonymization refers to the processing of personal data in such a way that it can no longer be attributed to a specific data subject without the use of additional information. Pseudonymization reduces the risk of (re-)identification while maintaining data utility for analytical purposes. In this case, sensitive identifiers such as the Social Security Number (SSN) are pseudonymized using an encrypted hashing function (e.g., SHA-256). The original SSN values are replaced with hashed representations, thereby preventing direct identification while preserving uniqueness for analytical consistency. Also, this is a one-way measure, it means that, it is not possible to reverse the hash back to the ssn without the original value.

### GDPR Provisions
The use of personal data in credit scoring must be assessed based on the key GDPR provisions:
- The Article 5 (Principles Relating of Processing of Personal Data) establishes core data protection principle - data minimization. This implies that only data strictly necessary for the credit risk assessment are going to be processed ( e.g., ssn should not be retained beyond identity verification purposes and direct identifiers such as name may not be relevant (and required) for model training. Also, the Article 5 limits the storage of the data only for as long as necessary (e.g., duration of data storage or periodic review of stored datasets).
- The Article 6 (Lawfulness of Processing) means that processing personal data (for credit scoring) relies on contractual necessity and legitimate interest, requiring an evaluation of the application prior to entering into a contract and demonstrating that the organization’s interests do not override the fundamental rights and freedoms of the data subject, respectively. In our case, analysing the credit score is a legitimate interest and is a contractual necessity.
- The Article 17 (Right to Erasure or Right to “be forgotten”) indicate that, under certain conditions, users can request to delete their personal data (backups included). In our project, no erasure mechanism was demonstrated in the pipeline.

### EU AI Act Reference
Under Annex III of the EU AI Act, AI systems used for credit scoring and evaluation of creditworthiness are classified as High-Risk AI systems. This classification imposes substantial compliance obligations on providers and deployers, e.g., a robust data governance and quality control, human oversight measures a documented risk management system or transparency and user information requirements. The fairness metrics computed in 02-data-scientist.ipynb (Disparate Impact ratio and Demographic Parity) are directly relevant. Under the EU AI Act, high-risk systems must demonstrate they do not produce discriminatory outcomes across protected groups (gender, age). Those findings should be reviewed as part of any conformity assessment.

### Proposed Governance Controls
In the case of NovaCred, since it works high-risk personal data and its processing for a credit application, these are the suggested governance controls to ensure regulatory compliance, accountability and ethical use: 
- Audit Trail: Every decision model should be automatically logged with a timestamp, the input features that were used and the output decision (if it was rejected or not). This allows NovaCred to explain any decisions, for customers or for auditing services, creating a traceable history.
- Human oversight: In borderline cases (e.g., applicants with credit score right at the approval threshold) should be manually reviewed instead of receiving a fully automated decision. This is required, by EU AI Act and GDPR (Article 22), to protect individuals from purely algorithmic decisions that significantly affects them.
- Consent and Transparency: Applicants must be clearly informed that an algorithm will evaluate their application and give explicit consent, before processing their data through an automated system. This is only lawful, under certain conditions, including the data subject’s consent.
- Retention and Data Lifecycle Policy: NovaCred must define a maximum retention period (e.g., 5 years), after which all PII fields must be deleted or fully anonymized. This is required by the Storage Limitation Principle (Article 5) that, as previously said, prohibits keeping personal information longer than necessary for its original purpose.

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
