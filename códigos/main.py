import math
import sys
from collections import Counter
from argparse import ArgumentParser
from utils import get_base_parser, get_dataset, get_X_y

def parse_args(argv):
    parser = ArgumentParser(parents=[get_base_parser()])
    args = parser.parse_args(argv)
    return args

#### Primeira etapa - Non_Frequent_Reduction
def Non_Frequent_Reduction(permission):
    return len(data[data[permission]==1])/len(data)

##### Segunda Etapa - Feature Discrimination
# fib representa a frequência do recurso fi em arquivos benignos
# fim representa a frequência do recurso fi em arquivos maliciosos
def fib(feature):
   return len(B[B[feature]==1])/len(B)

def fim(feature):
   return len(M[M[feature]==1])/len(M)
"""
  Score(fi) = 0 {frequência igual de ocorrência em ambas as classes; sem discriminação}
  Score(fi) ~ 0 {baixa frequência de ocorrência em qualquer uma das classes; pior característica discriminante}
  Score(fi) ~ 1 {alta frequência de ocorrência em qualquer uma das classes; melhor característica discriminativa}
"""
def Score(feature):
  fb = fib(feature)
  fm = fim(feature)
  score = 1.0 - (min(fb,fm)/max(fb,fm))
  return score

def entropy(labels): #labels --> RÓTULOS
    entropy=0
    label_counts = Counter(labels)
    for label in label_counts:
        prob_of_label = label_counts[label] / len(labels)
        entropy -= prob_of_label * math.log2(prob_of_label)
    return entropy

#### Terceira etapa - Information Gain
def information_gain(data, split_labels):
    info_gain = entropy(data)
    for branched_subset in split_labels:
        info_gain -= len(branched_subset) * entropy(branched_subset) / len(data)
    return info_gain

def get_unique_values(df):
    for column_name in df.columns:
        yield (column_name, df[column_name].unique())

def drop_irrelevant_columns(df):
    # retorna o df sem colunas irrelevantes (colunas com menos de 2 valores possíveis)
    irrelevant_columns = []
    for (column_name, unique_values) in get_unique_values(df):
        if(len(unique_values) < 2):
            irrelevant_columns.append(column_name)
    return df.drop(columns=irrelevant_columns)

if __name__=="__main__":
    args = parse_args(sys.argv[1:])
    data = get_dataset(args)
    X, y = get_X_y(args, get_dataset(args))
    B = data[(data['class'] == 0)]
    M = data[(data['class'] == 1)]
    total_of_benign = len(B)
    total_of_malware = len(M)

    for i in X.columns:
        if i == 'INTERNET':
            X = X.drop(columns=['INTERNET'])
        if i == 'ACCESS_NETWORK_STATE':
            X = X.drop(columns=['ACCESS_NETWORK_STATE'])
        X = drop_irrelevant_columns(X)
    
    ## corte a partir da característica mais frequente
    ft_sum = X.sum()
    ft_max = ft_sum.max()
    th = ft_max * 0.8
    select_ft = list()
    for index, value in ft_sum.items():
        if value >= th:
            select_ft.append(index)
    #print(select_ft)

    ## início do pré-processamento
    print("\nNon-Frequent Reduction --> FREQUÊNCIA DE UMA CARACTERÍSTICA")
    for i in select_ft:
        aux = Non_Frequent_Reduction(i)
        print(i, Non_Frequent_Reduction(i))

    print("\nFeature Discrimination --> SCORE")
    for feature in select_ft:
        print(feature, Score(feature))

    print("\nInformation Gain")
    for i in select_ft:
        if i != "class":
            new_data = information_gain(X,i)
            print(i, new_data)