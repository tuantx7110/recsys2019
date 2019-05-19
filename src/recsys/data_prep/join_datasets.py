from collections import defaultdict

import numpy as np
import pandas as pd

train = pd.read_csv("../../../data/train.csv")
train["src"] = "train"
train["is_test"] = 0
train["is_val"] = 0

test = pd.read_csv("../../../data/test.csv")
validation_set = pd.read_csv("../../../data/validation_items.csv").drop("clickout_id", axis=1)
validation_set["is_val"] = 1
validation_set["is_val"] = validation_set["is_val"].astype(np.int)
test["src"] = "test"
test["is_test"] = (test["reference"].isnull() & (test["action_type"] == "clickout item")).astype(np.int)
test = pd.merge(test, validation_set, how="left", on=["user_id", "session_id", "timestamp", "step"])
test["is_val"].fillna(0, inplace=True)

assert np.all(train.columns == test.columns)

events = pd.concat([train, test], axis=0)
events["is_val"] = events["is_val"].astype(np.int)
events.sort_values(["timestamp", "user_id", "step"], inplace=True)
events["fake_impressions"] = events.groupby(["user_id", "session_id"])["impressions"].bfill()
events["fake_prices"] = events.groupby(["user_id", "session_id"])["prices"].bfill()

events["clickout_step_rev"] = (
    events.groupby(["action_type", "session_id"])["step"].rank("max", ascending=False).astype(np.int)
)
events["clickout_step"] = (
    events.groupby(["action_type", "session_id"])["step"].rank("max", ascending=True).astype(np.int)
)
events["clickout_max_step"] = events["clickout_step"] + events["clickout_step_rev"] - 1

events.to_csv("../../../data/events_sorted.csv", index=False)
