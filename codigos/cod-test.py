# INFORMATION GAIN
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math
from collections import Counter

# Os arquivos de dados de entrada estão disponíveis no diretório "../input/".
# Por exemplo, executar isso (clicando em executar ou pressionando Shift+Enter) listará os arquivos no diretório de entrada


data = pd.read_csv('C:/Users/SVO-AVELL/CaracteristicasGerais/datasets/balanceados/drebin_215_permissions.csv')
#print(data.head())
#print(data.isnull().sum()) #Selecionar 0s

#A ideia por trás da construção de árvores é encontrar a melhor característica para dividir que gere o maior ganho de informação ou forneça a menor
#incerteza nas folhas seguintes

#Entropia
#Ainda encontraremos o ganho de informação, usando entropias ponderadas e escolheremos o atributo que proporcionou o ganho máximo de informação.
print("Há {} features no dataset".format(len(data.columns)))

#Função para cálculo da Entropia
def entropy(labels):
    entropy=0
    label_counts = Counter(labels)      #Um Counter é um dict e pode receber um objeto iterável ou um mapa como argumento para realizar a contagem de seus elementos.
    for label in label_counts:
        prob_of_label = label_counts[label] / len(labels)
        entropy -= prob_of_label * math.log2(prob_of_label)
    return entropy

#Função para cálculo do Ganho
def information_gain(starting_labels, split_labels):
    info_gain = entropy(starting_labels)
    for branched_subset in split_labels:        #subconjunto
        info_gain -= len(branched_subset) * entropy(branched_subset) / len(starting_labels)
    return info_gain

def split(dataset, column):
    split_data = []
    col_vals = data[column].unique() #Este método de geração de árvore só funciona com valores discretos
    for col_val in col_vals:
        split_data.append(dataset[dataset[column] == col_val])
    return(split_data)

def find_best_split(dataset):
    best_gain = 0
    best_feature = 0
    features = list(dataset.columns)
    features.remove('class')
    for feature in features:
        split_data = split(dataset, feature)
        split_labels = [dataframe['class'] for dataframe in split_data]
        gain = information_gain(dataset['class'], split_labels)
        if gain > best_gain:
            best_gain, best_feature = gain, feature
    print(best_feature, best_gain)
    return best_feature, best_gain

new_data = split(data, find_best_split(data)[0]) #contém uma lista de dataframes após a divisão

# CRIAR UMA CHAMADA RECURSIVA PARA CADA SUBCONJUNTO