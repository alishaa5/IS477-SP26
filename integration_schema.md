# Integration Schema

## Project: College Tuition and Post-Graduation Outcomes
## File: integration_schema.md

This document describes the conceptual data model and integration schema used to combine the three federal datasets in this project.

---

## Entity-Relationship Overview

All three datasets are linked using the UNITID variable, which is the federal standard unique identifier for postsecondary institutions assigned by the U.S. Department of Education. Every institution that participates in federal student aid programs has a stable UNITID that is consistent across all NCES and Department of Education data products.

```
+----------------------------------+
|       College Scorecard          |
|----------------------------------|
| UNITID (PK, string)              |
| INSTNM                           |
| STABBR                           |
| CONTROL                          |
| ICLEVEL                          |
| TUITIONFEE_IN                    |
| TUITIONFEE_OUT                   |
| DEBT_MDN                         |
| MD_EARN_WNE_P10                  |
+----------------------------------+
          |
          | UNITID (left join)
          |
          v
+----------------------------------+       +----------------------------------+
|  IPEDS Institutional             |       |  IPEDS Student Financial Aid     |
|  Characteristics (HD2023)        |       |  (SFA2223)                       |
|----------------------------------|       |----------------------------------|
| UNITID (FK, string)              |       | UNITID (FK, string)              |
| CNTLAFFI                         |       | CONTROL                          |
| CALSYS                           |       | LOCALE                           |
| OPENADMP                         |       | INSTSIZE                         |
|                                  |       | HBCU                             |
|                                  |       | LANDGRNT                         |
+----------------------------------+       +----------------------------------+
          |                                          |
          +------------------+-----------------------+
                             |
                             v
              +----------------------------------+
              |     Merged Dataset               |
              |  data/merged/merged_dataset.csv  |
              |----------------------------------|
              | One row per institution          |
              | Variables from all three sources |
              | Linked via UNITID                |
              +----------------------------------+
```

---

## Integration Strategy

### Join Type
Left join on UNITID with the College Scorecard as the anchor (left) table. Left joins were chosen to retain all institutions in the Scorecard even if they do not appear in every IPEDS file.

### Key Standardization
Before merging, UNITID was standardized to string type in all three datasets using astype(str). This was necessary because the College Scorecard encodes UNITID as integer while the IPEDS files encode it as string, causing silent merge failures if not standardized.

### Merge Order
1. College Scorecard (anchor) LEFT JOIN IPEDS Characteristics on UNITID
2. Result LEFT JOIN IPEDS Financial Aid on UNITID

### Output
The merged dataset is saved at data/merged/merged_dataset.csv and contains one row per institution with variables drawn from all three sources.

---

## Integration Query (Equivalent SQL)

The merge operation implemented in merge.py is equivalent to the following SQL query:

```sql
SELECT
    s.UNITID,
    s.INSTNM,
    s.STABBR,
    s.CONTROL,
    s.ICLEVEL,
    s.TUITIONFEE_IN,
    s.TUITIONFEE_OUT,
    s.DEBT_MDN,
    s.MD_EARN_WNE_P10,
    c.CNTLAFFI,
    c.CALSYS,
    c.OPENADMP,
    a.LOCALE,
    a.INSTSIZE,
    a.HBCU,
    a.LANDGRNT
FROM scorecard_clean s
LEFT JOIN ipeds_chars_clean c
    ON CAST(s.UNITID AS VARCHAR) = CAST(c.UNITID AS VARCHAR)
LEFT JOIN ipeds_aid_clean a
    ON CAST(s.UNITID AS VARCHAR) = CAST(a.UNITID AS VARCHAR);
```

---

## Data Sources and Temporal Coverage

| Dataset | Source | Survey Period | Row Count (approx) |
|---|---|---|---|
| College Scorecard | U.S. Dept of Education | Most recent cohort, March 2026 | ~6,500 institutions |
| IPEDS HD2023 | NCES | 2023 survey cycle | ~6,500 institutions |
| IPEDS SFA2223 | NCES | 2022-23 academic year | ~6,000 institutions |
| Merged Dataset | This project | Mixed (see above) | ~3,500 after filtering |

---

## Notes on Temporal Misalignment

The three datasets come from slightly different survey years. The College Scorecard uses the most recent cohort release from March 2026, the IPEDS Characteristics file uses the 2023 survey cycle, and the IPEDS Financial Aid file covers 2022-23. UNITID matching ensures institutions are correctly aligned across sources despite this temporal misalignment, but variables from different years may not perfectly reflect the same point in time.
