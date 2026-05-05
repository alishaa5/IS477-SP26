# College Tuition and Post-Graduation Outcomes: Analyzing the Financial Return on Higher Education

## Contributors

- Alisha Agrawal (University of Illinois Urbana-Champaign, IS 477, Spring 2026)
- Archana Nanthikattu (University of Illinois Urbana-Champaign, IS 477, Spring 2026)

## Summary

Higher education is one of the largest financial investments that individuals make in their lifetimes, yet many students make enrollment decisions with limited information about whether higher tuition actually translates to better financial outcomes after graduation. This project investigates the relationship between college tuition costs and post-graduation career outcomes for institutions across the United States.

The central research questions guiding this project are: whether there is a relationship between tuition cost and median earnings after graduation, how student debt relates to post-graduate earnings, whether certain types of institutions provide stronger financial outcomes relative to tuition costs, and how institutional characteristics such as public versus private classification influence graduate financial outcomes.

To answer these questions, we integrated three complementary federal datasets: the U.S. Department of Education College Scorecard, the IPEDS Institutional Characteristics file, and the IPEDS Student Financial Aid file. All three datasets were linked using the shared UNITID identifier that uniquely identifies each institution.

Our workflow proceeds through five stages: data acquisition via acquire.py, data cleaning via clean.py, dataset integration via merge.py, analysis and visualization via analyze.py, and end-to-end automation via a Snakemake workflow. All stages are fully reproducible from a single command.

Key findings indicate that private nonprofit institutions tend to produce graduates with higher median earnings than public or for-profit institutions. The data also shows that most institutions fall above the line where earnings equal debt, meaning graduates generally earn more than their total debt within ten years. However, a cluster of for-profit institutions shows unfavorable debt-to-earnings ratios. These patterns suggest that institution type is a more reliable predictor of financial outcomes than tuition cost alone.

## Data Profile

### Dataset 1: College Scorecard

Source: https://collegescorecard.ed.gov/data/

The College Scorecard dataset is maintained by the U.S. Department of Education and contains institution-level information about college costs, student debt, and post-graduation earnings. The file used is the most recent cohort release from March 2026. It is stored in the data/raw/ folder after being downloaded by acquire.py. Key variables used in this project include UNITID as the institution identifier, INSTNM for institution name, STABBR for state, CONTROL for institution type (public, private nonprofit, or private for-profit), ICLEVEL for institution level (4-year, 2-year, or less-than-2-year), TUITIONFEE_IN and TUITIONFEE_OUT for tuition costs, DEBT_MDN for median student debt at graduation, and MD_EARN_WNE_P10 for median earnings ten years after enrollment.

This dataset is publicly available from a federal government source and contains no personally identifiable information. All values are institution-level aggregates. Some values are suppressed for privacy when the underlying student population is too small to report without risking re-identification. These are reported as the string "PrivacySuppressed" and were treated as missing values in our analysis.

### Dataset 2: IPEDS Institutional Characteristics (HD2023)

Source: https://nces.ed.gov/ipeds/datacenter/data/HD2023.zip

The IPEDS Institutional Characteristics dataset is maintained by the National Center for Education Statistics and provides structural and geographic information about colleges and universities. It is stored in data/raw/ after extraction. Key variables used include UNITID, INSTNM, CITY, STABBR, CONTROL, and ICLEVEL. This dataset provides authoritative institutional classification that helps interpret variation in tuition and earnings across different types of schools. It is publicly released federal data with no restrictions beyond proper citation.

### Dataset 3: IPEDS Student Financial Aid (SFA2223)

Source: https://nces.ed.gov/ipeds/datacenter/data/SFA2223.zip

The IPEDS Student Financial Aid dataset covers the 2022-23 academic year and contains information about financial aid distribution and federal loan amounts at each institution. It is stored in data/raw/ after extraction. The key variable used is UNITID for joining and FLOAN_A for total federal loan dollars distributed, which was used as a proxy for federal aid availability. This dataset is also publicly released federal data with no use restrictions beyond citation.

### Integration

All three datasets share the UNITID variable, which is the federal standard identifier for postsecondary institutions and is consistent across all Department of Education and NCES data products. The College Scorecard served as the primary table, and the IPEDS datasets were joined to it using left joins on UNITID after standardizing the column to string type across all three sources. The integrated dataset is saved at data/merged/merged_dataset.csv.

## Data Quality

Data quality assessment was performed across all three datasets before integration. The most significant issue was the presence of "PrivacySuppressed" values in the College Scorecard, which appeared in key numeric columns including tuition, debt, and earnings. These values could not be used in calculations and were converted to missing values before any numeric operations.

A second issue was that key financial columns were read as object type by pandas due to the presence of these suppressed strings. This required explicit conversion to numeric format after handling the suppressed values.

A third issue involved the UNITID column, which was stored as integer in some files and string in others. This caused silent merge failures where the join would complete but produce no matched rows. Standardizing UNITID to string type across all datasets resolved this.

After loading, no duplicate UNITID values were found within any individual dataset. After merging and filtering for rows with complete values in the core financial variables, the working analysis dataset is a subset of the full merged table. Some institutions do not report all financial variables, so coverage is incomplete but the retained rows are reliable.

## Data Cleaning

Data cleaning is implemented in clean.py and runs on the raw CSV files produced by acquire.py. The first operation was replacing all instances of "PrivacySuppressed" with NaN so that those cells would not interfere with numeric calculations. The second operation was converting the tuition, debt, and earnings columns from object to float using pd.to_numeric with errors set to coerce, which turns any remaining non-numeric values into NaN. The third operation was casting UNITID to string in each dataset before merging to ensure consistent join behavior. The fourth operation was selecting only the columns relevant to our research questions from each dataset to keep the merged file manageable. The fifth operation was dropping rows that were missing values in the core financial variables after merging, so that only institutions with reasonably complete financial profiles were included in the analysis. Imputation was considered but rejected to avoid making assumptions about why those values were missing.

## Findings

Earnings by institution type: Private nonprofit institutions have the highest median earnings ten years post-enrollment, followed by public institutions, with private for-profit institutions showing the lowest median earnings. This is shown in results/figures/earnings_by_control.png.

Student debt versus earnings: Most institutions fall above the line where earnings equal debt, meaning that graduates at most schools earn more than their total debt by the ten-year mark. However, a cluster of private for-profit institutions falls at or below this line, indicating that their graduates carry debt comparable to or exceeding their annual earnings. This is shown in results/figures/debt_vs_earnings.png.

Tuition by institution level: Four-year institutions show much higher and more variable in-state tuition than two-year institutions. Two-year institutions are considerably more affordable and show tighter distributions. This is shown in results/figures/tuition_distribution.png.

Federal aid and earnings: Institutions where federal loan dollars are distributed to students are associated with modestly higher median earnings compared to institutions with no federal loan activity. This is shown in results/figures/aid_vs_earnings.png.

The top ten institutions by median earnings are mostly selective private nonprofit universities and specialized professional schools. The bottom ten are predominantly for-profit certificate and associate programs. These tables are saved at results/tables/top10_earnings.csv and results/tables/bottom10_earnings.csv. Summary statistics for all key variables are in results/tables/summary_statistics.csv.

## Future Work

One direction for future work would be a longitudinal analysis tracking how tuition-to-earnings ratios have changed over time for the same institutions. The current analysis uses a single snapshot and cannot capture trends.

A second direction would be incorporating field of study data. The College Scorecard provides earnings broken down by major, which would allow comparisons like engineering versus humanities at the same institution and would be more actionable for students choosing what to study.

A third direction would be using net price instead of published tuition. Net price after financial aid gives a more accurate picture of what students actually pay. The IPEDS Financial Aid dataset contains net price by income category, which could be incorporated in a more detailed model.

A fourth direction would be addressing selection effects. Our analysis identifies correlations but cannot establish causation. Students at high-earning schools may have had better outcomes regardless of where they enrolled due to pre-existing socioeconomic advantages. Future work could attempt to address this through methods that control for selectivity.

A fifth direction would be adding geographic visualizations such as state-level maps to reveal regional patterns in the financial return on higher education.

## Challenges

The most significant challenge was the "PrivacySuppressed" placeholder in the College Scorecard. Because it appeared in numeric columns, pandas read those columns as object type, which silently prevented any numeric computation. Diagnosing this required carefully inspecting column types and unique values.

A second challenge was the UNITID type mismatch across datasets. The merge would complete without errors but produce no matching rows because integer and string versions of the same ID were not treated as equal. Discovering this required checking the shape of intermediate join results.

A third challenge was inconsistent column naming across the IPEDS files, including differences in capitalization and trailing whitespace, which required normalizing column names before selection.

A fourth challenge was the size of the College Scorecard CSV, which contains several thousand columns. Loading the full file caused memory issues during development and required using usecols to load only the necessary columns.

A fifth challenge was the temporal misalignment across datasets. The three datasets come from slightly different survey years, which introduces minor inconsistencies when combining variables from different collection cycles.

## Reproducing

To reproduce the complete workflow from data acquisition through results, follow these steps.

First, clone the repository and navigate into it:

    git clone https://github.com/alishaa5/IS477-SP26.git
    cd IS477-SP26

Second, install the required dependencies:

    pip install -r requirements.txt

Third, run the full automated workflow using Snakemake:

    snakemake --cores 1

This will execute acquire.py, then clean.py, then merge.py, then analyze.py in the correct order. All outputs will be placed in data/ and results/.

Alternatively, the scripts can be run manually in order:

    python acquire.py
    python clean.py
    python merge.py
    python analyze.py

The acquire.py script downloads raw data directly from the College Scorecard and NCES servers, so internet access is required for that step. Expected outputs include the raw ZIP and CSV files in data/raw/, the merged dataset at data/merged/merged_dataset.csv, four figures in results/figures/, and three tables in results/tables/.

## References

U.S. Department of Education. College Scorecard Institution-Level Data, Most Recent Cohorts (March 2026). https://collegescorecard.ed.gov/data/. Accessed May 2026.

National Center for Education Statistics. IPEDS Institutional Characteristics Survey, 2023 (HD2023). https://nces.ed.gov/ipeds/datacenter/data/HD2023.zip. Accessed May 2026.

National Center for Education Statistics. IPEDS Student Financial Aid and Net Price Survey, 2022-23 (SFA2223). https://nces.ed.gov/ipeds/datacenter/data/SFA2223.zip. Accessed May 2026.

McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference, 51-56. https://pandas.pydata.org/

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science and Engineering, 9(3), 90-95. https://matplotlib.org/

Mölder, F., et al. (2021). Sustainable data analysis with Snakemake. F1000Research, 10, 33. https://snakemake.readthedocs.io/

Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585, 357-362. https://numpy.org/

## Contribution Statement

Archana Nanthikattu was primarily responsible for data cleaning, dataset merging, and the clean.py and merge.py scripts. Archana also wrote the initial drafts of the data quality and data cleaning sections of this report.

Alisha Agrawal was primarily responsible for data acquisition, variable selection, the acquire.py script, the analyze.py visualization script, and report writing. Alisha also coordinated the Snakemake workflow and final documentation.

Both team members contributed to research question development, result interpretation, and review of all written sections. Individual contributions are evidenced in the Git commit history.
