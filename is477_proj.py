import pandas as pd

# load all three datasets
scorecard = pd.read_csv("scorecard.csv", low_memory=False)
ipeds_chars = pd.read_csv("ipeds_characteristics.csv", low_memory=False)
ipeds_aid = pd.read_csv("ipeds_financial_aid.csv", low_memory=False)

# select columns

scorecard_cols = [
    "UNITID", "INSTNM", "CITY", "STABBR", "REGION",
    "CONTROL", "ICLEVEL", "TUITIONFEE_IN", "TUITIONFEE_OUT",
    "DEBT_MDN", "MD_EARN_WNE_P10", "LOCALE"
]

ipeds_chars_cols = [
    "UNITID", "CNTLAFFI", "CALSYS", "OPENADMP"
]

ipeds_aid_cols = [
    "UNITID", "FLOAN_A", "FGRNT_A", "ANYAIDP"
]

scorecard = scorecard[scorecard_cols]
ipeds_chars = ipeds_chars[ipeds_chars_cols]
ipeds_aid = ipeds_aid[ipeds_aid_cols]

# cleaning

# replace PrivacySuppressed with NaN
scorecard = scorecard.replace("PrivacySuppressed", pd.NA)

# convert numeric columns
numeric_cols = ["TUITIONFEE_IN", "TUITIONFEE_OUT", "DEBT_MDN", "MD_EARN_WNE_P10"]
scorecard[numeric_cols] = scorecard[numeric_cols].apply(pd.to_numeric, errors="coerce")

# drop rows missing key values
scorecard = scorecard.dropna(subset=numeric_cols)

# standardize UNITID as string for merging
scorecard["UNITID"] = scorecard["UNITID"].astype(str)
ipeds_chars["UNITID"] = ipeds_chars["UNITID"].astype(str)
ipeds_aid["UNITID"] = ipeds_aid["UNITID"].astype(str)

# merging
merged = scorecard.merge(ipeds_chars, on="UNITID", how="left")
merged = merged.merge(ipeds_aid, on="UNITID", how="left")

# save
merged.to_csv("merged_dataset.csv", index=False)

print(f"Rows: {merged.shape[0]}, Columns: {merged.shape[1]}")
print(merged.head())