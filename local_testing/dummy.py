from argparse import ArgumentParser
import pandas as pd

parser = ArgumentParser(description="dummy producer of submission.csv")
parser.add_argument('train', type=str, help='train csv')
parser.add_argument('test', type=str, help='test csv')

args = parser.parse_args()
sub = pd.read_csv(args.test, index_col='id')
sub['predictions'] = 0
sub.to_csv('submission.csv', index='id')
