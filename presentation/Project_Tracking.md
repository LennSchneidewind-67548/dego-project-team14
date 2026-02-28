# Project Tracking — Team 14

---

## Milestone Checklist

### Setup
- [x] GitHub repo created and public
- [x] All 4 members added and onboarded
- [x] Folder structure created (`data/`, `notebooks/`, `src/`, `presentation/`)
- [x] Dataset added to `data/`
- [x] Team members filled in README.md (all 4 names + student IDs)

### Analysis

#### 01-data-quality.ipynb -> Finish until 24.02.26 Afternoon
- [x] Load and parse nested JSON into flat DataFrame
- [x] Identify and count duplicate records
- [x] Identify inconsistent data types (e.g. income stored as string)
- [x] Identify missing / null values — per-column % missing
- [x] Identify inconsistent categorical coding (e.g. gender as `M` / `Male` / `male`)
- [x] Identify invalid / impossible values (e.g. negative credit history months)
- [x] Identify inconsistent date formats
- [x] Quantify every issue: count + % of affected records
- [x] Demonstrate remediation steps in code
- [x] Notebook runs clean (restart kernel → run all)

#### 02-bias-analysis.ipynb -> Finish until 27.02.26
- [x] Calculate gender approval rates (female vs. male)
- [x] Calculate Disparate Impact ratio — `DI = approval_rate(female) / approval_rate(male)`
- [x] Interpret DI against four-fifths rule (threshold: 0.8)
- [ ] Analyse age-based approval patterns — also compute DI for 50+ vs 30–50 (currently only <30 vs 30–50)
- [ ] Proxy discrimination analysis — correlate `zip_code` and `spending_behavior` with protected attributes; use Cramér's V instead of count-based observation
- [ ] Investigate interaction effects (e.g. age × gender) — add cross-tabulation and interaction plot
- [ ] Visualisations for all bias patterns — add 0.8 four-fifths reference line, interaction plot, proxy correlation heatmap
- [ ] Load cleaned dataset from Lenn (`cleaned_credit_applications.csv`) instead of raw JSON
- [ ] Remove redundant gender cleaning code — drop `M`→`Male` / `F`→`Female` normalisation (already done in data-quality notebook)
- [ ] Add statistical test — chi-squared test (and/or fairlearn / AIF360) to back up DI findings
- [ ] Extend outcome metrics — analyse interest rates and approved amounts by gender and age group, not just approval rates
- [ ] Strengthen interpretations — discuss confounders (income, debt-to-income) and suggest concrete mitigation steps (reweighting, threshold adjustment, feature removal)
- [ ] Notebook runs clean (restart kernel → run all)

#### 03-privacy-demo.ipynb -> Finish until 27.02.26
- [ ] Identify all PII fields: `full_name`, `email`, `ssn`, `ip_address`, `date_of_birth`, `zip_code`
- [ ] Demonstrate pseudonymization of ≥1 PII field (e.g. SHA-256 hash of `ssn`)
- [ ] Map findings to GDPR: Art. 6 (lawful basis), Art. 5 (minimization + storage limitation), Art. 17 (erasure)
- [ ] Reference EU AI Act — credit scoring as high-risk (Annex III)
- [ ] Propose concrete governance controls (audit trail, human oversight, consent, retention policy)
- [ ] Notebook runs clean (restart kernel → run all)

#### src/fairness_utils.py (optional -> Probably won't be needed in our implementation)
- [ ] DI ratio function extracted and importable
- [ ] Demographic parity difference function extracted
- [ ] Functions used/imported inside `02-data-scientist.ipynb`

### README -> Finish till 28.02.2026
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
