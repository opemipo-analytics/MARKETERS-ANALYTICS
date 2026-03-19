# AEDC Marketer Performance & Revenue Analysis

**Portfolio Project 1** — Python-powered performance analysis of field marketers at the **Abuja Electricity Distribution Company (AEDC)** ADO Area Office, May to June 2021.

> Built by **Opemipo Daniel Owolabi** — Data Analyst | Python · SQL · Power BI · Tableau  
> Faro, Portugal | opemipoowolabi001@gmail.com

---

## Business Problem

AEDC field marketers were responsible for visiting customers, collecting electricity bills, and reporting daily revenue. Performance data was tracked manually in Excel across multiple sheets — one per day — making it impossible to:

- Quickly identify top and bottom performers
- Visualise revenue collection trends over time
- Compare customer response rates across service centres
- Spot which book codes (customer zones) were underperforming

This project automates the entire analysis pipeline — from raw Excel ingestion to a visual performance dashboard — replacing hours of manual work with a single Python script.

---

## Dashboard Preview

![AEDC Dashboard](aedc_dashboard.png)

---

## Key Findings

| Metric | Value |
|--------|-------|
| Total Billed (May 2021) | N46.02 Million |
| Total Collected | N24.40 Million |
| Overall Collection Rate | 53.0% |
| Top Performer | FUNMILAYO AKEFE — N2.04M (71.4% rate) |
| Needs Improvement | INNOCENT OKENWA — N0.04M (6.1% rate) |
| June 2021 Revenue Growth | +72.3% over 9 reporting days |

---

## What the Dashboard Shows

### 1 — Total Revenue Collected per Marketer
Horizontal bar chart comparing total monthly revenue collected by each marketer, making it immediately clear who is driving the most value.

### 2 — Customer Response Rate per Marketer
Bar chart showing what percentage of assigned customers each marketer successfully engaged. A 40% target line is shown for reference. Green = above target, Orange = borderline, Red = below target.

### 3 — Daily Revenue Collection Trend — June 2021
Dual-axis chart showing cumulative collection (line) and daily incremental collection (bars). Revenue grew 72.3% from mid to end of June, showing strong late-month acceleration.

### 4 — Collection Rate vs Billing Amount
Scatter plot comparing each marketer's billing amount against their actual collection rate. Bubble size = customer population served.

---

## Project Structure

```
AEDC-MARKETERS-ANALYTICS/
│
├── aedc_analysis.py       # Main analysis and visualisation script
├── aedc_dashboard.png     # Output: 4-panel performance dashboard
├── README.md              # This file
└── data/
    └── ADO AEDC 2021.xlsx # Source data (19 sheets of daily tracking)
```

---

## How to Run

```bash
git clone https://github.com/opemipo-analytics/AEDC-MARKETERS-ANALYTICS.git
cd AEDC-MARKETERS-ANALYTICS

pip install pandas matplotlib seaborn openpyxl

python aedc_analysis.py
```

---

## Tools and Technologies

| Tool | Purpose |
|------|---------|
| Python 3 | Core scripting and automation |
| Pandas | Data extraction, cleaning, transformation |
| Matplotlib | Custom visualisations and charts |
| Seaborn | Visual theme and styling |
| Microsoft Excel | Original data source (19-sheet workbook) |

---

## Skills Demonstrated

- Data wrangling — handling messy, multi-sheet Excel files with inconsistent headers
- ETL pipeline — Extract, Transform, Analyse, Visualise
- Business intelligence — translating raw operational data into actionable KPIs
- Data storytelling — presenting findings through clear, labelled visualisations
- Real-world context — all data comes from an actual electricity utility operation

---

## Other Projects

| Project | Description |
|---------|-------------|
| [AEDC Revenue Forecasting ML](https://github.com/opemipo-analytics/aedc-revenue-forecasting) | Machine Learning revenue forecast (99.8% accuracy) |
| [AEDC Customer Segmentation](https://github.com/opemipo-analytics/aedc-customer-segmentation) | SQL and RFM customer segmentation analysis |

---

*This project is part of my data analytics portfolio, built from real data during my time as a Data Analyst at the Abuja Electricity Distribution Company (AEDC), Nigeria.*
