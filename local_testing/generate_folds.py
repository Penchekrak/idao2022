RANDOM_SEED = 43
DATA_PATH = "../data/dichalcogenides_public"
FOLD_INFO_PATH = "fold_info"

import os

import pandas as pd
from sklearn.model_selection import KFold

kfold = KFold(n_splits=5, random_state=RANDOM_SEED, shuffle=True)
train_files = pd.read_csv(os.path.join(DATA_PATH, "targets.csv"))
folds = kfold.split(train_files)
for i, (train_indices, test_indices) in enumerate(folds):
    os.makedirs(os.path.join(FOLD_INFO_PATH, f"fold_{i}"), exist_ok=True)

    with open(os.path.join(FOLD_INFO_PATH, f"fold_{i}", "train.csv"), 'w') as train_fold_info:
        train_files.iloc[train_indices].set_index('_id').to_csv(train_fold_info)
    with open(os.path.join(FOLD_INFO_PATH, f"fold_{i}", "test.csv"), 'w') as test_fold_info:
        train_files.iloc[test_indices]['_id'].to_csv(test_fold_info, index=False)
    with open(os.path.join(FOLD_INFO_PATH, f"fold_{i}", "test_answer.csv"), 'w') as test_fold_info:
        train_files.iloc[test_indices].set_index('_id').to_csv(test_fold_info)

