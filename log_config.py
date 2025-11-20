import logging
import sys
import os
LOG_FILE_NAME = 'logs.log'

console_logger = logging.getLogger("console")
console_logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
console_logger.addHandler(console_handler)
console_logger.propagate = False


file_logger = logging.getLogger("file")
file_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE_NAME, mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
file_logger.addHandler(file_handler)
file_logger.propagate = False


def clean_log_file():
    if os.path.exists(LOG_FILE_NAME):
        with open(LOG_FILE_NAME, "w", encoding="utf-8") as log_file:
            pass
        console_logger.info(f'Log file {LOG_FILE_NAME} cleaned.')
    else:
        console.logger.info('Log file does not exist yet.')
