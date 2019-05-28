import warnings

import numpy as np
import pandas as pd
from lightgbm import LGBMRanker
from recsys.df_utils import split_by_timestamp
from recsys.metric import mrr_fast
from recsys.transformers import DivideByRanking
from recsys.utils import group_lengths
from recsys.vectorizers import make_vectorizer_1, numerical_features_py
from scipy import sparse
from sklearn.compose import ColumnTransformer

warnings.filterwarnings("ignore")

df = pd.read_csv("../../data/events_sorted_trans_all.csv", nrows=1000000)

vectorizer = make_vectorizer_1()

df_train, df_val = split_by_timestamp(df)
mat_train = vectorizer.fit_transform(df_train, df_train["was_clicked"])
mat_val = vectorizer.transform(df_val)

# test initial MRR
model = LGBMRanker()
model.fit(mat_train, df_train["was_clicked"], group=group_lengths(df_train["clickout_id"]))
df_val["click_proba"] = model.predict(mat_val)
mrr_val = mrr_fast(df_val, "click_proba")
current_best_mrr = mrr_val

columns_to_add = set(numerical_features_py).intersection(set(df.columns))
columns_added = set()

print("MRR Starting {}".format(current_best_mrr))

while len(columns_to_add) > 0:
    column_to_try = list(columns_to_add)[0]
    if df_train[column_to_try].dtype == np.bool:
        df_train[column_to_try] = df_train[column_to_try].astype(np.float32)
        df_val[column_to_try] = df_val[column_to_try].astype(np.float32)

    new_vectorizer = ColumnTransformer(
        [("divide_by_rank", DivideByRanking(), list(columns_added) + [column_to_try, "rank"])]
    )

    mat_train_new = new_vectorizer.fit_transform(df_train, df_train["was_clicked"])
    mat_val_new = new_vectorizer.transform(df_val)

    mat_train_joined = sparse.hstack([mat_train, mat_train_new])
    mat_val_joined = sparse.hstack([mat_val, mat_val_new])

    model = LGBMRanker()
    model.fit(mat_train_joined, df_train["was_clicked"], group=group_lengths(df_train["clickout_id"]))

    # df_train["click_proba"] = model.predict(mat_train_joined)
    df_val["click_proba"] = model.predict(mat_val_joined)

    # mrr_train = mrr_fast(df_train, "click_proba")
    mrr_val = mrr_fast(df_val, "click_proba")

    if mrr_val > current_best_mrr + 0.0001:
        columns_added.add(column_to_try)
        current_best_mrr = mrr_val
        print("Keeping feature %s mrr val %.4f" % (column_to_try, mrr_val))

    else:
        print("Not add feature %s mrr val %.4f" % (column_to_try, mrr_val))
        # keeping the feature

    columns_to_add.remove(column_to_try)
