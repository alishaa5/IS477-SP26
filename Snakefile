# Snakefile — end-to-end pipeline for the College Outcomes project
#
# Usage:
#   snakemake --cores 1          # run full pipeline
#   snakemake --cores 1 --forceall   # re-run everything from scratch
#   snakemake --dag | dot -Tpng > dag.png   # visualise the DAG

# ── Final targets ─────────────────────────────────────────────────────────────
rule all:
    input:
        "results/figures/earnings_by_control.png",
        "results/figures/debt_vs_earnings.png",
        "results/figures/tuition_distribution.png",
        "results/figures/aid_vs_earnings.png",
        "results/tables/summary_statistics.csv",
        "results/tables/top10_earnings.csv",
        "results/tables/bottom10_earnings.csv",

# ── Step 1: Acquire raw data ──────────────────────────────────────────────────
rule acquire:
    output:
        # Snakemake needs concrete file targets; these are the extracted CSVs.
        # acquire.py prints the exact filenames; we match with wildcards below.
        touch("data/raw/.acquire_done")
    log:
        "logs/acquire.log"
    shell:
        "python acquire.py > {log} 2>&1"

# ── Step 2: Clean each dataset ────────────────────────────────────────────────
rule clean:
    input:
        "data/raw/.acquire_done"
    output:
        "data/cleaned/scorecard_clean.csv",
        "data/cleaned/ipeds_chars_clean.csv",
        "data/cleaned/ipeds_aid_clean.csv",
    log:
        "logs/clean.log"
    shell:
        "python clean.py > {log} 2>&1"

# ── Step 3: Merge / integrate datasets ───────────────────────────────────────
rule merge:
    input:
        "data/cleaned/scorecard_clean.csv",
        "data/cleaned/ipeds_chars_clean.csv",
        "data/cleaned/ipeds_aid_clean.csv",
    output:
        "data/merged/merged_dataset.csv"
    log:
        "logs/merge.log"
    shell:
        "python merge.py > {log} 2>&1"

# ── Step 4: Analyse and visualise ────────────────────────────────────────────
rule analyze:
    input:
        "data/merged/merged_dataset.csv"
    output:
        "results/figures/earnings_by_control.png",
        "results/figures/debt_vs_earnings.png",
        "results/figures/tuition_distribution.png",
        "results/figures/aid_vs_earnings.png",
        "results/tables/summary_statistics.csv",
        "results/tables/top10_earnings.csv",
        "results/tables/bottom10_earnings.csv",
    log:
        "logs/analyze.log"
    shell:
        "python analyze.py > {log} 2>&1"
