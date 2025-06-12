import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Admin/Downloads/sixth-syntax-462507-r5-b3e367858b75.json"
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)
class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data Ingestion initialized with bucket: {self.bucket_name} and file: {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            logger.info("Connecting to GCP Storage...")
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)

            # Print available files in the bucket
            logger.info("Available files in the bucket:")
            found = False
            for blob in bucket.list_blobs():
                logger.info(f"→ {blob.name}")
                if blob.name == self.file_name:
                    found = True

            if not found:
                raise CustomException(f"❌ File '{self.file_name}' not found in bucket '{self.bucket_name}'", None)

            # Download file
            blob = bucket.blob(self.file_name)
            os.makedirs(os.path.dirname(RAW_FILE_PATH), exist_ok=True)
            logger.info(f"📥 Downloading '{self.file_name}' to local path '{RAW_FILE_PATH}'")
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"✅ File successfully downloaded to: {RAW_FILE_PATH}")

        except Exception as e:
            logger.error("❌ Error while downloading the CSV file from GCP")
            raise CustomException("Failed to download CSV file", e)

    def split_data(self):
        try:
            logger.info("Starting data splitting process...")
            data = pd.read_csv(RAW_FILE_PATH)
            logger.info(f"Loaded data shape: {data.shape}")

            train_data, test_data = train_test_split(
                data,
                test_size=1 - self.train_test_ratio,
                random_state=42
            )

            os.makedirs(os.path.dirname(TRAIN_FILE_PATH), exist_ok=True)
            os.makedirs(os.path.dirname(TEST_FILE_PATH), exist_ok=True)

            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"✅ Train data saved to: {TRAIN_FILE_PATH}")
            logger.info(f"✅ Test data saved to: {TEST_FILE_PATH}")
        except Exception as e:
            logger.error("❌ Error while splitting the data")
            raise CustomException("Failed to split data into training and test sets", e)

    def run(self):
        try:
            logger.info("🚀 Starting the data ingestion process")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("✅ Data ingestion process completed successfully")
        except CustomException as ce:
            logger.error(f"❌ CustomException: {str(ce)}")
        finally:
            logger.info("🏁 Data ingestion process finished")

if __name__ == "__main__":
    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()