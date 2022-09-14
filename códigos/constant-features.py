from sklearn.feature_selection import VarianceThreshold

import numpy as np 
import pandas as pd 
from sklearn.feature_selection import VarianceThreshold
import math
from collections import Counter
from sklearn.model_selection import KFold

data = pd.read_csv('C:/Users/SVO-AVELL/CaracteristicasGerais/datasets/krono.csv')


X_train = data.iloc[:,:-1]
X_test = data.iloc[:,-1] 

sel = VarianceThreshold(threshold=0)
sel.fit(X_train)  # fit finds the features with zero variance

# print the constant features
print(
    len([
        x for x in X_train.columns
        if x not in X_train.columns[sel.get_support()]
    ]))
print([x for x in X_train.columns if x not in X_train.columns[sel.get_support()]])
