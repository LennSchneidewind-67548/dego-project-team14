# Project Tracking — Team 14

---

## Milestone Checklist

### Setup
- [x] GitHub repo created and public
- [x] All 4 members added and onboarded
- [x] Folder structure created (`data/`, `notebooks/`, `src/`, `presentation/`)
- [x] Dataset added to `data/`
- [ ] All Members commited their name to README.md

### Analysis

#### 01-data-engineer.ipynb
- [ ] Load and parse nested JSON into flat DataFrame
- [ ] Identify and count duplicate records
- [ ] Identify inconsistent data types (e.g. income stored as string)
- [ ] Identify missing / null values — per-column % missing
- [ ] Identify inconsistent categorical coding (e.g. gender as `M` / `Male` / `male`)
- [ ] Identify invalid / impossible values (e.g. negative credit history months)
- [ ] Identify inconsistent date formats
- [ ] Quantify every issue: count + % of affected records
- [ ] Demonstrate remediation steps in code
- [ ] Notebook runs clean (restart kernel → run all)

#### 02-data-scientist.ipynb
- [ ] Calculate gender approval rates (female vs. male)
- [ ] Calculate Disparate Impact ratio — `DI = approval_rate(female) / approval_rate(male)`
- [ ] Interpret DI against four-fifths rule (threshold: 0.8)
- [ ] Analyse age-based approval patterns
- [ ] Proxy discrimination analysis — correlate `zip_code` and `spending_behavior` with protected attributes
- [ ] Investigate interaction effects (e.g. age × gender)
- [ ] Visualizations for all bias patterns
- [ ] Notebook runs clean (restart kernel → run all)

#### 03-governance-officer.ipynb
- [ ] Identify all PII fields: `full_name`, `email`, `ssn`, `ip_address`, `date_of_birth`, `zip_code`
- [ ] Demonstrate pseudonymization of ≥1 PII field (e.g. SHA-256 hash of `ssn`)
- [ ] Map findings to GDPR: Art. 6 (lawful basis), Art. 5 (minimization + storage limitation), Art. 17 (erasure)
- [ ] Reference EU AI Act — credit scoring as high-risk (Annex III)
- [ ] Propose concrete governance controls (audit trail, human oversight, consent, retention policy)
- [ ] Notebook runs clean (restart kernel → run all)

#### src/fairness_utils.py
- [ ] DI ratio function extracted and importable
- [ ] Demographic parity difference function extracted
- [ ] Functions used/imported inside `02-data-scientist.ipynb`

### README
- [ ] Team members filled in (all 4 names + student IDs)
- [ ] Executive summary written
- [ ] Data quality table filled in with real numbers
- [ ] Bias section filled in (DI ratio value + interpretation)
- [ ] Privacy table filled in (action taken column)
- [ ] Governance recommendations written (≥3 concrete ones)
- [ ] Individual contributions filled in

### Video
- [ ] All 4 members recorded and speaking
- [ ] Duration checked (target: 5:45, max: 6:00, penalty at 7:00+)
- [ ] Key visualizations shown
- [ ] Specific numbers cited (DI ratio, duplicate count, etc.)
- [ ] Uploaded (YouTube unlisted / Google Drive) and link added to README

### Final Submission
- [ ] All notebooks run clean (restart kernel → run all)
- [ ] ≥10 meaningful commits, all 4 members have commits
- [ ] Repo is public
- [ ] Moodle submission done (GitHub URL)
- [ ] Deadline: 23:59 day before Session 6

### After Session 6
- [ ] Peer evaluation submitted on Moodle (within 48h)

---
