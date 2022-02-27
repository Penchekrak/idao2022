def classificate_class2(target):
    if target >= 0.39 and target < 0.43:
        return 1
    if target >= 0.34 and target < 0.38:
        return 2
    if target >= 0.27 and target <= 0.31:
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
    if target >= 1.08 and target <= 1.12:
        return 1
    if target >= 1. and target <= 1.04:
        return 2
    if target >= 0.93 and target <= 0.97:
        return 3
    if target >= 0.635 and target <= 0.675:
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
    if target >= 0.4 and target <= 0.44:
        return 1
    if target >= 0.345 and target <= 0.365:
        return 2
    if target >= 0.25 and target <= 0.29:
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
    if target >= 0.39 and target <= 0.43:
        return 1
    if target >= 0.335 and target <= 0.375:
        return 2
    if target >= 0.28 and target <= 0.31:
        return 3
    return 0

def convert_group_to_target_class5(group):
    if group == 1:
        return 0.409 #0.4
    elif group == 2:
        return 0.355 #0.35
    elif group == 3:
        return 0.295
