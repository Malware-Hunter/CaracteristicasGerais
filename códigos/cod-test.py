# INFORMATION GAIN
import numpy as np
import pandas as pd
import math
from collections import Counter
from sklearn.model_selection import KFold

#Função para cálculo da Entropia
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

if __name__=="__main__":
    data = pd.read_csv('C:/Users/SVO-AVELL/CaracteristicasGerais/datasets/drebin215.csv')
    #print(data.head())
    #print(data.isnull().sum()) #selecionar 0s

    #visualizar quantidade de dados
    print("Há {} features no conjunto de dados".format(len(data.columns)))

    for train_index, test_index in KFolders().split(data):
        X_train, X_test = data.loc[train_index,:], data.loc[test_index,:]
        new_data = criar_subconjunto(X_train, encontrar_melhor_subconjunto(X_train)[0]) #contém uma lista de dataframes após a divisão
            
    #CONFERIR SE OS DADOS DE SAIDA ESTÃO CORRETOS