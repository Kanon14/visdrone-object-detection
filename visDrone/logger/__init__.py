import logging 
import os
from datetime import datetime
from from_root import from_root


# Generate a unique log file name based on the current date and time
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define the directory path for storing log files
log_path = os.path.join(from_root(), 'log', LOG_FILE)

# Ensure the log directory exists
os.makedirs(log_path, exist_ok=True)

# Define the full path for the log file
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

# Configure the logging settings
logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)