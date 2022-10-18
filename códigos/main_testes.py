import numpy as np 
import pandas as pd
from fast_ml.feature_selection import get_constant_features
from sklearn.feature_selection import mutual_info_classif

data = pd.read_csv('C:/Users/SVO-AVELL/CaracteristicasGerais/datasets/drebin215.csv')
#X = data.iloc[:,:-1]
#y = data.iloc[:,-1]

# Primeira etapa - Non_Frequent_Reduction
def NFR(df):
    constant_features = get_constant_features(df)
    print(constant_features)

    # Remove do dataset as caracteristicas que não estão na lista de constantes
    constant_features_list = constant_features.query("Desc=='Constant'")['Var'].to_list()
    #print(constant_features_list)
    for x in range(0, len(constant_features_list)):
        a = constant_features_list[x] 
        if x not in df:    
            df.drop(columns = [a], inplace=True)
    return df

# Segunda Etapa - Feature Discrimination

#Benignos e Malignos
B = data[(data['class'] == 0)]
M = data[(data['class'] == 1)]

total_of_benign = len(B)
total_of_malware = len(M)

# Lista de caracteristicas
features_list = data.columns

# fib representa a frequência do recurso fi em arquivos benignos
def fib(feature):
   return len(B[B[feature]==1])/len(B)

# fim representa a frequência do recurso fi em arquivos maliciosos
def fim(feature):
   return len(M[M[feature]==1])/len(M)

for i in range(1, len(features_list)):
  Score_feature = 1 - (min(fib(features_list[i]), fim(features_list[i]))/(max(fib(features_list[i]), fim(features_list[i]))))
  print("Feature: ", features_list[i], "   Score: ", Score_feature)

def Score(feature):
  fb = fib(feature)
  fm = fim(feature)
  return 1.0 - (min(fb,fm)/max(fb,fm))

# Terceira Etapa - Information Gain
def calculateMutualInformationGain(features, data):
    feature_names = features.columns
    mutualInformationGain = mutual_info_classif(features, data, random_state = 0)
    data = {"features": feature_names, "score": mutualInformationGain}
    df = pd.DataFrame(data)
    df = df.sort_values(by=['score'], ascending=False)
    return df


if __name__=="__main__":
    for feature in features_list:
        print("Feature:", feature, "Score:", Score(feature))