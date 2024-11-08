import os, sys
import pandas as pd
import numpy as np
import mlflow


from networksecurity.entity.artifact_entity import DataTransformationArtifact
from networksecurity.entity.artifact_entity import ModelTrainerArtifact

from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.utils import save_object, load_object, load_numpy_array_data
from networksecurity.utils.main_utils.utils import evaluate_models

from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier

from sklearn.metrics import f1_score, precision_score, recall_score


class ModelTrainer:
    
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self, best_model, classication_metric):
        mlflow.set_tracking_uri("http://localhost:5000")
        with mlflow.start_run():
            f1_score = classication_metric.f1_score
            precision_score = classication_metric.precision_score
            recall_score = classication_metric.recall_score
            
            mlflow.log_metrics({'f1_score': f1_score, 'precision_score': precision_score, 'recall_score': recall_score})
            mlflow.sklearn.log_model(best_model, "model")
            
    
    
    
    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                    "Random Forest": RandomForestClassifier(verbose=1),
                    "Decision Tree": DecisionTreeClassifier(),
                    "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                    "Logistic Regression": LogisticRegression(verbose=1),
                    "AdaBoost": AdaBoostClassifier(),
                }
            
            params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            
            model_report: dict = evaluate_models(X_train = X_train, y_train = y_train, X_test = X_test, y_test = y_test,
                                                models = models, params = params)
            
            best_model_score: float = max(sorted(model_report.values()))
            
            best_model_name = list(models.keys())[list(model_report.values()).index(best_model_score)] 
            
            best_model = models[best_model_name]
            
            logging.info(f"########################## best model selected is : {best_model}")
            
            y_train_pred = best_model.predict(X_train)
            
            classification_train_metric = get_classification_score(y_true = y_train, y_pred = y_train_pred)
            
            ## Track the experiments with mlflow -> for train data
            self.track_mlflow(best_model, classification_train_metric)
            
            y_test_pred = best_model.predict(X_test)
            
            classification_test_metric = get_classification_score(y_true = y_test, y_pred = y_test_pred)
            
            ## Track the experiments with mlflow -> for test data
            self.track_mlflow(best_model, classification_test_metric)
            
            preprocessor = load_object(file_path = self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path , exist_ok=True )
            
            Network_Model = NetworkModel(preprocessor = preprocessor, model = best_model)
            
            save_object(self.model_trainer_config.trained_model_file_path, obj = Network_Model)
            
            
            ## Model Trainer Artifact
            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                                train_metric_artifact = classification_train_metric,
                                test_metric_artifact = classification_test_metric)
            
            logging.info(f"Model trainer artifact : {model_trainer_artifact}")
            
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
           
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
            
            
            model_trainer_artifact = self.train_model(X_train, y_train, X_test=X_test, y_test=y_test)
            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        