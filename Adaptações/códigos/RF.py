import pandas as pd
import numpy as np
import timeit
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def RF(data_result, dff):
    from sklearn import metrics
    state = np.random.randint(100)
    X = data_result
    Y = dff['class'] 

    start_time = timeit.default_timer()
    #split between train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, Y, stratify=Y, test_size=0.3,random_state=1)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.3, random_state=1)

    RF = RandomForestClassifier()
    RF.fit(X_train,y_train)

    #prediction labels for X_test
    y_pred=RF.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    elapsed_time = timeit.default_timer() - start_time

    accuracy = metrics.accuracy_score(y_test, y_pred)
    precision = metrics.precision_score(y_test, y_pred, zero_division = 0)
    recall = metrics.recall_score(y_test, y_pred, zero_division = 0)
    f1_score = metrics.f1_score(y_test, y_pred, zero_division = 0)
    fpr = fp/(fp+tn)

    data = [{'Time':elapsed_time,'Accuracy':accuracy,'Precision':precision,'Recall':recall,'F1_Score':f1_score,'Fpr':fpr}]
    df = pd.DataFrame(data)
    return df
