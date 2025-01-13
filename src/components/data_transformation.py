import sys


from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException

from src.logger import logging

import os
from src.utils import save_object







class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('dataset',"preprocessor.pkl")




class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer(self):
        try:
           numerical_columns = ["writing_score","reading_score"]
           categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
           ]

           numerical_pipeline = Pipeline(
             steps=[
                ("imputer" , SimpleImputer(strategy='median')),
                ("scaler", StandardScaler(with_mean=False))
             ]
           )


           cat_pipeline = Pipeline(
             steps=[
                ("imputer",SimpleImputer(strategy='most_frequent')),  ##using mode
                ("one_hot_encoder",OneHotEncoder(sparse_output=True)),
                ("scaler",StandardScaler(with_mean=False))
             ]
           )

           logging.info("categorical column encoding completed")
           logging.info("numerical column standaridized encoding completed")
                

           preprocessor = ColumnTransformer(
             [
                ("numerical_pipeline",numerical_pipeline,numerical_columns),
                ("cat_pipeline",cat_pipeline,categorical_columns)
             ]
            
           )
           return preprocessor


          


        except Exception as e:
          raise CustomException(e,sys)

        

    def initiate_data_trnsformation(self,train_path,test_path):
       try:

          train_df = pd.read_csv(train_path)
          test_df = pd.read_csv(test_path)

          logging.info("read the train and test completed")

          logging.info("obtaintaing preprocessing object")

          preprocceing_obj = self.get_data_transformer()

          target_column_names = "math_score"

          numerical_columns = ["writing_score","reading_score"]

          input_feature_train_df = train_df.drop(columns=[target_column_names],axis=1)
          target_feature_train_df = train_df[target_column_names]


          input_feature_test_df = test_df.drop(columns=[target_column_names],axis=1)
          target_feature_test_df = test_df[target_column_names]




          input_feature_train_array =  preprocceing_obj.fit_transform(input_feature_train_df)
          input_feature_test_array = preprocceing_obj.transform(input_feature_test_df)



          train_arr = np.c_[
             input_feature_train_array,np.array(target_feature_train_df)
          ]


          test_arr = np.c_[
             input_feature_test_array,np.array(target_feature_test_df)
          ]


          logging.info("saved preproccessing object.")


          ##save pickle file
          save_object(
             file_path = self.data_transformation_config.preprocessor_obj_file_path ,
             obj = preprocceing_obj

          )

          return(
             train_arr,
             test_arr,
             self.data_transformation_config.preprocessor_obj_file_path  ##pickle file path
          )


       except Exception as e:
          raise CustomException(e,sys)



