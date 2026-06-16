from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "online_shoppers_intention.csv"


def build_sample(seed=7, rows=3000):
    rng = np.random.default_rng(seed)
    data = pd.DataFrame(
        {
            "session_id": [f"SESSION-{i:05d}" for i in range(1, rows + 1)],
            "administrative": rng.poisson(2, rows),
            "administrative_duration": rng.gamma(1.8, 28, rows).round(2),
            "informational": rng.poisson(1, rows),
            "informational_duration": rng.gamma(1.5, 18, rows).round(2),
            "productrelated": rng.poisson(18, rows),
            "productrelated_duration": rng.gamma(2.4, 260, rows).round(2),
            "bouncerates": rng.beta(1.2, 12, rows).round(4),
            "exitrates": rng.beta(1.8, 10, rows).round(4),
            "pagevalues": rng.gamma(1.2, 8, rows).round(2),
            "specialday": rng.choice([0, 0.2, 0.4, 0.6, 0.8, 1], rows, p=[0.72, 0.08, 0.06, 0.05, 0.05, 0.04]),
            "month": rng.choice(["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rows),
            "operatingsystems": rng.integers(1, 8, rows),
            "browser": rng.integers(1, 14, rows),
            "region": rng.integers(1, 10, rows),
            "traffictype": rng.integers(1, 21, rows),
            "visitortype": rng.choice(["Returning_Visitor", "New_Visitor", "Other"], rows, p=[0.82, 0.16, 0.02]),
            "weekend": rng.choice([False, True], rows, p=[0.76, 0.24]),
        }
    )
    score = 0.04 + (data["pagevalues"] > 5) * 0.18 + (data["productrelated"] > 20) * 0.05 - data["bouncerates"] * 0.35
    data["revenue"] = rng.random(rows) < score.clip(0.01, 0.65)
    return data


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    build_sample().to_csv(OUTPUT, index=False)
    print(f"Wrote fallback shopper behavior sample to {OUTPUT}")


if __name__ == "__main__":
    main()
