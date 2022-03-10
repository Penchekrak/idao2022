import json
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
import yaml
from megnet.data.crystal import CrystalGraph
from megnet.models import MEGNetModel
from pymatgen.core import Structure
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import LearningRateScheduler
from wandb.keras import WandbCallback

import wandb


def energy_within_threshold(prediction, target):
    # compute absolute error on energy per system.
    # then count the no. of systems where max energy error is < 0.02.
    e_thresh = 0.02
    error_energy = tf.math.abs(target - prediction)

    success = tf.math.count_nonzero(error_energy < e_thresh)
    total = tf.size(target)
    return success / tf.cast(total, tf.int64)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('config', type=str, default='config.yaml')
    return parser


def exponential_scheduler(epoch, lr):
    if epoch < 300:
        return lr
    else:
        return lr * 0.9999


def prepare_model(model_config) -> MEGNetModel:
    nfeat_bond = model_config['nfeat_bond']
    r_cutoff = model_config['cutoff']
    gaussian_centers = np.linspace(0, r_cutoff + 1, nfeat_bond)
    gaussian_width = model_config['gaussian_width']
    model = MEGNetModel(
        graph_converter=CrystalGraph(cutoff=r_cutoff),
        centers=gaussian_centers,
        width=gaussian_width,
        metrics=energy_within_threshold,
        loss=model_config['losses'],
        npass=2,
        lr=model_config['lr'],
        optimizer_kwargs={'clipnorm': model_config['clipnorm']},
    )
    if model_config['preload_embeddings'] is not None:
        model_form = MEGNetModel.from_file(model_config['preload_embeddings'])
        embedding_layer = [i for i in model_form.layers if i.name.startswith('embedding')][0]
        embedding = embedding_layer.get_weights()[0]
        embedding_layer_index = [i for i, j in enumerate(model.layers) if j.name.startswith('atom_embedding')][0]
        model.layers[embedding_layer_index].set_weights([embedding])
        if model_config['freeze_preload_embeddings']:
            model.layers[embedding_layer_index].trainable = False
    return model


def read_pymatgen_dict(file):
    with open(file, "r") as f:
        d = json.load(f)
    return Structure.from_dict(d)


def prepare_dataset(data_config):
    dataset_path = Path(data_config['path'])
    targets = pd.read_csv(dataset_path / "targets.csv", index_col=0)
    struct = {
        item.name.strip(".json"): read_pymatgen_dict(item)
        for item in (dataset_path / "structures").iterdir()
    }

    data = pd.DataFrame(columns=["structures"], index=struct.keys())
    data = data.assign(structures=struct.values(), targets=targets)

    return train_test_split(data, test_size=data_config['train_val_ratio'], random_state=data_config['random_state'])


def train(config):
    model = prepare_model(config['model'])
    train_set, test_set = prepare_dataset(config["data"])
    model.train(
        train_set.structures,
        train_set.targets,
        validation_structures=test_set.structures,
        validation_targets=test_set.targets,
        callbacks=[
            WandbCallback(monitor='energy_within_threshold', mode='max'),
            LearningRateScheduler(schedule=exponential_scheduler),
        ],
        epochs=int(config['model']['epochs']),
        batch_size=int(config["model"]["batch_size"])
    )


def main(args):
    with open(args.config, 'r') as config_file:
        config = yaml.safe_load(config_file)
    wandb.init(project="idao", entity="penchekrak", config=config)
    train(config)


if __name__ == "__main__":
    argparser = create_parser()
    args = argparser.parse_args()
    main(args)
