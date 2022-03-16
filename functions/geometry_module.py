from pymatgen.core import PeriodicSite
import numpy as np

def gap_is_close_to_W(structure_sites, ideal_structure_sites):
    site_W1 = structure_sites[63]
    
    site_S1 = structure_sites[0]
    for x in ideal_structure_sites:
        flag = 0
        for y in structure_sites:
            flag +=  (x.coords == y.coords).all()
        if flag == 0:
            site_S1 = x
            break
            
    return abs(np.linalg.norm(site_W1.coords - site_S1.coords) - 2.41693) < 1e-4