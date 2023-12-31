import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object



class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor_obj.pkl')

class DataTransformation:

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):

        '''
        This function is used to transform the data
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = ["gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]

            numerical_pipeline = Pipeline(
                steps = [("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler(with_mean=False))
                        ]
                )
            
            categorical_pipeline = Pipeline(
                steps = [("imputer", SimpleImputer(strategy="most_frequent")),
                         ("one_hot_encoder", OneHotEncoder()),
                         ("scaler", StandardScaler(with_mean=False))
                         ]
                )

            logging.info("Numerical and categorical pipeline created and scaling and encoding is done")

            preprocessor = ColumnTransformer(
                [
                ("numerical_pipeline", numerical_pipeline, numerical_columns),
                ("categorical_pipeline", categorical_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
          
    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read the train and test data as DataFrame")

            logging.info("Getting Preprocessor object")

            prerocessor_obj = self.get_data_transformer_object()

            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_features_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_features_train_df = train_df[target_column_name]

            input_features_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_features_test_df = test_df[target_column_name]

            logging.info("applying preprocessor object on train dataframe and test dataframe")

            input_features_train_arr = prerocessor_obj.fit_transform(input_features_train_df)
            input_features_test_arr = prerocessor_obj.transform(input_features_test_df)

            train_arr = np.c_[input_features_train_arr, np.array(target_features_train_df)]
            test_arr = np.c_[input_features_test_arr, np.array(target_features_test_df)]

            logging.info("Saved the preprocessor object")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = prerocessor_obj
            )

            return (train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path)
        
        except Exception as e:
            raise CustomException(e, sys)

