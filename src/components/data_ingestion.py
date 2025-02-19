import os
import sys

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


from src.exception import CustomException 
from src.logger import logging

import pandas as pd

from sklearn.model_selection import train_test_split

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from dataclasses import dataclass ##create class variables



@dataclass #DECORATION DIRECTLY DEFINE IN CLASS VARIABLE

class DataIngestionConfig:
    train_data_path: str = os.path.join('dataset',"train.csv")   ##output store
    test_data_path: str = os.path.join('dataset',"test.csv")
    raw_data_path : str = os.path.join('dataset',"data.csv")



class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

           
    def initiate_data_ingestion(self):

        logging.info("entered the data ingestion")
        try:
            
            df = pd.read_csv(r'C:\Users\sanoj\OneDrive\Desktop\ML PROJECT 2025\notebook\data\stud.csv')

            #logging.info("read the dataset as dataframe")



            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)


            #logging.info("train test splitting initiated!")

            train_set, test_set = train_test_split(df,test_size=0.2,random_state=42)

            test_set.to_csv(self.ingestion_config.test_data_path,index = False,header = True)
            train_set.to_csv(self.ingestion_config.train_data_path, index= False , header = True)

            #logging.info("Ingestion of data is completed")
      
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                
            )


        except Exception as e:
            raise CustomException(e,sys)            
          


if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transforamtion = DataTransformation()
    data_transforamtion.initiate_data_trnsformation(train_data,test_data)

    