import pandas as pd
import numpy as np
import pymongo
from dotenv import load_dotenv
import os
import json
import sys
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

print(MONGODB_URI)


import certifi
ca = certifi.where()

from src.exception.exception import CustomerException
from src.logging.logging import logging



class ETL_pipeline:

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomerException(e,sys)
        

    def csv_to_json_convertor(self,file_path:str)->json:

        """
        This function converts csv file to json format

        """    

        try:
            logging.info("csv to json conversion started")

            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)

            records = list(json.loads(data.T.to_json()).values())
            logging.info("csv to json conversion completed")

            return records
        
        except Exception as e:
            logging.error("Error occurred in csv to json conversion")
            raise CustomerException(e,sys)
        

    def push_data_to_mongodb(self,records:json,database_name:str,collection_name:str):

        try:
            
            self.records = records
            self.database_name = database_name
            self.collection_name = collection_name

            logging.info("Data push to Mongodb started")
            self.mongo_client = pymongo.MongoClient(MONGODB_URI)
            self.database = self.mongo_client[self.database_name]
            self.collection = self.database[self.collection_name]

            self.collection.insert_many(self.records)
            logging.info("Data push to Mongodb completed")
            return len(self.records)


        except Exception as e:
            logging.error("Error occurred while pushing data to mongodb")
            raise CustomerException(e,sys)



if __name__=="__main__":
    FILE_PATH = "data\Telco-Customer-Churn.csv"
    DATABASE = "TelcoCustomerChurnDB"
    COLLECTION = "CustomerChurnCollection"

    etl = ETL_pipeline()
    records = etl.csv_to_json_convertor(file_path=FILE_PATH)
    number_of_records=etl.push_data_to_mongodb(records=records,database_name=DATABASE,collection_name=COLLECTION)
    print(f"Number of records inserted to Mongodb: {number_of_records}")



