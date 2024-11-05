# configuration details
from datetime import datetime
import os
from networksecurity.constant import training_pipeline

# to test whether the file is imported properly
print(training_pipeline.FILE_NAME)
print(training_pipeline.ARTIFACT_DIR)

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        """
    Configuration class for the training pipeline.

    Attributes:
        pipeline_name (str): Name of the pipeline.
        artifact_name (str): Name of the artifact directory.
        artifact_dir (str): Full path of the artifact directory, including timestamp.
        timestamp (str): Timestamp of pipeline execution.

    Parameters:
        timestamp (datetime, optional): Timestamp for pipeline execution. Defaults to current datetime.
    """
        # Convert timestamp to string format 
        # timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        timestamp = 'Folder'
        
        # Get pipeline name from training_pipeline constants folder
        self.pipeline_name = training_pipeline.FILE_NAME
        
        # Get artifact name from training_pipeline constants folder
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        
        # Construct artifact directory path using artifact name and timestamp
        self.artifact_dir = os.path.join(self.artifact_name)
        # self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        
        self.model_dir=os.path.join("final_model")
        
        # Store timestamp for future reference
        self.timestamp = timestamp


class DataIngestionConfig:
    """
    Configuration class for data ingestion.
    Parameters:
        training_pipeline_config (TrainingPipelineConfig): Configuration object for the training pipeline.
    """
    
    def __init__(self, training_pipeline_config: TrainingPipelineConfig): #training_pipeline_config is created above
        
        # Initialize data ingestion directory path using artifact directory from training pipeline config
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir,
                                                    training_pipeline.DATA_INGESTION_DIR_NAME)
        
        # Define feature store file path within data ingestion directory
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir, 
                                                         training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)
        
        # Define training file path within data ingestion directory
        self.training_file_path: str = os.path.join(self.data_ingestion_dir, 
                                                    training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME)
        
        # Define testing file path within data ingestion directory
        self.testing_file_path: str = os.path.join(self.data_ingestion_dir, 
                                                   training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME)
        
        # Define train-test split ratio
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT
        
        # Define collection name for database interactions
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        
        # Define database name for database interactions
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME
        
    

class DataValidationConfig:
    """
    Class representing the configuration for data validation
    """
    # Initializes the data validation configuration
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        
        # Directory path for data validation artifacts
        self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, 
                                                     training_pipeline.DATA_VALIDATION_DIR_NAME)
        
        # Directory path for valid data
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        
        # Directory path for invalid data
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        
        # File path for valid training data
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        
        # File path for valid testing data
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        
        # File path for invalid training data
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        
        # File path for invalid testing data
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
        
        #  Path to the data drift report file, used to track changes in data distribution
        self.drift_report_file_path: str = os.path.join(self.data_validation_dir,
                                                        training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                                                        training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        
        
class DataTransformationConfig:
    
    """
    Configuration class for data transformation.
    
    This class initializes the directory paths and file paths required for data transformation.
    """
    def __init__(self, training_pipeline_config : TrainingPipelineConfig):
        """
        Initializes the DataTransformationConfig instance.
        Parameters:
        ----------
        training_pipeline_config (TrainingPipelineConfig): Configuration object for training pipeline.
        """
        # Set data transformation directory path
        self.data_transformation_dir: str =     