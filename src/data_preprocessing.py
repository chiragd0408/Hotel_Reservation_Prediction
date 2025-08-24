import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import * 
from utils.common_functions import read_yaml,load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:

    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
    
    def preprocess_data(self,df):
        try:
            logger.info("Starting our Data Processing step")

            logger.info("Dropping the Columns")
            df.drop(columns=['Unnamed:0', 'Booking_ID'] , inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            logger.info("Applying Label Encoding")

            label_encoder = LabelEncoder()
            mappings = {}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label, code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}

            logger.info("Label Mapping are : ")
            for col,mappings in mappings.items():
                logger.info(f"{col} : {mappings}")

            logger.info("Doing Skewness Handling")

            skew_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x:x.skew())

            for column in skewness[skewness>skew_threshold].index:
                df[column] = np.log1p(df[column])
            return df
        
        except Exception as e:
            logger.error(f"Error during processing step {e}")
            raise CustomException("Error while preprocess data", e)
    
    def balance_data(self,df):
        try:
            logger.info("Handling Imbalanced Data")
            x = df.drop(columns = 'booking_status')
            y = df["booking_status"]

            smote = SMOTE(random_state=42)
            x_resampled,y_resampled = smote.fit_resample(x,y)

            balanced_df = pd.DataFrame(x_resampled , columns=x.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Data Balanced Successfully")
            return balanced_df
        
        except Exception as e:
            logger.error(f"Error during balancing data step {e}")
            raise CustomException("Error while balancing data", e)
        
    def :