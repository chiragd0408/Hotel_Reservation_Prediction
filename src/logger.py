import logging
import os
from datetime import datetime

LOGS_DIR = "logs",
os.makedirs(LOGS_DIR,exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

<<<<<<< HEAD
logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
=======
>>>>>>> 49e111ed0499132eab4ddebffc207b2254fa6b7a
