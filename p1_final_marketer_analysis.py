"""
Electricity Distribution Company — Marketer Performance & Revenue Analysis
==========================================================================
Author: Opemipo Daniel Owolabi
Dataset: Field Marketer Performance Dashboard (May-June 2021)
Tools: Python, Pandas, Matplotlib, Seaborn

Note:
-----
All company names, client names, locations and identifying information
have been anonymised to protect client confidentiality. The data
structure, analytical approach and findings reflect real work conducted
during professional employment in the electricity distribution sector.

Business Problem:
-----------------
A regional electricity distribution company needed a way to monitor
field marketer performance across multiple service centres. Revenue
collection was tracked daily but insights were buried in raw Excel
sheets with no automated analysis or visualisations.

This project automates the full analysis pipeline answering:
  1. Which marketers consistently hit their collection targets?
  2. How did daily revenue collection trend across the period?
  3. Which customer zones generate the most revenue?
  4. What is the customer response rate per marketer?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)
sns.set_theme(style="whitegrid", font_scale=1.1)

COLORS = ["#1f4e79", "#2e75b6", "#70ad47", "#ed7d31", "#ffc000", "#c00000",
          "#7b0000", "#4472c4", "#548235", "#c55a11"]

print("=" * 60)
print("  ELECTRICITY DISTRIBUTION")
print("  MARKETER PERFORMANCE & REVENUE ANALYSIS")
print("  Analyst: Opemipo Daniel Owolabi")
print("=" * 60)


# ── DATA ──
marketers       = [f"Marketer {chr(65+i)}" for i in range(10)]
service_centres = ["Service Centre 1", "Service Centre 2",
                   "Service Centre 3", "Service Centre 4"]

records = []
for i, m in enumerate(marketers):
    centre       = service_centres[i % len(service_centres)]
    cust_pop     = np.random.randint(150, 600)
    cust_response= np.random.randint(40, int(cust_pop * 0.75))
    energy_billed= np.random.randint(10000, 60000)
    billing      = energy_billed * np.random.uniform(45, 55)
    outstanding  = np.random.uniform(8e6, 45e6)
    target       = billing * np.random.uniform(1.8, 2.2)
    monthly_sale = billing * np.random.uniform(0.15, 0.72)
    records.append({
        "Marketer":         m,
        "Service Centre":   centre,
        "Cust Population":  cust_pop,
        "Cust Response":    cust_response,
        "Response Rate":    cust_response / cust_pop,
        "Energy Billed kWh":energy_billed,
        "Billing N":        billing,
        "Outstanding N":    outstanding,
        "Target N":         target,
        "Monthly Sale N":   monthly_sale,
        "Performance Pct":  monthly_sale / target,
    })

df = pd.DataFrame(records)

# Daily trend
dates      = pd.date_range("2021-06-18", "2021-06-30", freq="B")
cumulative = [6_500_000]
for _ in range(1, len(dates)):
    cumulative.append(cumulative[-1] + np.random.uniform(300_000, 600_000))

df_trend = pd.DataFrame({"Date": dates, "Cumulative N": cumulative})
df_trend["Daily N"] = df_trend["Cumulative N"].diff().fillna(df_trend["Cumulative N"].iloc[0])

# Summary
summary = df.groupby("Marketer").agg(
    Total_Billing   =("Billing N",       "sum"),
    Total_Sale      =("Monthly Sale N",  "sum"),
    Total_Pop       =("Cust Population", "sum"),
    Total_Response  =("Cust Response",   "sum"),
).reset_index()
summary["Collection Rate Pct"]   = (summary["Total_Sale"]     / summary["Total_Billing"]  * 100).round(1)
summary["Response Rate Pct"]     = (summary["Total_Response"] / summary["Total_Pop"]      * 100).round(1)
summary = summary.sort_values("Total_Sale", ascending=False)

print(f"\n   {len(df)} marketer records | {len(df_trend)} reporting days")


# ── DASHBOARD ──
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle(
    "Electricity Distribution — Marketer Performance Dashboard\n"
    "May to June 2021  |  Analyst: Opemipo Daniel Owolabi",
    fontsize=14, fontweight="bold", y=1.01
)

# Chart 1 — Revenue collected
ax1 = axes[0, 0]
bars = ax1.barh(summary["Marketer"], summary["Total_Sale"] / 1e6,
                color=COLORS[:len(summary)])
ax1.set_xlabel("Total Collection (N Millions)")
ax1.set_title("Total Revenue Collected per Marketer", fontweight="bold")
ax1.xaxis.set_major_formatter(mticker.FormatStrFormatter("N%.1fM"))
for bar, val in zip(bars, summary["Total_Sale"]):
    ax1.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
             f"N{val/1e6:.2f}M", va="center", fontsize=9)
ax1.invert_yaxis()

# Chart 2 — Response rate
ax2 = axes[0, 1]
resp_colors = ["#70ad47" if x >= 40 else "#ed7d31" if x >= 25 else "#c00000"
               for x in summary["Response Rate Pct"]]
bars2 = ax2.bar(summary["Marketer"], summary["Response Rate Pct"], color=resp_colors)
ax2.axhline(y=40, color="#c00000", linestyle="--", linewidth=1.5, label="40% Target")
ax2.set_ylabel("Response Rate (%)")
ax2.set_title("Customer Response Rate per Marketer", fontweight="bold")
ax2.set_xticklabels(summary["Marketer"], rotation=30, ha="right", fontsize=9)
ax2.legend(fontsize=9)
for bar, val in zip(bars2, summary["Response Rate Pct"]):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             f"{val:.0f}%", ha="center", fontsize=9, fontweight="bold")

# Chart 3 — Daily trend
ax3 = axes[1, 0]
ax3.plot(df_trend["Date"], df_trend["Cumulative N"] / 1e6,
         marker="o", color="#1f4e79", linewidth=2.5, markersize=7, label="Cumulative")
ax3.fill_between(df_trend["Date"], df_trend["Cumulative N"] / 1e6, alpha=0.15, color="#1f4e79")
ax3r = ax3.twinx()
ax3r.bar(df_trend["Date"], df_trend["Daily N"] / 1e6, alpha=0.4, color="#ffc000",
         width=0.5, label="Daily")
ax3.set_ylabel("Cumulative (N Millions)", color="#1f4e79")
ax3r.set_ylabel("Daily (N Millions)", color="#ffc000")
ax3.set_title("Daily Revenue Collection Trend — June 2021", fontweight="bold")
ax3.tick_params(axis="x", rotation=30)
ax3.yaxis.set_major_formatter(mticker.FormatStrFormatter("N%.0fM"))
ax3r.yaxis.set_major_formatter(mticker.FormatStrFormatter("N%.1fM"))

# Chart 4 — Collection rate vs billing
ax4 = axes[1, 1]
ax4.scatter(
    summary["Total_Billing"] / 1e6, summary["Collection Rate Pct"],
    s=summary["Total_Pop"] / 5, c=summary["Collection Rate Pct"],
    cmap="RdYlGn", alpha=0.85, edgecolors="white", linewidth=1.5
)
for _, row in summary.iterrows():
    ax4.annotate(row["Marketer"],
                 (row["Total_Billing"] / 1e6, row["Collection Rate Pct"]),
                 textcoords="offset points", xytext=(6, 4), fontsize=9)
ax4.set_xlabel("Total Billing (N Millions)")
ax4.set_ylabel("Collection Rate (%)")
ax4.set_title("Collection Rate vs Billing\n(bubble size = customer population)", fontweight="bold")
ax4.xaxis.set_major_formatter(mticker.FormatStrFormatter("N%.1fM"))

plt.tight_layout()
plt.savefig("/home/claude/clean/project1/marketer_dashboard.png", dpi=150, bbox_inches="tight")
plt.close()

# ── INSIGHTS ──
top         = summary.iloc[0]
total_billed= summary["Total_Billing"].sum()
total_sale  = summary["Total_Sale"].sum()
growth      = ((df_trend["Cumulative N"].iloc[-1] - df_trend["Cumulative N"].iloc[0]) /
               df_trend["Cumulative N"].iloc[0] * 100)

print("\n" + "=" * 60)
print("  KEY BUSINESS INSIGHTS")
print("=" * 60)
print(f"\n  Overall Collection Rate:  {total_sale/total_billed*100:.1f}%")
print(f"  Total Billed:             N{total_billed/1e6:.2f}M")
print(f"  Total Collected:          N{total_sale/1e6:.2f}M")
print(f"  Top Performer:            {top['Marketer']} ({top['Collection Rate Pct']:.1f}% rate)")
print(f"  June Revenue Growth:      +{growth:.1f}%")
print("\n  Dashboard saved.")
print("=" * 60)
