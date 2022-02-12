import os
import subprocess
from argparse import ArgumentParser
from tempfile import TemporaryDirectory

import mlflow
import numpy as np

from scoring import get_score

mlflow.set_tracking_uri('http://beleriand.velkerr.ru:8889')
parser = ArgumentParser(
    description="get filename of training file, run with given args, resulting file must be submission.csv")
parser.add_argument('runfile', type=str, help='file that generates submission')

STRUCTURE_DATA_PATH = "data/dichalcogenides_public/structures"
FOLD_INFO_PATH = 'fold_info'
TRAIN_FILE = "train.csv"
TEST_FILE = "test.csv"
TARGET_FILE = "test_answer.csv"
SUBMISSION_NAME = 'submission.csv'


def run(runfile, unknown, train, test, cwd=None):
    subprocess.run(f"python3 {runfile} {train} {test} " + " ".join(unknown), cwd=cwd, shell=True)


def loop_over_folds(runfile, unknown):
    folds = sorted(next(os.walk(FOLD_INFO_PATH))[1])
    results = {}
    for fold_path in folds:
        fold_info = os.path.join(FOLD_INFO_PATH, fold_path)
        with TemporaryDirectory() as tmpdir:
            os.symlink(os.path.abspath(os.path.join('..', STRUCTURE_DATA_PATH)), os.path.join(tmpdir, 'data'))
            os.symlink(os.path.abspath(os.path.join(fold_info, TRAIN_FILE)), os.path.join(tmpdir, TRAIN_FILE))
            os.symlink(os.path.abspath(os.path.join(fold_info, TEST_FILE)), os.path.join(tmpdir, TEST_FILE))

            run(runfile, unknown, TRAIN_FILE, TEST_FILE, cwd=tmpdir)

            score = get_score(os.path.join(fold_info, TARGET_FILE), submission=os.path.join(tmpdir, SUBMISSION_NAME))
            results[fold_path] = score
    return results


def main(runfile, unknown):
    with mlflow.start_run():
        results = loop_over_folds(runfile, unknown)
        mlflow.log_metrics(results)
        vals = list(results.values())
        mlflow.log_metric("mean_score", np.mean(vals))
        mlflow.log_metric("std_score", np.std(vals))


if __name__ == '__main__':
    args, unknown = parser.parse_known_args()
    main(args.runfile, unknown)
