# Product/User Behavior Analytics Dashboard

A professional user behavior analytics dashboard built on the real UCI **Online Shoppers Purchasing Intention** dataset.

## Dataset

Source: UCI Machine Learning Repository, Online Shoppers Purchasing Intention dataset.

The data contains ecommerce browsing sessions with page counts, page durations, bounce rates, exit rates, page values, visitor type, traffic type, weekend flag, and purchase outcome.

Important note: this dataset is session-level and does not include persistent user IDs or event timestamps. Because of that, the dashboard focuses on conversion behavior, engagement diagnostics, and funnel proxy analysis instead of pretending to perform true cohort retention.

## Features

- Conversion rate, sessions, conversions, average pages, duration, bounce rate, and exit rate.
- Funnel proxy from all sessions to product browsing, high engagement, page value, and conversion.
- Visitor type, traffic type, engagement band, and month-level analysis.
- Behavior diagnostics for high-exit and high-bounce sessions.
- SQL examples for analyst-style KPI validation.

## Run Locally

```powershell
pip install -r requirements.txt
streamlit run app.py
```

## Portfolio Story

This project answers product and growth questions:

- Which visitor types convert best?
- Which traffic types bring low-quality sessions?
- How do page value, bounce rate, and exit rate relate to conversion?
- Where does the shopping journey appear to lose intent?

## Project Files

- `app.py` - Streamlit product analytics dashboard.
- `data/online_shoppers_intention.csv` - cleaned real session dataset.
- `sql/retention_queries.sql` - SQL conversion and behavior queries.
- `scripts/seed_data.py` - fallback synthetic event generator kept for reproducibility.

