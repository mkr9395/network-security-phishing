from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation

from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


import sys

if __name__=='__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)       
        
        logging.info("Initiated Data Ingestion")       
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Completed Data Ingestion\n")
        print(dataingestionartifact) 
        
        
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        
        logging.info("Initiated Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Completed Data Validation\n")
        print(data_validation_artifact) 
        
        
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        
        logging.info("Initiated Data Transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Completed Data Transformation")
        print(data_transformation_artifact) 
        
        
    except Exception as e:
           raise NetworkSecurityException(e,sys)