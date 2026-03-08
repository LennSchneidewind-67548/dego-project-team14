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
- [x] Analyse age-based approval patterns — also compute DI for 50+ vs 30–50 (currently only <30 vs 30–50)
- [x] Proxy discrimination analysis — correlate `zip_code` and `spending_behavior` with protected attributes; use Cramér's V instead of count-based observation
- [x] Investigate interaction effects (e.g. age × gender) — add cross-tabulation and interaction plot
- [x] Visualisations for all bias patterns — add 0.8 four-fifths reference line, interaction plot, proxy correlation heatmap
- [x] Load cleaned dataset from Lenn (`cleaned_credit_applications.csv`) instead of raw JSON
- [x] Remove redundant gender cleaning code — drop `M`→`Male` / `F`→`Female` normalisation (already done in data-quality notebook)
- [x] Add statistical test — chi-squared test (and/or fairlearn / AIF360) to back up DI findings
- [x] Extend outcome metrics — analyse interest rates and approved amounts by gender and age group, not just approval rates
- [x] Strengthen interpretations — discuss confounders (income, debt-to-income) and suggest concrete mitigation steps (reweighting, threshold adjustment, feature removal)
- [x] Notebook runs clean (restart kernel → run all)

#### 03-privacy-demo.ipynb -> Finish until 27.02.26
- [x] Identify all PII fields: `full_name`, `email`, `ssn`, `ip_address`, `date_of_birth`, `zip_code`
- [x] Demonstrate pseudonymization of ≥1 PII field (e.g. SHA-256 hash of `ssn`)
- [x] Map findings to GDPR: Art. 6 (lawful basis), Art. 5 (minimization + storage limitation), Art. 17 (erasure)
- [x] Reference EU AI Act — credit scoring as high-risk (Annex III)
- [x] Propose concrete governance controls (audit trail, human oversight, consent, retention policy)
- [x] Notebook runs clean (restart kernel → run all)

### README -> Finish till 28.02.2026
- [x] Executive summary written
- [x] Data quality table filled in with real numbers
- [x] Bias section filled in (DI ratio value + interpretation)
- [x] Privacy table filled in (action taken column)
- [x] Governance recommendations written (≥3 concrete ones)
- [ ] Individual contributions filled in

### Video
- [x] All 4 members recorded and speaking
- [x] Duration checked (target: 5:45, max: 6:00, penalty at 7:00+)
- [x] Key visualizations shown
- [x] Specific numbers cited (DI ratio, duplicate count, etc.)
- [x] Uploaded (YouTube unlisted / Google Drive) and link added to README

### Final Submission
- [x] All notebooks run clean (restart kernel → run all)
- [x] ≥10 meaningful commits, all 4 members have commits
- [x] Repo is public
- [x] Moodle submission done (GitHub URL)
- [x] Deadline: 23:59 day before Session 6

### After Session 6
- [ ] Peer evaluation submitted on Moodle (within 48h)

---
