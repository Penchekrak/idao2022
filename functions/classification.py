from xgboost import XGBClassifier, XGBRegressor
from functions.features import distance_features

def predict_target_on_class(class_n, test_class_n, n, n_estim_clf=10, n_estim_reg=10):
    class_n['group'] = class_n['targets'].apply(lambda x: classificate_class(x, n))
    class_n = class_n[class_n.group != 0]
    
    class_n = distance_features(class_n)
    test_class_n = distance_features(test_class_n)
    
    for i in range(3):
        class_n['dist' + str(i+1)] = class_n[['Mo_S_dist', 'S_Se_dist', 'Mo_Se_dist']].apply(lambda row: sorted(row)[i], axis=1)
        test_class_n['dist' + str(i+1)] = test_class_n[['Mo_S_dist', 'S_Se_dist', 'Mo_Se_dist']].apply(lambda row: sorted(row)[i], axis=1)

    feature_list = ['dist1', 'dist2', 'dist3']
    clf = XGBClassifier(n_estimators=n_estim_clf, random_state=0xC0FFEE)
    clf.fit(class_n[feature_list], class_n['group'])
    test_class_n['group'] = clf.predict(test_class_n[feature_list])
    
    feature_list = ['dist1', 'dist2', 'dist3', 'group']
    reg = XGBRegressor(n_estimators=n_estim_reg, random_state=0xC0FFEE)
    reg.fit(class_n[feature_list], class_n['targets'])
    
    class_n_predict_target = reg.predict(test_class_n[feature_list])
    return class_n_predict_target

def classificate_class(target, n):
    if n == 2:
        if target >= 0.375 and target < 0.44:
            return 1
        if target >= 0.335 and target < 0.375:
            return 2
        if target >= 0.26 and target <= 0.321:
            return 3
        return 0
    elif n == 3:
        if target >= 1.07 and target <= 1.13:
            return 1
        if target >= 0.985 and target <= 1.06:
            return 2
        if target >= 0.93 and target <= 0.97:
            return 3
        if target >= 0.635 and target <= 0.68:
            return 4
        return 0
    elif n == 4:
        if target >= 0.4 and target <= 0.44:
            return 1
        if target >= 0.345 and target <= 0.365:
            return 2
        if target >= 0.25 and target <= 0.31:
            return 3
        return 0
    elif n == 5:
        if target >= 0.375 and target <= 0.44:
            return 1
        if target >= 0.325 and target <= 0.375:
            return 2
        if target >= 0.267 and target <= 0.317:
            return 3
        return 0