import numpy as np
from functions.geometry_module import symmetry_transform_up, orange_closer, is_boarder, dist_to_diag

def unufication_class2(sample):
    sample['representative'] = sample['representative'].apply(lambda x: symmetry_transform_up(x.copy(), x[0].coords))
    sample['representative'] = sample['representative'].apply(lambda x: orange_closer(x.copy()))
    
    return sample

def distance_features(data):
    data['dist_to_diag_Mo'] = data['representative'].apply(lambda x: dist_to_diag(x[0].coords))
    data['dist_to_diag_S'] = data['representative'].apply(lambda x: dist_to_diag(x[1].coords))
    data['dist_to_diag_Se'] = data['representative'].apply(lambda x: dist_to_diag(x[2].coords))
    
    data['Mo_S_dist'] = data['representative'].apply(lambda x: np.linalg.norm(x[0].coords - x[1].coords)**0.5)
    data['S_Se_dist'] = data['representative'].apply(lambda x: np.linalg.norm(x[1].coords - x[2].coords)**0.5)
    data['Mo_Se_dist'] = data['representative'].apply(lambda x: np.linalg.norm(x[0].coords - x[2].coords)**0.5)
    return data


def geometrical_features(data):
    data = distance_features(data)

    for i in range(3):
        data['Mo_coords_' + str(i)] = data['representative'].apply(lambda x: x[0].frac_coords[i])

    for i in range(3):
        data['S_coords_' + str(i)] = data['representative'].apply(lambda x: x[1].frac_coords[i])

    for i in range(3):
        data['Se_coords_' + str(i)] = data['representative'].apply(lambda x: x[2].frac_coords[i])

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
