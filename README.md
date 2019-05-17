# recsys2019

Current process (full)
----------------------

1. cd data/
2. ./download_data.sh
3. cd ../../src/recsys/data_prep
4. ./run_data_prep.sh
5. cd ..
6. cd data_generator; python generate_data_parallel_all.py; cd - (pypy is good)
7. python split_events_sorted_trans.py (pypy is good)
8. python vectorize_datasets.py
9. python model_val.py (validate model)
10. python model_submit.py (make test predictions)
11. python make_blend.py (prepare submission file)

Steps 6-11 are also inside run_all.sh script

Quick validation (1 million rows)
----------------------

1. cd data/
2. ./download_data.sh
3. cd ../../src/recsys/data_prep
4. ./run_data_prep.sh
5. cd ..
6. cd data_generator; python generate_data_parallel_quick.py; cd - (pypy is good)
7. python quick_validate.py

Best submissions
---------------

Commit | 1m validation | Full validation | Leaderboard
--- | --- | --- | ---
unk | 0.6196 | 0.6174 | 0.6750
unk | 0.6233 | 0.6226 | 0.6776
unk | 0.6272 | 0.6237 | 0.6782
@14f76d | 0.6275 | 0.6241 | 0.6787
@995156 | 0.6330 | 0.6255 | 0.6795
@657072 | 0.6336 | 0.6266 | 0.6802
@560cd0 | 0.6352 | 0.6269 | 0.6807
@b7db8d | 0.6357 | 0.6289 | 0.6810
@c4993e | XXXXXX | 0.6297 | 0.6815

```

Feather
---------------

Run `to_feather.py` in data/ for process raw data into feather files for faster experiments.
`wr_eda.ipynb` in notebooks/ shows some EDA on intersections of IDs and session lengths.
