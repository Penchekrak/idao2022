import pandas as pd

THRESHOLD = 0.02


def get_score(target, submission):
    submission_df = pd.read_csv(submission, index_col='id')
    target_df = pd.read_csv(target, index_col='id')
    joined = target_df.join(submission_df)
    diff = joined['predictions'] - joined['band_gap']
    diff = diff.abs()
    within_threshold = diff < THRESHOLD
    return within_threshold.mean()
