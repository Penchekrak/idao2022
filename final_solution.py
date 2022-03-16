import pandas as pd
import numpy as np

import tensorflow as tf
from xgboost import XGBClassifier

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

import pymatgen

from functions.prepare_data_and_sub import prepare_dataset, make_prediction
from functions.classification import predict_target_on_class
from functions.strusture_analysis import decompose, make_masks, find_differ_sites

from functions.prepare_data_and_sub import read_pymatgen_dict
ideal_structure = read_pymatgen_dict('ideal_structure.json')
ideal_structure_sites = ideal_structure.sites

data = prepare_dataset('data/dichalcogenides_public/')
data['decomposition'] = data.structures.apply(decompose)
mask_list = make_masks(data)
data['representative'] = data['structures'].apply(lambda x: find_differ_sites(x.sites, ideal_structure_sites))

test = prepare_dataset('data/dichalcogenides_private/', train=False)
test['decomposition'] = test.structures.apply(decompose)
mask_list_test = make_masks(test)
test['representative'] = test['structures'].apply(lambda x: find_differ_sites(x.sites, ideal_structure_sites))

test = make_prediction(test, ideal_structure_sites, mask_list_test)

n_estim_clf_list = [10, 14, 10, 12]
n_estim_reg_list = [12, 14, 15, 14]
for n in range(2, 6):
    class_n_predict_target = predict_target_on_class(data[mask_list[n]], test[mask_list_test[n]], n, n_estim_clf_list[n-2], n_estim_reg_list[n-2])
    test.loc[mask_list_test[n], 'predictions'] = class_n_predict_target

test[['predictions']].to_csv('./submission.csv', index_label='id')
