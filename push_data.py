import os
import sys
import pandas as pd
import json
import pymongo
import certifi
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class NetworkDataExtract:
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())  # Convert DataFrame to list of JSON records
            return records
        except Exception as e:
            logging.error("Error in csv_to_json_converter: %s", e)
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database_name, collection_name):
        try:
            db = self.mongo_client[database_name]  # Access the database
            collection = db[collection_name]       # Access the collection
            
            result = collection.insert_many(records)  # Insert records
            return len(result.inserted_ids)           # Return count of inserted records
        except Exception as e:
            logging.error("Unable to insert data into MongoDB: %s", e)
            raise NetworkSecurityException(e, sys)

# Main execution
if __name__ == "__main__":
    FILE_PATH = 'Network_Data/phisingData.csv'
    DATABASE = 'mlops'
    COLLECTION = "NetworkData"
    
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_converter(file_path=FILE_PATH)
    no_of_records = network_obj.insert_data_mongodb(records, DATABASE, COLLECTION)
    
    print(no_of_records)
