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

if __name__=="__main__":
    args = parse_args(sys.argv[1:])
    data = get_dataset(args)
    X, y = get_X_y(args, get_dataset(args))
    B = data[(data['class'] == 0)]
    M = data[(data['class'] == 1)]
    total_of_benign = len(B)
    total_of_malware = len(M)
    select_ft = list()
    ## início do pré-processamento

    for i in data.columns:
        aux = Non_Frequent_Reduction(i)
        if aux >= 0.8:
            print(i, Non_Frequent_Reduction(i))
            select_ft.append(i)

    for feature in select_ft:
        print(feature, Score(feature))

    print("\nInformation Gain")
    select_ft_count = 0 
    for i in select_ft:
        if i != "class":
            new_data = information_gain(X,i)
            print(i, new_data)
            select_ft_count+=1 
    print("QUANTIDADE DE FEATURES SELECIONADAS --> ",select_ft_count)