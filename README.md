# DEGO Project - Team 14

## Executive Summary


## Team Members

| Role | Name | Student ID |
|------|------|------------|
| Data Engineer | Lenn Louis Schneidewind | 67548 |
| Data Scientist | | |
| Governance Officer | Eduarda Dionísio | 56503 |
| Product Lead | Leon Werner Schmidt | 71644 |

## Project Description
Credit scoring bias analysis for DEGO course.

## Data Quality Findings


## Bias Detection & Fairness

## Privacy Assessment


## Governance Recommendations
#Identification of Data 
Identification of Personal Data (PII) Under the Article 4 of the GDPR, personal data is means “any informations relating to an identified or identifiable natural person (the data subject)”, directly or indirectly. These identifiers has one or more factors related with physical, cultural, economic or social identity of a (natural) person.  Based on this definition, the dataset used for the credit score analysis contains some attributes that are considered as Personal Identifiable Information. 

Direct Identifiers:
Direct Identifiers enable to identify an individual immediately such as:
- full_name - that directly reveals the identity of the individual;
- email - a unique contact identifier linked to a specific person;
- ssn (social security number) - a unique national identification number that unequivocally  identifies an individual in a whole national system.

Indirect Identifiers:
Indirect identifiers includes attributes that may not identify a person directly or indepently, just combined with other data. In this case, the attributes are quasi-identifiers that significantly increases (re-)identification risk when combined with other attributes such as demographic data. For example:
- ip_adress
- date_of_birth
- zip_code 

Even tough these fields are not always uniquely identifying on their own, they relate to identifiable individuals when processed in combination, under the scope of GDPR. 

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
