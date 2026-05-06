# Data Dictionary

## Project: College Tuition and Post-Graduation Outcomes
## File: data/merged/merged_dataset.csv

This data dictionary describes all variables in the merged dataset produced by merge.py.
The merged dataset integrates three federal data sources linked by the UNITID identifier.

---

## Source 1: College Scorecard (Most Recent Cohorts, March 2026)
Source URL: https://collegescorecard.ed.gov/data/

| Variable | Type | Description | Values / Units |
|---|---|---|---|
| UNITID | String | Unique institution identifier assigned by the U.S. Department of Education. Primary join key across all three datasets. | Integer encoded as string |
| INSTNM | String | Full name of the postsecondary institution. | Text |
| STABBR | String | Two-letter postal abbreviation for the state where the institution is located. | e.g., IL, CA, NY |
| CONTROL | Integer | Institution control type indicating ownership and governance. | 1 = Public, 2 = Private Nonprofit, 3 = Private For-Profit |
| ICLEVEL | Integer | Highest level of award or degree offered by the institution. | 1 = 4-year, 2 = 2-year, 3 = Less-than-2-year |
| TUITIONFEE_IN | Float | Published in-state tuition and required fees for the most recent academic year available. Does not reflect financial aid. | US Dollars |
| TUITIONFEE_OUT | Float | Published out-of-state tuition and required fees for the most recent academic year available. Does not reflect financial aid. | US Dollars |
| DEBT_MDN | Float | Median cumulative federal loan debt at the time of graduation or program completion among students who received federal aid and completed a program. | US Dollars |
| MD_EARN_WNE_P10 | Float | Median annual earnings of students who were working and not enrolled in further education 10 years after initial enrollment. Derived from federal tax records matched to student aid records. | US Dollars |

### Notes on Missing Values (College Scorecard)
Values reported as "PrivacySuppressed" in the original source indicate that the underlying student count was below the minimum reporting threshold required to protect student privacy. These values were converted to NaN (missing) during data cleaning. Institutions with suppressed values in TUITIONFEE_IN, DEBT_MDN, or MD_EARN_WNE_P10 were excluded from the final analysis dataset.

---

## Source 2: IPEDS Institutional Characteristics Survey 2023 (HD2023)
Source URL: https://nces.ed.gov/ipeds/datacenter/data/HD2023.zip

| Variable | Type | Description | Values / Units |
|---|---|---|---|
| UNITID | String | Unique institution identifier. Join key. | Integer encoded as string |
| INSTNM | String | Full institution name as reported in the IPEDS survey. | Text |
| CITY | String | City where the institution's main campus is located. | Text |
| STABBR | String | Two-letter state abbreviation. | e.g., IL, CA, NY |
| CONTROL | Integer | Institution control type. | 1 = Public, 2 = Private Nonprofit, 3 = Private For-Profit |
| ICLEVEL | Integer | Institution level based on highest award offered. | 1 = 4-year, 2 = 2-year, 3 = Less-than-2-year |

### Notes
CONTROL and ICLEVEL from this source serve as a cross-reference to the College Scorecard values. In cases of minor discrepancy due to differences in collection timing, the Scorecard values are used in the analysis.

---

## Source 3: IPEDS Student Financial Aid Survey 2022-23 (SFA2223)
Source URL: https://nces.ed.gov/ipeds/datacenter/data/SFA2223.zip

| Variable | Type | Description | Values / Units |
|---|---|---|---|
| UNITID | String | Unique institution identifier. Join key. | Integer encoded as string |
| FLOAN_A | Float | Total dollar amount of federal loans distributed to all students at the institution during the 2022-23 academic year. Used as a proxy for whether the institution actively participates in federal financial aid programs and the scale of student borrowing. | US Dollars |

---

## Derived / Computed Variables

No additional derived variables were created in the merged dataset. All analysis computations (e.g., ratios, group means) are performed within analyze.py and are not stored back into the merged dataset file.

---

## File Encoding and Format

- File format: CSV (comma-separated values)
- Character encoding: UTF-8
- Header row: Yes, first row
- Missing values: Represented as empty cells (NaN in pandas)
- Location in repository: data/merged/merged_dataset.csv

---

## Ethical and Legal Constraints

All three source datasets are publicly released by U.S. federal government agencies and are in the public domain under U.S. government open data policy. No personally identifiable information is included in any dataset. All values are institution-level aggregates. Privacy suppression has been applied by the original data producers to protect individual student privacy before public release. No additional consent or licensing is required to use or redistribute these datasets beyond proper citation.
