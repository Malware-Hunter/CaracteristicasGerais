import pandas as pd
import math
from scipy.stats import entropy
from collections import Counter

data = pd.read_csv('C:/Users/SVO-AVELL/CaracteristicasGerais/datasets/KronoDroid_Emulador_Permission_SystemCalls_LIMPO.csv')

#Benignos e Malignos
B = data[(data['class'] == 0)]
M = data[(data['class'] == 1)]

total_of_benign = len(B)
total_of_malware = len(M)

# Lista de caracteristicas
features_list = data.columns

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

#for i in range(1, len(features_list)):
#  Score_feature = 1 - (min(fib(features_list[i]), fim(features_list[i]))/(max(fib(features_list[i]), fim(features_list[i]))))
#  print("Feature: ", features_list[i], "   Score: ", Score_feature)

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

#### Terceira Etapa - Information Gain
def _Ex_a_v_(Ex, a, v, nan=True):
    if nan:
        return [x for x, t in zip(Ex, a) if (isinstance(t, float) and
                                             isinstance(v, float) and
                                             math.isnan(t)        and
                                             math.isnan(v))       or
                                             (t == v)]
    else:
        return [x for x, t in zip(Ex, a) if t == v]

def info_gain(Ex, a, nan=True):
    H_Ex = entropy(list(Counter(Ex).values()))
    sum_v = 0
    for v in set(a):
        Ex_a_v = _Ex_a_v_(Ex, a, v, nan)
        sum_v += (len(Ex_a_v) / len(Ex)) *\
(entropy(list(Counter(Ex_a_v).values())))
    result = H_Ex - sum_v
    return result

if __name__=="__main__":
  
  NFR_list = []
  
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
    print("Feature:", feature, "Score:", Score(feature))
  
  
  print("\nInformation Gain")
  ig_df = pd.DataFrame(columns=["Feature", "IG"])
  for i in NFR_list:
      if i != "class":
          ig_df = pd.concat([ig_df, pd.DataFrame([[i, info_gain(i,data)]], columns=["Feature", "IG"])])
  print(ig_df)