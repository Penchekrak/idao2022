def classificate_class2(target):
    if 0.39 <= target < 0.43:
        return 1
    if 0.34 <= target < 0.38:
        return 2
    if 0.27 <= target <= 0.31:
        return 3
    return 0

def classificate_class2_wide(target):
    if 0.37 <= target < 0.434:
        return 1
    if 0.33 <= target < 0.37:
        return 2
    if 0.267 <= target <= 0.321:
        return 3
    return 0

def convert_group_to_target_class2(group):
    if group == 1:
        return 0.41
    elif group == 2:
        return 0.36
    elif group == 3:
        return 0.29

def classificate_class3(target):
    if 1.08 <= target <= 1.12:
        return 1
    if 1. <= target <= 1.04:
        return 2
    if 0.93 <= target <= 0.97:
        return 3
    if 0.635 <= target <= 0.675:
        return 4
    return 0

def classificate_class3_wide(target):
    if 1.08 <= target <= 1.12:
        return 1
    if 1. <= target <= 1.04:
        return 2
    if 0.93 <= target <= 0.97:
        return 3
    if 0.635 <= target <= 0.675:
        return 4
    return 0

def convert_group_to_target_class3(group):
    if group == 1:
        return 1.10
    elif group == 2:
        return 1.2
    elif group == 3:
        return 0.95
    elif group == 4:
        return 0.655

def classificate_class4(target): # maybe add class
    if 0.4 <= target <= 0.44:
        return 1
    if 0.345 <= target <= 0.365:
        return 2
    if 0.25 <= target <= 0.29:
        return 3
    return 0

def convert_group_to_target_class4(group):
    if group == 1:
        return 0.42
    elif group == 2:
        return 0.355
    elif group == 3:
        return 0.27

def classificate_class5(target):
    if 0.39 <= target <= 0.43:
        return 1
    if 0.335 <= target <= 0.375:
        return 2
    if 0.28 <= target <= 0.31:
        return 3
    return 0

def convert_group_to_target_class5(group):
    if group == 1:
        return 0.409 #0.4
    elif group == 2:
        return 0.355 #0.35
    elif group == 3:
        return 0.295
