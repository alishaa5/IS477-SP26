Status Report
Project Overview and Current Progress

For this milestone, our main focus was building a clean and usable dataset that we can actually analyze later. The project is centered around understanding relationships between college cost, student debt, earnings after graduation, and financial aid. To do this, we worked with multiple datasets and combined them into one main dataset that we will use moving forward.

So far, we have successfully loaded, cleaned, and merged three datasets. These include the College Scorecard dataset, the IPEDS characteristics dataset, and the IPEDS financial aid dataset. Using pandas in Python, we selected only the most relevant columns from each dataset so we are not working with unnecessary data. Some of the key variables we kept include tuition for in state and out of state students, median debt, median earnings ten years after enrollment, and indicators for financial aid.

After selecting the columns, we focused on cleaning the data. One issue we ran into was that some values were labeled as “PrivacySuppressed,” which cannot be used for analysis. We replaced those values with missing values so they would not interfere with calculations. We also converted important columns into numeric format because they were originally read as text. This step was important so that we can later perform calculations and comparisons. We then removed rows that were missing key financial variables to make sure the dataset is more reliable.

Next, we standardized the UNITID column across all datasets by converting it into a string format. This was necessary because UNITID is the main key used to merge the datasets together. Once everything was consistent, we merged the datasets using left joins so that we kept as much data as possible from the main dataset.

Finally, we exported the merged dataset as a file called merged_dataset.csv. This file now serves as the foundation for the rest of our project. Overall, this step was important because it turned raw and messy data into something structured and ready to analyze.

Tasks Completed and Artifacts

We have made solid progress on the main tasks from our project plan. First, we completed the data acquisition step by identifying and loading all three datasets. These datasets are stored in the repository and can be accessed directly for reproducibility.

Second, we completed the data cleaning process. This includes handling missing values, converting data types, and removing unreliable rows. The script used for this step is included in the repository and documents exactly how the cleaning was done.

Third, we completed the data integration step. We merged all datasets into one final dataset using a shared key. The output file merged_dataset.csv is included in the repository and represents the main artifact for this milestone.

In terms of artifacts, the repository currently includes the raw datasets, the Python script used for cleaning and merging, and the final merged dataset. These files show the full workflow from raw data to cleaned data.

Updated Timeline

We are currently on track with our original timeline, but we made a few small adjustments based on how long certain steps actually took. Data cleaning took longer than expected because we had to carefully handle missing and inconsistent values.

At this point, data acquisition, cleaning, and merging are fully completed. The next step is exploratory data analysis, which we plan to start immediately. This will include looking at distributions, identifying trends, and creating visualizations.

After that, we will move into deeper analysis where we examine relationships between variables like tuition and earnings or financial aid and debt. Finally, we will work on summarizing our findings and preparing the final deliverables.

Overall, we are slightly behind our original estimate for cleaning, but we adjusted the timeline and are still in a good position to complete everything on time.

Changes to Project Plan

There were a few changes to our original project plan. Initially, we planned to keep more variables from each dataset, but after reviewing the data, we realized that focusing on fewer, more meaningful variables would make the analysis clearer and more manageable.

We also decided to remove rows with missing key financial values instead of trying to impute them. This decision was made to avoid introducing bias or incorrect assumptions into the dataset.

Another change was how we approached merging. At first, we considered using inner joins, but we switched to left joins so that we would not lose too much data from the main dataset.

These changes helped improve the overall quality of the dataset and made our workflow more efficient.

Challenges and How We Addressed Them

One of the biggest challenges we faced was dealing with missing and suppressed data. The “PrivacySuppressed” values made it difficult to work with certain variables. We solved this by converting those values into missing values and then removing rows where key variables were missing.

Another challenge was inconsistent data types across datasets. Some numeric columns were read as strings, which caused issues during cleaning. We fixed this by explicitly converting those columns into numeric format and handling any errors that came up.

Merging the datasets was also a challenge at first because the UNITID column was not in the same format across all files. Once we standardized it as a string, the merging process worked correctly.

Overall, these challenges slowed us down at first, but they helped us better understand the data and improve the quality of our final dataset.

Individual Contributions

Archana worked on the data cleaning and merging process. This included writing the Python script, selecting relevant columns, handling missing values, and creating the final merged dataset. Archana also ensured that the dataset is structured correctly for future analysis.

Alisha worked on data acquisition and initial exploration. This included identifying the datasets, understanding what each variable represents, and helping decide which columns should be included in the final dataset. Alisha also reviewed the merged dataset to make sure everything looked correct.

Both team members contributed to discussing challenges and making decisions about how to clean and merge the data. All contributions are reflected in the Git commit history.

Next Steps

The next step is to begin exploratory data analysis. We will start by creating summary statistics and visualizations to better understand the data. After that, we will look for patterns and relationships between variables such as tuition, debt, earnings, and financial aid.

We will also begin thinking about how to present our findings in a clear and meaningful way for the final project. This includes deciding what visualizations to include and how to explain our results.

Overall, we have built a strong foundation with our cleaned dataset, and we are ready to move into the analysis phase.
