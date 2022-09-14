import numpy as np 
import pandas as pd 
from sklearn.feature_selection import VarianceThreshold
import math
from collections import Counter
from sklearn.model_selection import KFold

##
def excluir_feaures_constantes():
    #usando sklearn variancethreshold para encontrar recursos constantes
    sel = VarianceThreshold(threshold=0)
    sel.fit(X_train) #fit encontra os recursos com variância zero

    ## get_support é um vetor booleano que indica quais recursos são retidos
    # se somarmos get_support, obtemos o número de recursos que não são constantes
    #print(sum(sel.get_support()))
    
    #características constantes
    print(
        len([
            x for x in X_train.columns
            if x not in X_train.columns[sel.get_support()]
        ]))

    [x for x in X_train.columns if x not in X_train.columns[sel.get_support()]]

    #descartando colunas dos conjuntos train e test, constantes
    X_train = sel.transform(X_train)
    X_test = sel.transform(X_test)

    #checar a exclusão 
    return X_train.shape, X_test.shape

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

def information_gain():
    for train_index, test_index in KFolders().split(data):
        X_train, X_test = data.loc[train_index,:], data.loc[test_index,:]
        new_data = criar_subconjunto(X_train, encontrar_melhor_subconjunto(X_train)[0]) #contém uma lista de dataframes após a divisão
        return new_data

if __name__=="__main__":
    data = pd.read_csv('/home/savi/CaracteristicasGerais/datasets/androcrawl.csv')
    #visualizar quantidade de dados - def
    #print(data.head())
    #print(data.isnull().sum()) #selecionar 0s
    print("Há {} features no conjunto de dados".format(len(data.columns)))

    X_train = data.iloc[:,:-1]
    X_test = data.iloc[:,-1] 
   
    #excluir_feaures_constantes()
    #A PARTIR DESSE PONTO, OCORREU A REMOÇÃO DE RECURSOS CONSTANTES
    information_gain()
    