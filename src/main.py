import datetime

from src.config import *
from src.logger import initialize_logger

if __name__ == "__main__":
    
    # Create logger
    formatted_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    log_path = LOG_FOLDER.joinpath(formatted_time + ".log")
    logger = initialize_logger(log_path)
    logger.info(f"Logger initialized with name: {log_path}")
    