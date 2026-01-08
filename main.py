
from src.logging.logging import logging
from src.exception.exception import CustomerException
from src.pipeline.training_pipeline import TrainingPipeline



import sys

if __name__=='__main__':
    try:
        training_pipeline = TrainingPipeline()
        model_evaluation_artifact = training_pipeline.run_pipeline()
        print(model_evaluation_artifact)
        
    except Exception as e:
        logging.error("Error in main.py")
        raise CustomerException(e,sys)    
        