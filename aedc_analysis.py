"""
AEDC ADO Area Office - Marketer Performance & Revenue Analysis
=============================================================
Author: Opemipo Daniel Owolabi
Dataset: AEDC ADO Marketers Dashboard (May–June 2021)
Tools: Python, Pandas, Matplotlib, Seaborn

Business Problem:
-----------------
The Abuja Electricity Distribution Company (AEDC) needed a way to monitor
field marketer performance across multiple service centres. Revenue collection
was tracked daily but insights were buried in raw Excel sheets with no
automated visualisations or trend analysis.

This project automates the extraction, transformation, and analysis of that
data — answering key business questions:
  1. Which marketers consistently hit their collection targets?
  2. How did daily revenue collection trend across June 2021?
  3. Which book codes (customer zones) generate the most revenue?
  4. What is the customer response rate per marketer?

This is the exact workflow a Data Analyst would build to replace manual
Excel dashboards with reproducible, scalable Python analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
FILE = "/mnt/user-data/uploads/AEDC_ADO_2026.xlsx"
COLORS = ["#1f4e79", "#2e75b6", "#70ad47", "#ed7d31", "#ffc000", "#c00000"]
sns.set_theme(style="whitegrid", font_scale=1.1)

print("=" * 60)
print("  AEDC ADO MARKETER PERFORMANCE ANALYSIS")
print("  Opemipo Daniel Owolabi | Data Analytics Portfolio")
print("=" * 60)


# ─────────────────────────────────────────────
# 1. LOAD & CLEAN MARKETER PERFORMANCE DATA
#    Source: '18TH' sheet (May 2021 final dashboard)
# ─────────────────────────────────────────────
print("\n[1/4] Loading marketer performance data...")

df_raw = pd.read_excel(FILE, sheet_name="18TH", header=None)

# Extract marketer rows (rows where col 0 is a number = marketer ID rows)
marketer_rows = []
current_marketer = None

for _, row in df_raw.iterrows():
    name = row[1]
    book_code = row[3]
    cust_pop = row[4]
    cust_response = row[5]
    pct_response = row[6]
    energy_billed = row[7]
    billing_n = row[9]
    outstanding = row[10]
    target = row[11]
    monthly_sale = row[12]
    performance = row[13]

    if isinstance(name, str) and name.strip() not in ["NAME OF MARKETER", "PPM", ""]:
        if not name.startswith("ADO") and "TOTAL" not in name and "ACCOUNT" not in name:
            current_marketer = name.strip()

    if isinstance(book_code, str) and book_code.startswith("98-") and current_marketer:
        try:
            marketer_rows.append({
                "Marketer": current_marketer,
                "Book Code": book_code.strip(),
                "Cust Population": float(cust_pop) if pd.notna(cust_pop) else None,
                "Cust Response": float(cust_response) if pd.notna(cust_response) else None,
                "Response Rate": float(pct_response) if pd.notna(pct_response) else None,
                "Energy Billed (kWh)": float(energy_billed) if pd.notna(energy_billed) else None,
                "Billing (N)": float(billing_n) if pd.notna(billing_n) else None,
                "Outstanding (N)": float(outstanding) if pd.notna(outstanding) else None,
                "Target (N)": float(target) if pd.notna(target) else None,
                "Monthly Sale (N)": float(monthly_sale) if pd.notna(monthly_sale) else None,
                "Performance %": float(performance) if pd.notna(performance) else None,
            })
        except (ValueError, TypeError):
            pass

df = pd.DataFrame(marketer_rows).dropna(subset=["Marketer", "Billing (N)"])
print(f"   ✓ Loaded {len(df)} marketer-book records across {df['Marketer'].nunique()} marketers")


# ─────────────────────────────────────────────
# 2. LOAD DAILY COLLECTION TREND DATA
#    Source: Daily snapshot sheets (p18th → p30)
# ─────────────────────────────────────────────
print("[2/4] Building daily collection trend...")

# Each p-sheet = a daily running total snapshot
daily_snapshots = {
    "2021-06-18": ("p 18th", 2, 3),   # (sheet, total_row, amount_col)
    "2021-06-21": ("P21",    2, 3),
    "2021-06-22": ("P22",    2, 3),
    "2021-06-23": ("p23",    2, 3),
    "2021-06-24": ("P24",    1, 3),
    "2021-06-27": ("p27",    2, 3),
    "2021-06-28": ("p28",    2, 3),
    "2021-06-29": ("p29",    1, 3),
    "2021-06-30": ("p30",    1, 3),
}

trend_rows = []
for date_str, (sheet, tot_row, amt_col) in daily_snapshots.items():
    d = pd.read_excel(FILE, sheet_name=sheet, header=None)
    amount = d.iloc[tot_row, amt_col]
    contracts = d.iloc[tot_row, 1]
    try:
        trend_rows.append({
            "Date": pd.to_datetime(date_str),
            "Cumulative Collection (N)": float(amount),
            "Contracts Collected": float(contracts)
        })
    except (ValueError, TypeError):
        pass

df_trend = pd.DataFrame(trend_rows).sort_values("Date").reset_index(drop=True)
# Calculate daily incremental collections
df_trend["Daily Collection (N)"] = df_trend["Cumulative Collection (N)"].diff().fillna(
    df_trend["Cumulative Collection (N)"].iloc[0]
)
print(f"   ✓ Built trend data for {len(df_trend)} daily snapshots")


# ─────────────────────────────────────────────
# 3. AGGREGATED MARKETER SUMMARY
# ─────────────────────────────────────────────
print("[3/4] Aggregating marketer KPIs...")

marketer_summary = df.groupby("Marketer").agg(
    Total_Billing=("Billing (N)", "sum"),
    Total_Monthly_Sale=("Monthly Sale (N)", "sum"),
    Total_Cust_Pop=("Cust Population", "sum"),
    Total_Cust_Response=("Cust Response", "sum"),
    Avg_Performance=("Performance %", "mean"),
    Book_Codes=("Book Code", "count")
).reset_index()

marketer_summary["Collection Rate %"] = (
    marketer_summary["Total_Monthly_Sale"] / marketer_summary["Total_Billing"] * 100
).round(1)
marketer_summary["Customer Response Rate %"] = (
    marketer_summary["Total_Cust_Response"] / marketer_summary["Total_Cust_Pop"] * 100
).round(1)
marketer_summary = marketer_summary.sort_values("Total_Monthly_Sale", ascending=False)

print(f"   ✓ Summary built for {len(marketer_summary)} marketers")


# ─────────────────────────────────────────────
# 4. VISUALISATIONS
# ─────────────────────────────────────────────
print("[4/4] Generating dashboard visualisations...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle(
    "AEDC ADO Area Office — Marketer Performance Dashboard\nMay–June 2021  |  Analyst: Opemipo Daniel Owolabi",
    fontsize=15, fontweight="bold", y=1.01
)

# --- Chart 1: Total Collection by Marketer ---
ax1 = axes[0, 0]
bars = ax1.barh(
    marketer_summary["Marketer"],
    marketer_summary["Total_Monthly_Sale"] / 1e6,
    color=COLORS[:len(marketer_summary)]
)
ax1.set_xlabel("Total Collection (₦ Millions)")
ax1.set_title("💰 Total Revenue Collected per Marketer", fontweight="bold")
ax1.xaxis.set_major_formatter(mticker.FormatStrFormatter("₦%.1fM"))
for bar, val in zip(bars, marketer_summary["Total_Monthly_Sale"]):
    ax1.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
             f"₦{val/1e6:.2f}M", va="center", fontsize=9)
ax1.invert_yaxis()

# --- Chart 2: Customer Response Rate ---
ax2 = axes[0, 1]
colors_resp = ["#70ad47" if x >= 40 else "#ed7d31" if x >= 25 else "#c00000"
               for x in marketer_summary["Customer Response Rate %"]]
bars2 = ax2.bar(
    marketer_summary["Marketer"],
    marketer_summary["Customer Response Rate %"],
    color=colors_resp
)
ax2.axhline(y=40, color="#c00000", linestyle="--", linewidth=1.5, label="40% Target")
ax2.set_ylabel("Response Rate (%)")
ax2.set_title("📊 Customer Response Rate per Marketer", fontweight="bold")
ax2.set_xticklabels(marketer_summary["Marketer"], rotation=30, ha="right", fontsize=9)
ax2.legend(fontsize=9)
for bar, val in zip(bars2, marketer_summary["Customer Response Rate %"]):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             f"{val:.0f}%", ha="center", fontsize=9, fontweight="bold")

# --- Chart 3: Daily Collection Trend ---
ax3 = axes[1, 0]
ax3.plot(df_trend["Date"], df_trend["Cumulative Collection (N)"] / 1e6,
         marker="o", color="#1f4e79", linewidth=2.5, markersize=7, label="Cumulative")
ax3.fill_between(df_trend["Date"], df_trend["Cumulative Collection (N)"] / 1e6,
                 alpha=0.15, color="#1f4e79")
ax3_right = ax3.twinx()
ax3_right.bar(df_trend["Date"], df_trend["Daily Collection (N)"] / 1e6,
              alpha=0.4, color="#ffc000", width=0.5, label="Daily")
ax3.set_ylabel("Cumulative (₦ Millions)", color="#1f4e79")
ax3_right.set_ylabel("Daily (₦ Millions)", color="#ffc000")
ax3.set_title("📈 Daily Revenue Collection Trend — June 2021", fontweight="bold")
ax3.tick_params(axis="x", rotation=30)
ax3.yaxis.set_major_formatter(mticker.FormatStrFormatter("₦%.0fM"))
ax3_right.yaxis.set_major_formatter(mticker.FormatStrFormatter("₦%.1fM"))

# --- Chart 4: Collection Rate vs Billing ---
ax4 = axes[1, 1]
scatter = ax4.scatter(
    marketer_summary["Total_Billing"] / 1e6,
    marketer_summary["Collection Rate %"],
    s=marketer_summary["Total_Cust_Pop"] / 5,
    c=marketer_summary["Collection Rate %"],
    cmap="RdYlGn",
    alpha=0.85, edgecolors="white", linewidth=1.5
)
for _, row in marketer_summary.iterrows():
    ax4.annotate(row["Marketer"].split()[0],
                 (row["Total_Billing"] / 1e6, row["Collection Rate %"]),
                 textcoords="offset points", xytext=(6, 4), fontsize=9)
ax4.set_xlabel("Total Billing (₦ Millions)")
ax4.set_ylabel("Collection Rate (%)")
ax4.set_title("🎯 Collection Rate vs Billing Amount\n(bubble size = customer population)", fontweight="bold")
ax4.xaxis.set_major_formatter(mticker.FormatStrFormatter("₦%.1fM"))

plt.tight_layout()
plt.savefig("/home/claude/aedc_project/aedc_dashboard.png", dpi=150, bbox_inches="tight")
print("   ✓ Dashboard saved: aedc_dashboard.png")


# ─────────────────────────────────────────────
# 5. PRINT SUMMARY INSIGHTS
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KEY BUSINESS INSIGHTS")
print("=" * 60)

top = marketer_summary.iloc[0]
bottom = marketer_summary.iloc[-1]
total_collected = marketer_summary["Total_Monthly_Sale"].sum()
total_billed = marketer_summary["Total_Billing"].sum()
overall_rate = total_collected / total_billed * 100

print(f"\n  📌 Overall Collection Rate:   {overall_rate:.1f}%")
print(f"  📌 Total Billed (May 2021):   ₦{total_billed/1e6:.2f}M")
print(f"  📌 Total Collected:           ₦{total_collected/1e6:.2f}M")
print(f"\n  🏆 Top Performer:    {top['Marketer']}")
print(f"     → Collected ₦{top['Total_Monthly_Sale']/1e6:.2f}M ({top['Collection Rate %']:.1f}% rate)")
print(f"\n  ⚠️  Needs Improvement: {bottom['Marketer']}")
print(f"     → Collected ₦{bottom['Total_Monthly_Sale']/1e6:.2f}M ({bottom['Collection Rate %']:.1f}% rate)")

# June trend insight
june_start = df_trend["Cumulative Collection (N)"].iloc[0]
june_end = df_trend["Cumulative Collection (N)"].iloc[-1]
june_growth = ((june_end - june_start) / june_start) * 100
print(f"\n  📈 June 2021 Revenue Growth: +{june_growth:.1f}%")
print(f"     (₦{june_start/1e6:.2f}M → ₦{june_end/1e6:.2f}M over {len(df_trend)} reporting days)")

print("\n  ✅ Analysis complete. Dashboard saved.")
print("=" * 60)
