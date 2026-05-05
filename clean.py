"""
clean.py — Load raw CSVs, select relevant columns, and apply cleaning operations.
Outputs cleaned CSVs to data/cleaned/.
"""

import os
import sys
import glob
import pandas as pd

RAW_DIR     = os.path.join("data", "raw")
CLEANED_DIR = os.path.join("data", "cleaned")
os.makedirs(CLEANED_DIR, exist_ok=True)

# column sections

SCORECARD_COLS = [
    "UNITID", "INSTNM", "CITY", "STABBR", "REGION",
    "CONTROL", "ICLEVEL", "TUITIONFEE_IN", "TUITIONFEE_OUT",
    "DEBT_MDN", "MD_EARN_WNE_P10", "LOCALE",
]

IPEDS_CHARS_COLS = [
    "UNITID", "CNTLAFFI", "CALSYS", "OPENADMP",
]

IPEDS_AID_COLS = [
    "UNITID", "CONTROL", "LOCALE", "INSTSIZE", "HBCU", "LANDGRNT",
]

NUMERIC_COLS = ["TUITIONFEE_IN", "TUITIONFEE_OUT", "DEBT_MDN", "MD_EARN_WNE_P10"]

# helpers

def find_csv(directory: str, stem: str) -> str:
    """Find a CSV in directory whose name contains stem (case-insensitive)."""
    pattern = os.path.join(directory, "*.csv")
    matches = [p for p in glob.glob(pattern) if stem.lower() in os.path.basename(p).lower()]
    if not matches:
        raise FileNotFoundError(
            f"No CSV containing '{stem}' found in {directory}. "
            "Run acquire.py first."
        )
    return matches[0]


def select_available_cols(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Select only columns that actually exist in the dataframe."""
    missing = [c for c in cols if c not in df.columns]
    if missing:
        print(f"  WARNING: columns not found and will be skipped: {missing}", file=sys.stderr)
    available = [c for c in cols if c in df.columns]
    return df[available]

# per dataset clean

def clean_scorecard(path: str) -> pd.DataFrame:
    print(f"  Reading scorecard: {path}")
    df = pd.read_csv(path, low_memory=False)
    print(f"    Raw shape: {df.shape}")

    df = select_available_cols(df, SCORECARD_COLS)

    # replace college nan
    df = df.replace("PrivacySuppressed", pd.NA)


    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # drop rows
    key_cols = [c for c in NUMERIC_COLS if c in df.columns]
    before = len(df)
    df = df.dropna(subset=key_cols)
    print(f"    Dropped {before - len(df)} rows with missing key numeric values.")

    # standardize
    df["UNITID"] = df["UNITID"].astype(str).str.strip()

    # remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset="UNITID")
    print(f"    Dropped {before - len(df)} duplicate UNITID rows.")

    print(f"    Cleaned shape: {df.shape}")
    return df


def clean_ipeds_chars(path: str) -> pd.DataFrame:
    print(f"  Reading IPEDS characteristics: {path}")
    df = pd.read_csv(path, low_memory=False)
    print(f"    Raw shape: {df.shape}")

    df = select_available_cols(df, IPEDS_CHARS_COLS)
    df["UNITID"] = df["UNITID"].astype(str).str.strip()
    df = df.drop_duplicates(subset="UNITID")

    print(f"    Cleaned shape: {df.shape}")
    return df


def clean_ipeds_aid(path: str) -> pd.DataFrame:
    print(f"  Reading IPEDS financial aid: {path}")
    df = pd.read_csv(path, low_memory=False)
    print(f"    Raw shape: {df.shape}")

    df = select_available_cols(df, IPEDS_AID_COLS)
    df["UNITID"] = df["UNITID"].astype(str).str.strip()
    df = df.drop_duplicates(subset="UNITID")

    print(f"    Cleaned shape: {df.shape}")
    return df

# main

def main():
    print("=== clean.py: cleaning raw datasets ===\n")

    scorecard_path   = scorecard_path   = find_csv(RAW_DIR, "Most-Recent-Cohorts-Institution")
    ipeds_chars_path = find_csv(RAW_DIR, "hd2023")
    ipeds_aid_path   = find_csv(RAW_DIR, "sfa2223")

    scorecard   = clean_scorecard(scorecard_path)
    ipeds_chars = clean_ipeds_chars(ipeds_chars_path)
    ipeds_aid   = clean_ipeds_aid(ipeds_aid_path)

    scorecard.to_csv(os.path.join(CLEANED_DIR, "scorecard_clean.csv"), index=False)
    ipeds_chars.to_csv(os.path.join(CLEANED_DIR, "ipeds_chars_clean.csv"), index=False)
    ipeds_aid.to_csv(os.path.join(CLEANED_DIR, "ipeds_aid_clean.csv"), index=False)

    print("\n=== clean.py complete ===")


if __name__ == "__main__":
    main()
