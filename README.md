# Product/User Behavior Analytics & Retention Analysis

A product analytics project focused on why users leave, where funnels break, and how retention changes by cohort, plan, and acquisition channel.

## What It Demonstrates

- Funnel analysis from signup to purchase.
- Cohort retention analysis by signup month.
- Churn risk analysis from inactivity windows.
- User journey analysis from event sequences.
- Python, Pandas, Seaborn, SQL, and dashboard storytelling.

## Run Locally

```powershell
pip install -r requirements.txt
python .\scripts\seed_data.py
streamlit run app.py
```

The app automatically creates `data/user_events.csv` if it does not exist.

## Analyst Questions Answered

- Where are users dropping off in the funnel?
- Which cohorts retain better?
- Which plans or channels have churn risk?
- What journeys are most common before purchase?

## Files

- `app.py` - Streamlit analytics dashboard.
- `scripts/seed_data.py` - deterministic product event dataset generator.
- `sql/retention_queries.sql` - reusable SQL analysis examples.
- `data/user_events.csv` - generated event-level data.

