import pandas as pd

SUBMISSION_NAME = 'submission.csv'
THRESHOLD = 0.02


def get_score(target, submission=SUBMISSION_NAME):
    submission_df = pd.read_csv(submission, index_col='id')
    target_df = pd.read_csv(target, index_col='_id')
    joined = target_df.join(submission_df)
    diff = joined['predictions'] - joined['band_gap']
    diff = diff.abs()
    within_threshold = diff < THRESHOLD
    return within_threshold.mean()
