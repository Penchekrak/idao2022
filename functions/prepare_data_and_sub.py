import pandas as pd
from pathlib import Path
import yaml
import json
from pymatgen.core import Structure

from functions.geometry_module import gap_is_close_to_W

def read_pymatgen_dict(file):
    with open(file, "r") as f:
        d = json.load(f)
    return Structure.from_dict(d)


def prepare_dataset(dataset_path, train=True):
    dataset_path = Path(dataset_path)
    struct = {
        item.name.strip(".json"): read_pymatgen_dict(item)
        for item in (dataset_path / "structures").iterdir()
    }

    data = pd.DataFrame(columns=["structures"], index=struct.keys())
    data = data.assign(structures=struct.values())
    if train:
        targets = pd.read_csv(dataset_path / "targets.csv", index_col=0)
        data = data.assign(targets=targets)

    return data

def make_prediction(data, ideal_structure_sites, mask_list):
    data['predictions'] = -1
    data.loc[mask_list[0], 'predictions'] = 1.808

    data['is_close'] = data['structures'].apply(lambda x: gap_is_close_to_W(x.sites, ideal_structure_sites))
    data.loc[mask_list[1] & ~data['is_close'], 'predictions'] = 1.14
    data.loc[mask_list[1] & data['is_close'], 'predictions'] = 1.18
    return data

def energy_within_threshold(prediction, target):
    e_thresh = 0.02
    error_energy = abs(target - prediction)

    success = sum(error_energy < e_thresh)
    return success / len(prediction)