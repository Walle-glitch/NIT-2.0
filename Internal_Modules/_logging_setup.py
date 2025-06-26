# Internal_Modules/_logging_setup.py
"""
Logging setup for Discord bot modules. Creates daily log files and console output.
"""
import logging
import os
from datetime import datetime

# Determine base logs directory relative to project root
MODULE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(MODULE_DIR, '..'))
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')

# Ensure logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)


def setup_logging() -> logging.Logger:
    """
    Configure root logger to log to a daily file and console.
    Returns the configured logger instance.
    """
    # Log filename for today's date
    log_filename = os.path.join(LOGS_DIR, f"log-{datetime.now():%Y-%m-%d}.txt")

    # Create root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid adding handlers multiple times
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger