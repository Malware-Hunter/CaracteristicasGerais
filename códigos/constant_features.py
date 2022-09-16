### REMOVER FEATURES COM BAIXA FREQUÊNCIA
### O CÓDIGO GERA UM VETOR CONTENDO AS FEATURES CONSTANTES

import numpy as np
from sklearn.feature_selection import VarianceThreshold
import pandas as pd

FEATURES_CONSTANTES = []
data = pd.read_csv('C:/Users/SVO-AVELL/CaracteristicasGerais/datasets/krono.csv')
print(data)
print("################################################################")
X_train = data.iloc[:,:-1]
#X_test = data.iloc[:,-1] 

sel = VarianceThreshold(threshold=0)
sel.fit(X_train)  # fit encontra as features com variancia igual a zero

for x in X_train.columns:
        if x not in X_train.columns[sel.get_support()]:
            FEATURES_CONSTANTES.append(x)

#print(len(FEATURES_CONSTANTES))
#print(FEATURES_CONSTANTES)
