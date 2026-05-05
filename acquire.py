"""
acquire.py — Download all raw datasets programmatically.

Sources:
  - College Scorecard: https://collegescorecard.ed.gov/data/
  - IPEDS: https://nces.ed.gov/ipeds/use-the-data
"""

import os
import sys
import hashlib
import requests
import zipfile
import io


RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# dataset registry
DATASETS = [
    (
        
        "https://ed-public-download.scorecard.network/downloads/Most-Recent-Cohorts-Institution_03232026.zip",
        "scorecard.zip",
        None,  
    ),
    (
        
        "https://nces.ed.gov/ipeds/datacenter/data/HD2023.zip",
        "ipeds_characteristics.zip",
        None,
    ),
    (
    
        "https://nces.ed.gov/ipeds/datacenter/data/SFA2223.zip",
        "ipeds_financial_aid.zip",
        None,
    ),
]

# helpers

def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: str) -> None:
    print(f"  Downloading {url}")
    resp = requests.get(url, stream=True, timeout=120)
    resp.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"  Saved → {dest}  (sha256: {sha256(dest)})")


def extract_csv_from_zip(zip_path: str, out_dir: str, target_stem: str) -> str:
    """Extract the first CSV whose name contains target_stem (case-insensitive)."""
    with zipfile.ZipFile(zip_path) as zf:
        candidates = [n for n in zf.namelist()
                      if n.lower().endswith(".csv") and target_stem.lower() in n.lower()]
        if not candidates:
            # fall back: first CSV in archive
            candidates = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not candidates:
            raise FileNotFoundError(f"No CSV found in {zip_path}")
        chosen = candidates[0]
        out_path = os.path.join(out_dir, os.path.basename(chosen))
        with zf.open(chosen) as src, open(out_path, "wb") as dst:
            dst.write(src.read())
        print(f"  Extracted {chosen} → {out_path}")
        return out_path


# mai

def main():
    print("=== acquire.py: downloading raw datasets ===\n")

    zip_meta = [
        ("scorecard.zip",           "MERGED"),          
        ("ipeds_characteristics.zip", "hd2023"),
        ("ipeds_financial_aid.zip",   "sfa2223"),
    ]

    for (url, filename, expected_sha), (_, stem) in zip(DATASETS, zip_meta):
        zip_path = os.path.join(RAW_DIR, filename)

        # download if not already present
        if not os.path.exists(zip_path):
            download(url, zip_path)
        else:
            print(f"  Already present: {zip_path}  (sha256: {sha256(zip_path)})")

        # integrity check
        if expected_sha and sha256(zip_path) != expected_sha:
            print(f"  WARNING: sha256 mismatch for {filename}!", file=sys.stderr)

        # extract 
        extract_csv_from_zip(zip_path, RAW_DIR, stem)

    print("\n=== acquire.py complete ===")


if __name__ == "__main__":
    main()
