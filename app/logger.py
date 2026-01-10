import logging
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL")
LOG_FOLDER = "logs"

# check log folder existence otherwise create logs folder
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)


logs_file = os.path.join(LOG_FOLDER, f"app_{datetime.now().strftime('%Y-%m-%d')}.log")

logger  = logging.getLogger("app_logger")
logger.setLevel(LOG_LEVEL)

# log formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# file handler
file_handler = logging.FileHandler(logs_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
