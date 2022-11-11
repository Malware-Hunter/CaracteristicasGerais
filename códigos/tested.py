import pandas as pd

data = pd.read_csv(r'datasets\drebin_215_permissions.csv')
X = data.iloc[:,:-1]
Y = data.iloc[:,-1]

df_clone=data[:] 


print(data.columns)

data = data.drop(columns=['INTERNET'])

data = data.drop(columns=['ACCESS_NETWORK_STATE'])

print(data.columns)
