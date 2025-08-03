import logging
import sys

console_logger = logging.getLogger(__name__)

console_logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_format = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
console_handler.setFormatter(console_format)
console_logger.addHandler(console_handler)
console_logger.propagate = False
