# pushing data to MongoDB

import os
import sys

from dotenv import load_dotenv # call environment variables
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

print(MONGO_DB_URL)


import pandas
import numpy
import json
import pymongo
import certifi # set of roots certificate for secure https connection, here for mongodb
ca = certifi.where()

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.drop_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values()) # list of json records of dictionary
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database,
            self.collection = collection,
            self.records = records,
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL),
            self.database = self.mongo_client[self.database]
            
            self.collection = self.mongo_client[self.collection]
            
            self.connection.insert_many(self.records)
            
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)
            

if __name__ == "__main__":
    FILE_PATH = 'Network_Data\phisingData.csv'
    DATABASE = 'mlops'
    Collection = "NetworkData"
    
    network_obj = NetworkDataExtraction()
    network_obj.csv_to_json_converter(file_path = FILE_PATH)
    no_of_records = network_obj.insert_data_mongodb(records = records, database = DATABASE, Collection=Collection)
    
    print(no_of_records)
    
    