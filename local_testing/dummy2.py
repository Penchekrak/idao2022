from argparse import ArgumentParser

import pandas as pd
import yaml

from baseline import prepare_model
from baseline import read_pymatgen_dict

parser = ArgumentParser(description="dummy producer of submission.csv")
parser.add_argument('train', type=str, help='train csv')
parser.add_argument('test', type=str, help='test csv')
parser.add_argument('config', type=str, default='config.yaml', help='config')


def main(config, test_path):
    model = prepare_model(
        float(config["model"]["cutoff"]), float(config["model"]["lr"])
    )
    model.load_weights(config['checkpoint_path'])

    test_df = pd.read_csv(test_path)

    struct = {item: read_pymatgen_dict(item + '.json') for item in test_df['id']}
    private_test = pd.DataFrame(columns=['id', 'structures'], index=struct.keys())
    private_test = private_test.assign(structures=struct.values())
    private_test = private_test.assign(predictions=model.predict_structures(private_test.structures))
    private_test[['predictions']].to_csv('./submission.csv', index_label='id')


if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.config) as file:
        config = yaml.safe_load(file)
    main(config, args.test)
