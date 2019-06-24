import subprocess
import os

ps = []
for n in range(32):
    args = ["python", "generate_training_data.py", "--hashn", str(n)]
    p = subprocess.Popen(args)
    ps.append(p)

for p in ps:
    p.wait()

os.system(
    "paste -d, ../../../data/events_sorted_trans_0*.csv ../../../data/features/comp-v1-selected.csv ../../../data/features/price_features.csv ../../../data/features/time_rank_user-features.csv > ../../../data/events_sorted_trans_all.csv"
)
