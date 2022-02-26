from collections import defaultdict
from tqdm.notebook import tqdm

def decompose(structure):
    result = defaultdict(int)
    for site in structure.sites:
        result[site.species.formula] += 1
    return result

def make_masks(data):
    mask_list = [
            data['decomposition'] == defaultdict(int, {'Mo1': 63, 'W1': 1, 'Se1': 2, 'S1': 126}), #done
            data['decomposition'] == defaultdict(int, {'Mo1': 63, 'W1': 1, 'Se1': 1, 'S1': 126}), #done
            data['decomposition'] == defaultdict(int, {'Mo1': 63, 'Se1': 1, 'S1': 126}), #done
            data['decomposition'] == defaultdict(int, {'Mo1': 63, 'W1': 1, 'S1': 126}),
            data['decomposition'] == defaultdict(int, {'Mo1': 63, 'Se1': 2, 'S1': 126}),
            data['decomposition'] == defaultdict(int, {'Mo1': 63, 'S1': 126}),

    ]
    return mask_list

def extract_ideal_structure(data):
    sample_for_extract = data[data['decomposition'] == defaultdict(int, {'Mo1': 63, 'W1': 1, 'S1': 126})].copy()
    ideal_structure_sites = []
    def _extract(structure):
        for site in structure.sites:
            if site.species.formula != 'W1' and site not in ideal_structure_sites:
                ideal_structure_sites.append(site)

    for structure in tqdm(sample_for_extract['structures'].values):
        _extract(structure)
    return ideal_structure_sites

def find_differ_sites(structure_sites, ideal_structure_sites):
    differ_sites = []
    for x in ideal_structure_sites:
        flag = 0
        for y in structure_sites:
            if (abs(x.coords - y.coords) < 1e-7).all():
                flag = 1
                if x.species.formula != y.species.formula:
                    differ_sites.append(y) # find another site on this position
                break
        if flag == 0: # didn't find site
            differ_sites.append(x)
    return differ_sites
#     differ_sites_in_order = [None, None, None]
#     for x in differ_sites:
#         if x.species.formula == 'Mo1' or x.species.formula == 'W1':
#             differ_sites_in_order[0] = x
#         elif x.species.formula == 'S1':
#             differ_sites_in_order[1] = x
#         else:
#             differ_sites_in_order[2] = x
#     return differ_sites_in_order
