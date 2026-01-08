import sys

from src.exception.exception import CustomerException
from src.logging.logging import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import Data_transformation
from src.components.data_validation import Data_Validation
from src.components.model_train import ModelTrainer
from src.components.model_evaluation import ModelEvaluation


from src.entity.config_entity.config_entity import (
                                                    Data_Ingestion_Config,
                                                    Data_Transformation_Config,
                                                    Data_Validation_Config,
                                                    Model_Train_Config,
                                                    ModelEvaluationConfig,
                                                    Training_Pipeline_Config
                                                    )

class TrainingPipeline:

    def __init__(self):
        try:
            self.training_pipeline_config = Training_Pipeline_Config()
        except Exception as e:
            raise CustomerException(e,sys)
        

    def start_data_ingestion(self):

        try: 

            logging.info("========== Data Ingestion Started ==========")   

            data_ingestion_config = Data_Ingestion_Config(training_pipeline_config=self.training_pipeline_config) 
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("========== Data Ingestion Completed ==========")

            return data_ingestion_artifact

        except Exception as e:
            raise CustomerException(e,sys)


    def start_data_validation(self,data_ingestion_artifact):

        try:
            
            logging.info("========== Data Validation Started ==========")

            data_validation_config = Data_Validation_Config(training_pipeline_config=self.training_pipeline_config)
            data_validation = Data_Validation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("========== Data Validation Completed ==========")

            return data_validation_artifact


        except Exception as e:
            raise CustomerException(e,sys)

    def start_data_transformation(self,data_validation_artifact):

        try:
            
            logging.info("========== Data Transformation Started ==========")

            data_tranformation_config = Data_Transformation_Config(training_pipeline_config=self.training_pipeline_config)
            data_tranformation = Data_transformation(data_transformation_config=data_tranformation_config,data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_tranformation.initiate_data_transformation()
            logging.info("========== Data Transformation Completed ==========")

            return data_transformation_artifact

        except Exception as e:
            raise CustomerException(e,sys)


    def start_model_training(self,data_transformation_artifact):

        try:
            
            logging.info("========== Model Training Started ==========")

            model_training_config = Model_Train_Config(training_pipeline_config=self.training_pipeline_config)
            model_training = ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_train_config=model_training_config)
            model_training_artifact = model_training.initiate_model_trainer()

            logging.info("========== Model Training Completed ==========")

            return model_training_artifact


        except Exception as e:
            raise CustomerException(e,sys)


    def start_model_evaluation(self,data_transfromation_artifact,model_training_artifact):
        try:
            logging.info("========== Model Evaluation Started ==========")
            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            model_evaluation = ModelEvaluation(model_evaluation_config=model_evaluation_config,
                                                data_transformation_artifact=data_transfromation_artifact,
                                                model_train_artifact=model_training_artifact
                                                )
            
            model_evaluation_artifact = model_evaluation.evaluate()

            if not model_evaluation_artifact.is_model_accepted:
                raise Exception("Train model rejected by evaluation criteria")
            
            logging.info("========== Model Evaluation Completed ==========")

            return model_evaluation_artifact

        except Exception as e:
            raise CustomerException(e,sys)


    def run_pipeline(self):
        """
            Entry point for the pipeline

        """          

        try:
            
            logging.info("========== Training Pipeline Started ==========")


            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_training_artifact = self.start_model_training(data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_transformation_artifact,model_training_artifact)

            logging.info(
                f"Pipeline completed successfully | "
                f"Best Model: {model_training_artifact.best_model_name}"
            )

            logging.info("========== Training Pipeline Completed ==========")

            return model_evaluation_artifact


        except Exception as e:
            raise CustomerException(e,sys)                  


