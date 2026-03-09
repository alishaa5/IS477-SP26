# Project Plan  
**Alisha Agrawal and Archana Nanthikattu**  
IS 477  

## Overview

The goal of this project is to analyze the relationship between college tuition costs and post-graduation career outcomes for students in the United States. Higher education is one of the largest financial investments individuals make, yet many students make enrollment decisions with limited information about whether higher tuition actually leads to better financial outcomes after graduation. While some institutions charge significantly higher tuition, it is not always clear whether those institutions produce graduates with higher earnings or stronger long-term financial outcomes. Understanding the relationship between tuition costs, student debt, and graduate earnings can help students make more informed decisions about where and what to study.

This project will investigate whether institutions with higher tuition costs tend to produce graduates with higher median earnings after graduation and whether this relationship varies across different institutions. In addition, the project will explore how student debt levels relate to post-graduate earnings and whether certain institutions appear to provide stronger financial outcomes relative to tuition costs. The goal is not only to examine tuition and earnings separately, but to analyze the broader financial return on investment (ROI) associated with different colleges.

To accomplish this, we will integrate multiple datasets that contain information about institutional characteristics, tuition costs, student financial aid, student debt, and post-graduation earnings. These datasets will be merged using the **UNITID identifier**, which uniquely identifies institutions across federal higher education datasets.

The project workflow will involve several steps. First, we will collect and inspect the datasets to understand their structure and relevant variables. Next, we will clean the data by addressing missing values, formatting issues, and inconsistencies across datasets. After cleaning, we will integrate the datasets using Python and the pandas library to create a combined dataset that links tuition, institutional characteristics, financial aid, and graduate outcomes.

Once the integrated dataset is prepared, we will conduct exploratory data analysis to identify patterns and relationships between tuition costs, student debt, and graduate earnings. We will calculate derived metrics such as tuition-to-earnings ratios and other indicators that approximate financial return on investment. Visualizations such as scatter plots, distributions, and comparative charts will be used to better understand trends across institutions.

The final outcome of this project will be an integrated dataset, a set of visualizations, and an analytical report that provides insights into how tuition costs relate to post-graduate career outcomes. Ultimately, the analysis aims to provide a clearer picture of whether higher education costs correspond with stronger financial outcomes for graduates.

## Team

This project is being completed by two team members, and responsibilities will be shared while also assigning primary ownership of specific tasks.

### Archana Nanthikattu
Primary responsibilities include data cleaning, dataset integration, and exploratory data analysis. Archana will focus on merging datasets using the UNITID identifier and ensuring that variables related to tuition, student debt, and earnings are properly aligned across sources. She will also contribute to generating visualizations and performing statistical analysis to explore relationships between tuition and graduate outcomes.

### Alisha Agrawal
Primary responsibilities include dataset preparation, variable selection, and documentation of the data processing pipeline. Alisha will focus on identifying relevant variables within each dataset, helping structure the combined dataset, and assisting with exploratory analysis. She will also contribute to writing documentation and interpreting the results of the analysis.

### Shared Responsibilities
Both team members will collaborate on developing the research questions, interpreting results, creating visualizations, and writing the final report. Both members will contribute commits to the GitHub repository and collaborate on updating the project plan and documentation as the project evolves.

## Research / Business Questions

The main goal of this project is to evaluate the financial outcomes associated with attending different colleges in the United States. The project will focus on answering the following questions:

1. **Is there a relationship between tuition cost and median earnings after graduation?**  
   This question examines whether students who attend higher-tuition institutions tend to earn higher salaries after graduation compared to students who attend lower-cost institutions.

2. **How does student debt relate to post-graduate earnings?**  
   This question explores whether institutions with higher student debt levels produce graduates with higher earnings that justify that debt.

3. **Do certain types of institutions provide stronger financial outcomes relative to tuition costs?**  
   This question evaluates whether certain institutions appear to provide stronger financial return on investment when comparing tuition costs to graduate earnings.

4. **How do institutional characteristics influence tuition and graduate outcomes?**  
   By incorporating institutional information such as public vs private classification and geographic location, we can explore whether institutional type influences financial outcomes for students.

These questions are directly answerable using the selected datasets because they contain variables related to tuition, financial aid, student debt, institutional characteristics, and post-graduate earnings.

## Datasets

This project uses three publicly available datasets from federal education sources. These datasets complement each other and can be integrated using the **UNITID identifier**, which uniquely identifies each higher education institution.

### Dataset 1: College Scorecard Data
Source: https://collegescorecard.ed.gov/data

The College Scorecard dataset is maintained by the U.S. Department of Education and contains information about college costs, student debt, and post-graduation earnings. This dataset includes key variables such as:

- Institution name  
- In-state tuition  
- Out-of-state tuition  
- Median student debt  
- Median earnings after graduation  
- Public vs private institution classification  

This dataset is central to the project because it contains the variables directly related to graduate earnings and student debt outcomes. It also includes the **UNITID variable**, which allows it to be linked with IPEDS datasets.

### Dataset 2: IPEDS Institutional Characteristics
Source: https://nces.ed.gov/ipeds/datacenter/

The Integrated Postsecondary Education Data System (IPEDS) Institutional Characteristics dataset provides structural information about colleges and universities. Key variables include:

- Institution name  
- Institution type  
- Location (city, state, ZIP code)  
- Institutional classification  
- Administrative and institutional identifiers  

This dataset provides contextual information about each institution that can help interpret differences in tuition costs and outcomes.

### Dataset 3: IPEDS Student Financial Aid Data
Source: https://nces.ed.gov/ipeds/datacenter/

The IPEDS Student Financial Aid dataset provides information about financial aid distribution, tuition pricing, and net price calculations for students. Variables include:

- Net price for students by income category  
- Financial aid distributions  
- Tuition and fee structures  
- Grant and scholarship information  

This dataset helps provide deeper insight into the financial burden experienced by students and complements the tuition and debt information found in the College Scorecard dataset.

### Dataset Integration

All three datasets share the **UNITID identifier**, which uniquely identifies each institution. This shared identifier allows the datasets to be merged together to create a comprehensive dataset that includes tuition, institutional characteristics, financial aid, student debt, and graduate earnings.

Because these datasets come from official government sources, they have clear documentation, consistent identifiers, and reliable data provenance.

## Timeline

During Week 1 we will review the datasets and their documentation to understand the available variables and dataset structures. Archana will focus on cleaning the datasets by handling missing values and standardizing formats while both team members inspect the documentation.

During Week 2 the datasets will be integrated using the UNITID identifier. Archana will primarily handle the merging process while Alisha will focus on identifying and selecting the variables that will be used in the analysis.

During Week 3 we will conduct exploratory data analysis and generate visualizations that show relationships between tuition, student debt, and graduate earnings.

During Week 4 both team members will interpret the results and prepare the final report and documentation for the project.

This timeline may evolve as we progress through the project and identify additional analytical opportunities.

## Constraints

There are several potential challenges associated with this project.

One limitation is that datasets may contain missing or incomplete data for certain institutions or variables. Some colleges may not report certain financial or earnings information, which could limit the number of institutions included in the final analysis.

Another challenge involves differences in how variables are measured across datasets. Even though the datasets share the UNITID identifier, variable definitions and reporting methods may differ, which may require additional cleaning and normalization before the datasets can be merged.

Additionally, the datasets represent aggregate institutional data rather than individual student-level data. As a result, our analysis can identify general trends but cannot capture individual variation among students.

There may also be limitations related to time coverage. Some datasets may represent different reporting years, which could introduce inconsistencies if not properly aligned.

Finally, while these datasets provide strong indicators of financial outcomes, they cannot fully capture non-financial benefits of higher education such as career mobility, personal development, or job satisfaction.


## Gaps

There are several areas where additional input or exploration may be required.

First, we may need to identify the most relevant earnings and debt variables within the College Scorecard dataset, as it contains many related variables with slightly different definitions.

Second, we may need to determine the most meaningful way to measure return on investment (ROI). This could involve creating new derived metrics such as tuition-to-earnings ratios or comparing debt levels with median graduate earnings.

Third, additional filtering may be required to ensure that the institutions included in the analysis have complete and comparable data across all datasets.

Finally, as we progress through the project, we may identify additional variables or datasets that could strengthen the analysis. The project plan may evolve as we gain a deeper understanding of the data and analytical possibilities.
