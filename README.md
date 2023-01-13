# Recriação e adaptação do experimento: A multi-tiered feature selection model for android malware detection based on Feature discrimination and Information Gain
_MTmain_ad.py_ recria o experimento fazendo adapatações em relação ao experimento original.
## As adaptações foram adicionadas na primeita etapa do pré-processamento do conjunto de dados:
# Adaptações
- Remoção de características comuns: INTERNET e ACCESS_NETWORK_STATE
- Filtragem das características a partir da característica mais frequente
- Para uma melhor filtragem de conjuntos menores, testes foram realizado usando valores menores de _threshol_: 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50
# Tais adaptações foram tomadas por conta da distribuição das características no conjunto de dados
## Link para visualização de resultados testes [Tabelas](https://docs.google.com/spreadsheets/d/1dCuyj8D3xlrWKMQDF5hm8E2GYLfKQg_YCWt3DJSFt88/edit#gid=0)
