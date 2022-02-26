import numpy as np
from functions.geometry_module import symmetry_transform_up, orange_closer, is_boarder

def classificate_class2(target):
    if target >= 0.39 and target < 0.43:
        return 1
    if target >= 0.34 and target < 0.38:
        return 2
    if target >= 0.27 and target <= 0.31:
        return 3
    return 0


def unufication_class2(sample):
    sample['representative'] = sample['representative'].apply(lambda x: symmetry_transform_up(x.copy(), x[0].coords))
    sample['representative'] = sample['representative'].apply(lambda x: orange_closer(x.copy()))
    
    return sample

def geometrical_features(data):
    for i in range(3):
        data['Mo_coords_' + str(i)] = data['representative'].apply(lambda x: x[0].frac_coords[i])

    for i in range(3):
        data['S_coords_' + str(i)] = data['representative'].apply(lambda x: x[1].frac_coords[i])

    for i in range(3):
        data['Se_coords_' + str(i)] = data['representative'].apply(lambda x: x[2].frac_coords[i])

    data['Mo_S_dist'] = data['representative'].apply(lambda x: np.linalg.norm(x[0].coords - x[1].coords)**0.5)
    data['S_Se_dist'] = data['representative'].apply(lambda x: np.linalg.norm(x[1].coords - x[2].coords)**0.5)
    data['Mo_Se_dist'] = data['representative'].apply(lambda x: np.linalg.norm(x[0].coords - x[2].coords)**0.5)


    data['M_is_boarder'] = data['representative'].apply(lambda x: is_boarder(x[0]))
    data['S_is_boarder'] = data['representative'].apply(lambda x: is_boarder(x[1]))
    data['Se_is_boarder'] = data['representative'].apply(lambda x: is_boarder(x[2]))
    data['M_is_boarder_0'] = data['M_is_boarder'] == 0
    data['M_is_boarder_1'] = data['M_is_boarder'] == 1
    data['S_is_boarder_0'] = data['S_is_boarder'] == 0
    data['S_is_boarder_1'] = data['S_is_boarder'] == 1
    data['Se_is_boarder_1'] = data['Se_is_boarder'] == 1
    data['Se_is_boarder_0'] = data['Se_is_boarder'] == 0
    
    return data