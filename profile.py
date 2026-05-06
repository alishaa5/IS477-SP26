"""
profile.py — Data quality profiling for all three raw datasets.

This script assesses the quality of the raw datasets before any cleaning
is applied. It reports on shape, data types, missing values, suppressed
values, duplicate records, and basic summary statistics for key numeric
columns. Run this script after acquire.py and before clean.py.

Usage:
    python profile.py
"""

import os
import sys
import glob
import pandas as pd
import numpy as np

RAW_DIR = os.path.join("data", "raw")
PROFILE_DIR = os.path.join("results", "profile")
os.makedirs(PROFILE_DIR, exist_ok=True)

NUMERIC_COLS = ["TUITIONFEE_IN", "TUITIONFEE_OUT", "DEBT_MDN", "MD_EARN_WNE_P10"]


# helpers

def find_csv(directory: str, stem: str) -> str:
    pattern = os.path.join(directory, "*.csv")
    matches = [p for p in glob.glob(pattern)
               if stem.lower() in os.path.basename(p).lower()]
    if not matches:
        raise FileNotFoundError(
            f"No CSV containing '{stem}' found in {directory}. "
            "Run acquire.py first."
        )
    return matches[0]


def profile_dataset(name: str, path: str, numeric_cols: list = None) -> dict:
    print(f"\n{'='*60}")
    print(f"  Profiling: {name}")
    print(f"  File: {path}")
    print(f"{'='*60}")

    df = pd.read_csv(path, low_memory=False)

    print(f"\n  Shape: {df.shape[0]} rows x {df.shape[1]} columns")

    # data types
    type_counts = df.dtypes.value_counts()
    print(f"\n  Column data types:")
    for dtype, count in type_counts.items():
        print(f"    {dtype}: {count} columns")

    # missing values
    total_cells = df.shape[0] * df.shape[1]
    missing = df.isnull().sum().sum()
    print(f"\n  Missing values: {missing} ({100*missing/total_cells:.2f}% of all cells)")

    # columns with most missing
    missing_by_col = df.isnull().sum()
    top_missing = missing_by_col[missing_by_col > 0].sort_values(ascending=False).head(10)
    if len(top_missing) > 0:
        print(f"\n  Top columns with missing values:")
        for col, count in top_missing.items():
            pct = 100 * count / df.shape[0]
            print(f"    {col}: {count} missing ({pct:.1f}%)")

    # privacy suppressed values (College Scorecard specific)
    suppressed_counts = {}
    for col in df.columns:
        if df[col].dtype == object:
            n = (df[col] == "PrivacySuppressed").sum()
            if n > 0:
                suppressed_counts[col] = n

    if suppressed_counts:
        total_suppressed = sum(suppressed_counts.values())
        print(f"\n  PrivacySuppressed values found: {total_suppressed} total across {len(suppressed_counts)} columns")
        # show top affected columns
        top_suppressed = sorted(suppressed_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"  Top columns with suppressed values:")
        for col, count in top_suppressed:
            pct = 100 * count / df.shape[0]
            print(f"    {col}: {count} suppressed ({pct:.1f}%)")
    else:
        print(f"\n  No PrivacySuppressed values found.")

    # duplicate UNITID check
    if "UNITID" in df.columns:
        dupes = df["UNITID"].duplicated().sum()
        print(f"\n  Duplicate UNITID values: {dupes}")
        print(f"  Unique UNITID values: {df['UNITID'].nunique()}")
        print(f"  UNITID dtype: {df['UNITID'].dtype}")

    # numeric summary for key columns
    if numeric_cols:
        available = [c for c in numeric_cols if c in df.columns]
        if available:
            print(f"\n  Numeric summary (after treating PrivacySuppressed as NaN):")
            temp = df[available].replace("PrivacySuppressed", np.nan)
            for col in available:
                temp[col] = pd.to_numeric(temp[col], errors="coerce")
            summary = temp.describe().T
            print(summary.to_string())

    result = {
        "name": name,
        "rows": df.shape[0],
        "cols": df.shape[1],
        "missing_cells": int(missing),
        "missing_pct": round(100 * missing / total_cells, 2),
        "suppressed_cols": len(suppressed_counts),
        "total_suppressed": sum(suppressed_counts.values()) if suppressed_counts else 0,
        "duplicate_unitids": int(df["UNITID"].duplicated().sum()) if "UNITID" in df.columns else None,
    }

    return result


def main():
    print("=== profile.py: data quality profiling ===")
    print(f"Looking for raw CSVs in: {RAW_DIR}\n")

    if not os.path.exists(RAW_DIR):
        print(f"ERROR: {RAW_DIR} does not exist. Run acquire.py first.", file=sys.stderr)
        sys.exit(1)

    datasets = [
        ("College Scorecard", "Most-Recent-Cohorts-Institution", NUMERIC_COLS),
        ("IPEDS Institutional Characteristics (HD2023)", "hd2023", []),
        ("IPEDS Student Financial Aid (SFA2223)", "sfa2223", []),
    ]

    summaries = []
    for name, stem, num_cols in datasets:
        try:
            path = find_csv(RAW_DIR, stem)
            result = profile_dataset(name, path, num_cols)
            summaries.append(result)
        except FileNotFoundError as e:
            print(f"\n  WARNING: {e}", file=sys.stderr)
            continue

    # write summary report
    if summaries:
        summary_df = pd.DataFrame(summaries)
        out_path = os.path.join(PROFILE_DIR, "data_quality_report.csv")
        summary_df.to_csv(out_path, index=False)
        print(f"\n\n{'='*60}")
        print(f"  Profile summary saved to: {out_path}")
        print(f"{'='*60}")
        print(summary_df.to_string(index=False))

    print("\n=== profile.py complete ===")


if __name__ == "__main__":
    main()
