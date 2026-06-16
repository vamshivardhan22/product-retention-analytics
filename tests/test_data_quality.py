import unittest
from pathlib import Path

import pandas as pd


class ProductBehaviorDataQualityTests(unittest.TestCase):
    def setUp(self):
        self.data = pd.read_csv(Path("data/online_shoppers_intention.csv"))

    def test_required_columns_exist(self):
        required = {
            "session_id",
            "administrative",
            "informational",
            "productrelated",
            "bouncerates",
            "exitrates",
            "pagevalues",
            "month",
            "traffictype",
            "visitortype",
            "weekend",
            "revenue",
        }
        self.assertTrue(required.issubset(self.data.columns))

    def test_conversion_data_is_valid(self):
        self.assertGreater(len(self.data), 10000)
        self.assertGreater(self.data["revenue"].mean(), 0)
        self.assertLess(self.data["revenue"].mean(), 1)
        self.assertTrue((self.data["bouncerates"] >= 0).all())
        self.assertTrue((self.data["exitrates"] >= 0).all())


if __name__ == "__main__":
    unittest.main()
