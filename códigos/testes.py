import pandas as pd 
import numpy as np 
import math
from collections import Counter

def gmf(permissions):
	count = {}
	for p in permissions:
		if p in count:
			count[p] +=1
		else:
			count[p] = 1
	sorted_count = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_count

def get80(sorted_count):
	eighty_percet = int(len(sorted_count)*0.8)
	return sorted_count[:eigthy_percent]

#### Primeira etapa - Non_Frequent_Reduction
def NFR(permission):
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

#### Terceira etapa - Non_Frequent_Reduction
def information_gain(data, split_labels):
    info_gain = entropy(data)
    for branched_subset in split_labels:
        info_gain -= len(branched_subset) * entropy(branched_subset) / len(data)
    return info_gain
	
if __name__=="__main__":	
	data = pd.read_csv(r'caminho_do_dataset')
	X = data.iloc[:,:-1]
	Y = data.iloc[:,-1]
	NFR_list = []

	#Benignos e Malignos
	B = data[(data['class'] == 0)]
	M = data[(data['class'] == 1)]

	total_of_benign = len(B)
	total_of_malware = len(M)

	# Lista de nomes das caracteristicas
	features_list = data.columns

	print("Non-Frequent Reduction --> FREQUÊNCIA DE UMA CARACTERÍSTICA")
	permission = data.columns
	for i in permission:
		aux = NFR(i)
		if aux >= 0.8:
			print(i, NFR(i))
			NFR_list.append(i)

	print("\nFeature Discrimination --> SCORE")
	#print(NFR_list)
	for feature in NFR_list:
		print(feature, Score(feature))

	print("\nInformation Gain")
	for i in NFR_list:
		if i != "class":
			new_data = information_gain(X,i)
			print(i, new_data)
