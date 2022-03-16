import numpy as np

def distance_features(data):
    
    data['Mo_S_dist'] = data['representative'].apply(lambda x: np.linalg.norm(x[0].coords - x[1].coords)**0.5)
    data['S_Se_dist'] = data['representative'].apply(lambda x: np.linalg.norm(x[1].coords - x[2].coords)**0.5)
    data['Mo_Se_dist'] = data['representative'].apply(lambda x: np.linalg.norm(x[0].coords - x[2].coords)**0.5)
    return data