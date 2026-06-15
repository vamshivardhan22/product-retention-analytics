from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "user_events.csv"


def build_events(seed=7, users=2500):
    rng = np.random.default_rng(seed)
    DATA_DIR.mkdir(exist_ok=True)
    start = pd.Timestamp("2025-01-01")
    channels = ["Organic", "Paid Search", "Social", "Referral", "Email"]
    plans = ["Free", "Starter", "Pro", "Team"]
    events = []

    for i in range(1, users + 1):
        user_id = f"USER-{i:05d}"
        signup = start + pd.Timedelta(days=int(rng.integers(0, 240)))
        channel = rng.choice(channels, p=[0.31, 0.24, 0.18, 0.15, 0.12])
        plan = rng.choice(plans, p=[0.46, 0.26, 0.2, 0.08])
        stickiness = {"Free": 0.42, "Starter": 0.56, "Pro": 0.68, "Team": 0.75}[plan]

        events.append([user_id, signup, "signup", channel, plan, "landing"])
        active_days = sorted(set(int(x) for x in rng.exponential(28, size=int(rng.integers(8, 45))) if x < 180))
        for day in active_days:
            event_date = signup + pd.Timedelta(days=day)
            if rng.random() > stickiness and day > 30:
                continue
            events.append([user_id, event_date, "session_start", channel, plan, "home"])
            if rng.random() < 0.74:
                events.append([user_id, event_date + pd.Timedelta(minutes=2), "view_feature", channel, plan, rng.choice(["search", "dashboard", "reports"])])
            if rng.random() < 0.42:
                events.append([user_id, event_date + pd.Timedelta(minutes=5), "activation", channel, plan, "core_action"])
            if rng.random() < 0.23:
                events.append([user_id, event_date + pd.Timedelta(minutes=8), "checkout_start", channel, plan, "billing"])
            if rng.random() < 0.16:
                events.append([user_id, event_date + pd.Timedelta(minutes=11), "purchase", channel, plan, "subscription"])

    df = pd.DataFrame(events, columns=["user_id", "event_time", "event_name", "acquisition_channel", "plan", "screen"])
    df["event_time"] = pd.to_datetime(df["event_time"])
    return df.sort_values(["event_time", "user_id"])


def main():
    events = build_events()
    events.to_csv(OUTPUT, index=False)
    print(f"Wrote {len(events):,} events to {OUTPUT}")


if __name__ == "__main__":
    main()
