import os, sys
import pandas as pd
import numpy as np


from networksecurity.entity.artifact_entity import DataTransformationArtifact
from networksecurity.entity.artifact_entity import ModelTrainerArtifact

from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.utils import save_object, load_object, load_numpy_array_data

from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier

from sklearn.metric import f1_score, precision_score, recall_score


class ModelTrainer:
    
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
        
        
        
    
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        
        try:
            train_file_path: str = self.data_transformation_artifact.transformed_train_file_path
            test_file_path: str = self.data_transformation_artifact.transformed_test_file_path

            # loading trin and test array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]   
            )
            
            
            model = self.train_model(X_train, y_train)
            y_pred = model.predict(X_test)
            
            
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        