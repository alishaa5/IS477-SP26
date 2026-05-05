"""
merge.py — Integrate the three cleaned datasets into one merged CSV.
Outputs data/merged/merged_dataset.csv.
"""

import os
import pandas as pd

CLEANED_DIR = os.path.join("data", "cleaned")
MERGED_DIR  = os.path.join("data", "merged")
os.makedirs(MERGED_DIR, exist_ok=True)

def main():
    print("=== merge.py: integrating cleaned datasets ===\n")

    scorecard   = pd.read_csv(os.path.join(CLEANED_DIR, "scorecard_clean.csv"),   low_memory=False)
    ipeds_chars = pd.read_csv(os.path.join(CLEANED_DIR, "ipeds_chars_clean.csv"), low_memory=False)
    ipeds_aid   = pd.read_csv(os.path.join(CLEANED_DIR, "ipeds_aid_clean.csv"),   low_memory=False)

    # unitid is string
    for df in (scorecard, ipeds_chars, ipeds_aid):
        df["UNITID"] = df["UNITID"].astype(str).str.strip()

    print(f"  Scorecard rows:       {len(scorecard):,}")
    print(f"  IPEDS chars rows:     {len(ipeds_chars):,}")
    print(f"  IPEDS aid rows:       {len(ipeds_aid):,}")

    # left join
    # with complete outcome data).
    merged = scorecard.merge(ipeds_chars, on="UNITID", how="left")
    merged = merged.merge(ipeds_aid,   on="UNITID", how="left")

    
    chars_matched = merged["CNTLAFFI"].notna().sum() if "CNTLAFFI" in merged.columns else 0
    aid_matched   = merged["FLOAN_A"].notna().sum()  if "FLOAN_A"  in merged.columns else 0
    print(f"\n  Merged rows:          {len(merged):,}")
    print(f"  Columns:              {merged.shape[1]}")
    print(f"  IPEDS chars matched:  {chars_matched:,} / {len(merged):,}")
    print(f"  IPEDS aid matched:    {aid_matched:,} / {len(merged):,}")

    out_path = os.path.join(MERGED_DIR, "merged_dataset.csv")
    merged.to_csv(out_path, index=False)
    print(f"\n  Saved → {out_path}")

    print("\n=== merge.py complete ===")


if __name__ == "__main__":
    main()
