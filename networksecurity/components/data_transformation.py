import pandas as pd
import numpy as np
import sys, os

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.entity.artifact_entity import DataTransformationArtifact

from networksecurity.entity.config_entity import DataTransformationConfig

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    
    def __init__(self, data_validation_artifact : DataValidationArtifact, 
                 data_transformation_config : DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod    
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_object(cls) -> Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info("Entered get_data_transformer_object method of Transformation class")
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor = Pipeline(steps=[
                ("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)



    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered the initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transaformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            # training Dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            
            # repalcing all -1 values in target column with 0
            target_feature_train_df.replace(-1,0,inplace=True)
            
            # test Dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            
            # replacing all -1 values in target column with 0
            target_feature_test_df.replace(-1,0,inplace=True)
            
            # calling the KNNImputer and Pipeline
            preprocessor = self.get_data_transformer_object()
            
            transformed_input_train_features = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_test_features = preprocessor.transform(input_feature_test_df)
            
            # combine tranform input array and transformed target feature
            train_arr = np.c_[transformed_input_train_features, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_features, np.array(target_feature_test_df)]
            
            # save the numpy array
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array = train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array = test_arr)
            
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            
            # saving preprocessor inside final_model folder
            save_object("final_model/preprocessor.pkl", preprocessor)
            
            # preparing artifacts
            data_transformation_artifacts = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path,
            )
            return data_transformation_artifacts
            
    
        except Exception as e:
            raise NetworkSecurityException(e,sys)