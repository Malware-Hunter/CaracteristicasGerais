import pandas as pd 
import numpy as np 
import math
from collections import Counter

#### Primeira etapa - Non_Frequent_Reduction
def NFR(permission):
    return len(data[data[permission]==1])/len(data)

##### Segunda Etapa - Feature Discrimination
# fib representa a frequência do recurso fi em arquivos benignos
def fib(feature):
   return len(B[B[feature]==1])/len(B)

# fim representa a frequência do recurso fi em arquivos maliciosos
def fim(feature):
   return len(M[M[feature]==1])/len(M)

def Score(feature):
  fb = fib(feature)
  fm = fim(feature)
  """
  Score(fi) = 0 {frequência igual de ocorrência em ambas as classes; sem discriminação}
  Score(fi) ~ 0 {baixa frequência de ocorrência em qualquer uma das classes; pior característica discriminante}
  Score(fi) ~ 1 {alta frequência de ocorrência em qualquer uma das classes; melhor característica discriminativa}
  """
  score = 1.0 - (min(fb,fm)/max(fb,fm))
  return score

def entropy(labels):
    entropy=0
    label_counts = Counter(labels)
    for label in label_counts:
        prob_of_label = label_counts[label] / len(labels)
        entropy -= prob_of_label * math.log2(prob_of_label)
    return entropy

#### Terceira etapa - Non_Frequent_Reduction
def information_gain(starting_labels, split_labels):
    info_gain = entropy(starting_labels)
    for branched_subset in split_labels:
        info_gain -= len(branched_subset) * entropy(branched_subset) / len(starting_labels)
    return info_gain
	
if __name__=="__main__":
	
	data = pd.read_csv(r'C:\Users\SVO-AVELL\CaracteristicasGerais\datasets\KronoDroid_Emulador_Permission_SystemCalls_LIMPO.csv')
	X = data.iloc[:,:-1]
	Y = data.iloc[:,-1]
	NFR_list = []

	#Benignos e Malignos
	B = data[(data['class'] == 0)]
	M = data[(data['class'] == 1)]

	total_of_benign = len(B)
	total_of_malware = len(M)

	# Lista de caracteristicas
	features_list = data.columns

	print("Non-Frequent Reduction")
	permission = data.columns
	for i in permission:
		aux = NFR(i)
		if aux >= 0.8:
			print(i, "Frequencia ", NFR(i))
			NFR_list.append(i)

	print("\nFeature Discrimination")
	#print(NFR_list)
	for feature in NFR_list:
		print(feature, "Score:", Score(feature))

	print("\nInformation Gain")
	for i in NFR_list:
		if i != "class":
			new_data = information_gain(X,i)
			print(i, new_data)
