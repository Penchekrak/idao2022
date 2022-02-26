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

def is_boarder(site): #if it's on boarder returns numeration
    k = -1.732050807568879 
    b_Mo_1 = 40.52245196764198
    b_Mo_2 = 1.8419297755492612

    b_S_1 = 42.36438130112811 
    b_S_2 = 3.683859109035394
    if site.species.formula == 'Mo1':
        if abs(site.coords[1] - 1.8419295545177048) < 1e-7 or abs(site.coords[1] - k * site.coords[0] - b_Mo_1) < 1e-7:
            return 0
        elif abs(site.coords[1] - 21.18219065056405) < 1e-7 or abs(site.coords[1] - k * site.coords[0] - b_Mo_2) < 1e-7:
            return 1
        else:
            return -1
    else:
        if abs(site.coords[1] - 0.9209648877746301) < 1e-7 or abs(site.coords[1] - k * site.coords[0] - b_S_1) < 1e-7:
            return 0
        elif abs(site.coords[1] - 20.261225983820975) < 1e-7 or abs(site.coords[1] - k * site.coords[0] - b_Mo_2) < 1e-7:
            return 1
        else:
            return -1
        
        
def get_symmetry_coord(point):
    a = np.array([22.33221003,  1.84192955,  3.719751  ])
    b = np.array([-11.16610482,  21.18219065 ,  3.719751  ])
    c = np.array([22.33221003,  1.84192955,  2.1549  ])
    x = b - a
    y = c - a
    i = x[1]*y[2] - x[2]*y[1]
    j = x[2]*y[0] - x[0]*y[2]
    k = x[0]*y[1] - x[1]*y[0]
    D = -(a[0]*i + a[1] * j + a[2]*k)
#     print(D == -(a[0]*i + a[1] * j + a[2]*k))
    
    t = -(point[0]*i + point[1]*j + point[2]*k + D) / [i**2+j**2+k**2]
    x3 = np.array([i,j,k]) * t + point
    return 2 * x3 - point
def is_up(point):
    a = np.array([22.33221003,  1.84192955,  3.719751  ])
    b = np.array([-11.16610482,  21.18219065 ,  3.719751  ])
    c = np.array([22.33221003,  1.84192955,  2.1549  ])
    x = b - a
    y = c - a
    i = x[1]*y[2] - x[2]*y[1]
    j = x[2]*y[0] - x[0]*y[2]
    k = x[0]*y[1] - x[1]*y[0]
#     print(point.dot(np.array([i,j,k])))
    return (point-a).dot(np.array([i,j,k])) <= 0

def get_symmetry_coord(point):
    a = np.array([22.33221003,  1.84192955,  3.719751  ])
    b = np.array([-11.16610482,  21.18219065 ,  3.719751  ])
    c = np.array([22.33221003,  1.84192955,  2.1549  ])
    x = b - a
    y = c - a
    i = x[1]*y[2] - x[2]*y[1]
    j = x[2]*y[0] - x[0]*y[2]
    k = x[0]*y[1] - x[1]*y[0]
    D = -(a[0]*i + a[1] * j + a[2]*k)
    
    t = -(point[0]*i + point[1]*j + point[2]*k + D) / [i**2+j**2+k**2]
    x3 = np.array([i,j,k]) * t + point
    return 2 * x3 - point

def is_up(point):
    a = np.array([22.33221003,  1.84192955,  3.719751  ])
    b = np.array([-11.16610482,  21.18219065 ,  3.719751  ])
    c = np.array([22.33221003,  1.84192955,  2.1549  ])
    x = b - a
    y = c - a
    i = x[1]*y[2] - x[2]*y[1]
    j = x[2]*y[0] - x[0]*y[2]
    k = x[0]*y[1] - x[1]*y[0]
    return (point-a).dot(np.array([i,j,k])) <= 0

def symmetry_transform_up(sites, gap_pos):
    W_up = is_up(gap_pos)
    if W_up:
        return sites

    sites_new = []
    for site in sites.copy():
            new_coord = get_symmetry_coord(site.coords)
            if np.abs(site.coords[2] - 2.1549) < 1e-2:
                new_coord[2] = 5.2846
            elif np.abs(site.coords[2] - 5.2846) < 1e-2:
                new_coord[2] = 2.1549
            new_elt = PeriodicSite(species=site.species,coords=new_coord,properties=site.properties, lattice = site.lattice,coords_are_cartesian = True)
            sites_new.append(new_elt)

    return sites_new


def orange_is_close(point):
    if np.abs(point[2] - 2.1549)<1e-2:
        return True
    elif np.abs(point[2] - 5.2846)<1e-2:
        return False
def orange_closer(sites):
    sites_new = []
    sites_old = []
    W_up = True
    for site in sites:
        if site.species.formula == 'Se1': #\
            new_coord = site.coords
            if np.abs(site.coords[2] - 2.1549)<1e-2:
                new_coord[2] = 5.2846
            elif np.abs(site.coords[2] - 5.2846)<1e-2:
                new_coord[2] = 2.1549
            new_elt = PeriodicSite(species=site.species,coords=new_coord,properties=site.properties, lattice = site.lattice,coords_are_cartesian = True)
            sites_new.append(new_elt)
            sites_old.append(site)
            W_up = orange_is_close(site.coords)
            continue
        else:
    #         ste = site.copy()
            new_coord = site.coords
            if np.abs(site.coords[2] - 2.1549)<1e-2:
                new_coord[2] = 5.2846
            elif np.abs(site.coords[2] - 5.2846)<1e-2:
                new_coord[2] = 2.1549
            new_elt = PeriodicSite(species=site.species,coords=new_coord,properties=site.properties, lattice = site.lattice,coords_are_cartesian = True)
            sites_new.append(new_elt)
            sites_old.append(site)
    return sites_old if W_up else sites_new

def dist_to_diag(point):
    lvl11_x = -11.16610
    lvl11_y = 21.18219
    lvl12_x = 22.332
    lvl12_y = 1.8419
    
    lvl21_x = 23.9273
    lvl21_y = 0.92096
    lvl22_x = -9.5709
    lvl22_y = 20.26122
    
    if abs(point[2] - 3.7198) < 1e-3:
        k =(lvl11_y - lvl12_y) / (lvl11_x - lvl12_x)
        b = lvl11_y - lvl11_x * k
        A = k
        B = -1
        C = b
        d = abs(A * point[0] + B * point[1] + C) / np.sqrt(A ** 2 + B ** 2)
        return d
    else:
        k =(lvl21_y - lvl22_y) / (lvl21_x - lvl22_x)
        b = lvl21_y - lvl21_x * k
        A = k
        B = -1
        C = b
        d = abs(A * point[0] + B * point[1] + C) / np.sqrt(A ** 2 + B ** 2)
        return d
