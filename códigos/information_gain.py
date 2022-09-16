import numpy as np 
import pandas as pd 
from sklearn.feature_selection import VarianceThreshold
import math
from collections import Counter
from sklearn.model_selection import KFold

##Função para cálculo da Entropia
def entropia(labels):
    entropy=0
    label_counts = Counter(labels)      # Um Counter é um dict e pode receber um objeto iterável ou um mapa como argumento para realizar a contagem de seus elementos
    for label in label_counts:
        prob_of_label = label_counts[label] / len(labels)
        entropy -= prob_of_label * math.log2(prob_of_label)
    return entropy

#Função para cálculo do Ganho
def information_gain(starting_labels, split_labels):
    info_gain = entropia(starting_labels)
    for branched_subset in split_labels:        #subconjunto
        info_gain -= len(branched_subset) * entropia(branched_subset) / len(starting_labels)
    return info_gain

def encontrar_melhor_subconjunto(dataset):
    best_gain = 0
    best_feature = 0
    features = list(dataset.columns)
    features.remove('class')
    for feature in features:
        subconjunto = criar_subconjunto(dataset, feature)
        split_labels = [dataframe['class'] for dataframe in subconjunto]
        gain = information_gain(dataset['class'], split_labels)
        if gain > best_gain:
            best_gain, best_feature = gain, feature
    print(best_feature, best_gain)
    return best_feature, best_gain

def criar_subconjunto(dataset, column):
    subconjunto = [] #dados divididos
    col_vals = data[column].unique() #Este método de geração de árvore só funciona com valores discretos
    for col_val in col_vals:
        subconjunto.append(dataset[dataset[column] == col_val])
    return(subconjunto)

# FOLDERS
def KFolders():
    kf = KFold(n_splits=10, shuffle=False) # set a divisão em 10 folds
    kf.get_n_splits(data) # retorna o número de iterações divididas na validação cruzada
    return (kf)

def information_gain(starting_labels, split_labels):
    info_gain = entropia(starting_labels)
    for branched_subset in split_labels:
        info_gain -= len(branched_subset) * entropia(branched_subset) / len(starting_labels)
    return info_gain

if __name__=="__main__":
    data = pd.read_csv('C:/Users/SVO-AVELL/CaracteristicasGerais/datasets/krono.csv')
    #visualizar quantidade de dados - def
    #print(data.head())
    #print(data.isnull().sum()) #selecionar 0s
    print("Há {} features no conjunto de dados".format(len(data.columns)))

    X_train = data.iloc[:,:-1]
    X_test = data.iloc[:,-1] 
   
    #excluir_feaures_constantes()
    #A PARTIR DESSE PONTO, OCORREU A REMOÇÃO DE RECURSOS CONSTANTES
    
    encontrar_melhor_subconjunto(X_train)
    