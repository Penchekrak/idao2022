import json
from argparse import ArgumentParser

import numpy as np
import pandas as pd
import tensorflow as tf
import yaml
from megnet.data.crystal import CrystalGraph
from megnet.models import MEGNetModel
from pymatgen.core import Structure
from sklearn.model_selection import train_test_split


def read_pymatgen_dict(file):
    with open(file, "r") as f:
        d = json.load(f)
    return Structure.from_dict(d)


def energy_within_threshold(prediction, target):
    # compute absolute error on energy per system.
    # then count the no. of systems where max energy error is < 0.02.
    e_thresh = 0.02
    error_energy = tf.math.abs(target - prediction)

    success = tf.math.count_nonzero(error_energy < e_thresh)
    total = tf.size(target)
    return success / tf.cast(total, tf.int64)


def prepare_dataset(dataset_path):
    targets = pd.read_csv(dataset_path)
    struct = {
        item: read_pymatgen_dict('data/' + item + '.json')
        for item in targets['id']
    }

    data = pd.DataFrame(columns=["structures"], index=struct.keys())
    data = data.assign(structures=struct.values(), targets=targets['band_gap'].values)
    return train_test_split(data, test_size=0.25, random_state=666)


def prepare_model(cutoff, lr):
    nfeat_bond = 10
    r_cutoff = cutoff
    gaussian_centers = np.linspace(0, r_cutoff + 1, nfeat_bond)
    gaussian_width = 0.8

    return MEGNetModel(
        graph_converter=CrystalGraph(cutoff=r_cutoff),
        centers=gaussian_centers,
        width=gaussian_width,
        loss=["MAE"],
        npass=2,
        lr=lr,
        metrics=energy_within_threshold
    )


def main(config, train_path, test_path):
    train, test = prepare_dataset(train_path)
    model = prepare_model(
        float(config["model"]["cutoff"]),
        float(config["model"]["lr"]),
    )
    model.train(
        train.structures,
        train.targets,
        validation_structures=test.structures,
        validation_targets=test.targets,
        epochs=int(config["model"]["epochs"]),
        batch_size=int(config["model"]["batch_size"]),
    )

    model = prepare_model(
        float(config["model"]["cutoff"]), float(config["model"]["lr"])
    )
    model.load_weights(config['checkpoint_path'])

    test_df = pd.read_csv(test_path)

    struct = {item: read_pymatgen_dict('data/' + item + '.json') for item in test_df['id']}
    private_test = pd.DataFrame(columns=['id', 'structures'], index=struct.keys())
    private_test = private_test.assign(structures=struct.values())
    private_test = private_test.assign(predictions=model.predict_structures(private_test.structures))
    private_test[['predictions']].to_csv('./submission.csv', index_label='id')


if __name__ == '__main__':
    parser = ArgumentParser(description="dummy producer of submission.csv")
    parser.add_argument('train', type=str, help='train csv')
    parser.add_argument('test', type=str, help='test csv')
    parser.add_argument('config', type=str, default='config.yaml', help='config')
    args = parser.parse_args()
    with open(args.config) as file:
        config = yaml.safe_load(file)
    main(config, args.train, args.test)
