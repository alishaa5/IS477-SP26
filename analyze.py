"""
analyze.py — Produce summary statistics and visualizations from the merged dataset.
Outputs go to results/figures/ and results/tables/.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend for CI / headless environments
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

MERGED_PATH  = os.path.join("data", "merged", "merged_dataset.csv")
FIGURES_DIR  = os.path.join("results", "figures")
TABLES_DIR   = os.path.join("results", "tables")
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR,  exist_ok=True)

# label maps

CONTROL_LABELS = {1: "Public", 2: "Private Nonprofit", 3: "Private For-Profit"}
ICLEVEL_LABELS = {1: "4-year", 2: "2-year", 3: "Less-than-2-year"}

# helpers

def save_fig(name: str) -> None:
    path = os.path.join(FIGURES_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Figure saved → {path}")


def fmt_dollar(x, _):
    return f"${x:,.0f}"

# analyses

def summary_stats(df: pd.DataFrame) -> None:
    cols = ["TUITIONFEE_IN", "TUITIONFEE_OUT", "DEBT_MDN", "MD_EARN_WNE_P10"]
    stats = df[cols].describe().T
    path = os.path.join(TABLES_DIR, "summary_statistics.csv")
    stats.to_csv(path)
    print(f"  Table saved → {path}")
    print(stats.to_string())


def earnings_by_control(df: pd.DataFrame) -> None:
    """Median earnings 10 years post-enrollment by institution control type."""
    df2 = df.copy()
    df2["Control"] = df2["CONTROL"].map(CONTROL_LABELS)
    grouped = df2.groupby("Control")["MD_EARN_WNE_P10"].median().dropna().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#2196F3", "#4CAF50", "#FF5722"]
    grouped.plot(kind="bar", ax=ax, color=colors[:len(grouped)], edgecolor="white", width=0.6)
    ax.set_title("Median Earnings 10 Years Post-Enrollment\nby Institution Control Type", fontsize=12)
    ax.set_xlabel("")
    ax.set_ylabel("Median Earnings (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    ax.tick_params(axis="x", rotation=15)
    plt.tight_layout()
    save_fig("earnings_by_control.png")


def debt_vs_earnings(df: pd.DataFrame) -> None:
    """Scatter: median debt vs median earnings, coloured by control type."""
    df2 = df.dropna(subset=["DEBT_MDN", "MD_EARN_WNE_P10", "CONTROL"]).copy()
    df2["Control"] = df2["CONTROL"].map(CONTROL_LABELS).fillna("Unknown")

    color_map = {"Public": "#2196F3", "Private Nonprofit": "#4CAF50",
                 "Private For-Profit": "#FF5722", "Unknown": "#9E9E9E"}

    fig, ax = plt.subplots(figsize=(8, 5))
    for label, group in df2.groupby("Control"):
        ax.scatter(group["DEBT_MDN"], group["MD_EARN_WNE_P10"],
                   alpha=0.4, s=18, label=label, color=color_map.get(label, "#9E9E9E"))

    # 1:1 reference line (debt equals earnings)
    lim = max(df2["DEBT_MDN"].max(), df2["MD_EARN_WNE_P10"].max()) * 1.05
    ax.plot([0, lim], [0, lim], "k--", linewidth=0.8, alpha=0.5, label="Debt = Earnings")

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    ax.set_xlabel("Median Student Debt (USD)")
    ax.set_ylabel("Median Earnings 10 Yrs Post-Enrollment (USD)")
    ax.set_title("Student Debt vs. Earnings by Institution Type")
    ax.legend(fontsize=8, markerscale=1.5)
    plt.tight_layout()
    save_fig("debt_vs_earnings.png")


def tuition_distribution(df: pd.DataFrame) -> None:
    """Box plots: in-state tuition distribution by institution level."""
    df2 = df.dropna(subset=["TUITIONFEE_IN", "ICLEVEL"]).copy()
    df2["Level"] = df2["ICLEVEL"].map(ICLEVEL_LABELS).fillna("Other")

    order = ["4-year", "2-year", "Less-than-2-year", "Other"]
    groups = [df2.loc[df2["Level"] == lbl, "TUITIONFEE_IN"].dropna() for lbl in order]
    groups = [(lbl, g) for lbl, g in zip(order, groups) if len(g) > 0]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.boxplot([g.values for _, g in groups],
               tick_labels=[lbl for lbl, _ in groups],
               patch_artist=True,
               boxprops=dict(facecolor="#90CAF9", color="#1565C0"),
               medianprops=dict(color="#B71C1C", linewidth=2),
               flierprops=dict(marker="o", markersize=2, alpha=0.4))
    ax.set_title("In-State Tuition Distribution by Institution Level")
    ax.set_xlabel("Institution Level")
    ax.set_ylabel("In-State Tuition (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    plt.tight_layout()
    save_fig("tuition_distribution.png")


def aid_vs_earnings(df: pd.DataFrame) -> None:
    if "ANYAIDP" not in df.columns:
        print("  ANYAIDP not found, using FLOAN_A instead.")
        if "FLOAN_A" not in df.columns:
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.text(0.5, 0.5, "Data not available", ha="center")
            save_fig("aid_vs_earnings.png")
            return
        df = df.copy()
        df["ANYAIDP"] = (df["FLOAN_A"] > 0).map({True: 1, False: 2})

    df2 = df.dropna(subset=["ANYAIDP", "MD_EARN_WNE_P10"]).copy()
    df2["Aid Available"] = df2["ANYAIDP"].map({1: "Yes", 2: "No"}).fillna("Unknown")
    grouped = df2.groupby("Aid Available")["MD_EARN_WNE_P10"].median().dropna()

    fig, ax = plt.subplots(figsize=(5, 4))
    grouped.plot(kind="bar", ax=ax, color=["#4CAF50", "#F44336"], edgecolor="white", width=0.5)
    ax.set_title("Median Earnings by Federal Aid Availability")
    ax.set_xlabel("Any Federal Aid Available")
    ax.set_ylabel("Median Earnings 10 Yrs Post-Enrollment (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    save_fig("aid_vs_earnings.png")


def top_bottom_earnings_table(df: pd.DataFrame) -> None:
    """Save tables of top-10 and bottom-10 schools by median earnings."""
    cols = ["INSTNM", "CITY", "STABBR", "MD_EARN_WNE_P10", "DEBT_MDN", "TUITIONFEE_IN"]
    available = [c for c in cols if c in df.columns]
    df2 = df.dropna(subset=["MD_EARN_WNE_P10"])[available].copy()

    top10 = df2.nlargest(10, "MD_EARN_WNE_P10")
    bot10 = df2.nsmallest(10, "MD_EARN_WNE_P10")

    top10.to_csv(os.path.join(TABLES_DIR, "top10_earnings.csv"), index=False)
    bot10.to_csv(os.path.join(TABLES_DIR, "bottom10_earnings.csv"), index=False)
    print(f"  Tables saved → results/tables/top10_earnings.csv, bottom10_earnings.csv")


# main

def main():
    print("=== analyze.py: generating results ===\n")

    if not os.path.exists(MERGED_PATH):
        raise FileNotFoundError(f"Merged dataset not found at {MERGED_PATH}. Run merge.py first.")

    df = pd.read_csv(MERGED_PATH, low_memory=False)
    print(f"  Loaded merged dataset: {df.shape[0]:,} rows × {df.shape[1]} columns\n")

    print("-- Summary statistics --")
    summary_stats(df)

    print("\n-- Earnings by institution control type --")
    earnings_by_control(df)

    print("\n-- Debt vs. earnings scatter --")
    debt_vs_earnings(df)

    print("\n-- Tuition distribution by institution level --")
    tuition_distribution(df)

    print("\n-- Aid availability vs. earnings --")
    aid_vs_earnings(df)

    print("\n-- Top/bottom earnings tables --")
    top_bottom_earnings_table(df)

    print("\n=== analyze.py complete ===")


if __name__ == "__main__":
    main()
