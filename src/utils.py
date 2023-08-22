import os
import sys
import pandas as pd
import numpy as np
import dill

from src.exception import CustomException
from sklearn.metrics import r2_score




def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as f:
            dill.dump(obj,f)

    except Exception as e:
        raise CustomException(e, sys)
    

def evaluate_models(X_train,X_test,y_train,y_test,models):
    try:

        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        report = {}

        for m in models:
            model = models[m]
            model.fit(X_train, y_train) # training the model

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test) 

            train_r2 = r2_score(y_train, y_train_pred)
            test_r2 = r2_score(y_test, y_test_pred) 

            report[m] = {'train_r2': train_r2, 'test_r2': test_r2}
           
        return report
    



        pass
    except Exception as e:
        raise CustomException(e, sys)
