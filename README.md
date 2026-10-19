# Product Behavior and Conversion Analytics

A Streamlit dashboard for exploring e-commerce session behavior and purchase conversion. The project uses product analytics metrics to compare visitor groups, traffic sources, engagement patterns, and conversion outcomes.

## Features

- Conversion rate, session counts, average pages viewed, session duration, bounce rate, and exit rate.
- Funnel-style analysis of product browsing, engagement, page value, and conversion.
- Breakdown by visitor type, traffic type, engagement band, and month.
- Diagnostics for sessions with high bounce or exit rates.
- SQL examples for validating conversion and behavior metrics.

## Dataset

The project uses the Online Shoppers Purchasing Intention dataset from the UCI Machine Learning Repository. It contains session-level attributes such as page counts, page durations, bounce and exit rates, page value, visitor type, traffic type, weekend flag, and purchase outcome.

The dataset does not provide persistent user IDs or event timestamps. Therefore, the project analyzes session behavior and conversion patterns rather than claiming true user-level cohort retention.

## Tech stack

- Python
- pandas
- Streamlit
- SQL

## Run locally

Requirements: Python and pip.

```bash
git clone https://github.com/vamshivardhan22/product-retention-analytics.git
cd product-retention-analytics
pip install -r requirements.txt
streamlit run app.py
```

## Project files

- `app.py` — Streamlit dashboard.
- `data/online_shoppers_intention.csv` — cleaned session dataset.
- `sql/retention_queries.sql` — SQL conversion and behavior queries.
- `scripts/seed_data.py` — synthetic data generator.

## Example questions

- Which visitor types have higher conversion rates?
- How does traffic source relate to conversion?
- How do page value, bounce rate, and exit rate vary across sessions?
- Where does the shopping journey appear to lose intent?

## Skills demonstrated

Python, data analysis, product analytics, conversion funnel analysis, KPI reporting, SQL, and dashboard development.
