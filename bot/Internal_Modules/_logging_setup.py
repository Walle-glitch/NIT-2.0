import logging
import os
from datetime import datetime

def setup_logging():
    # Skapa loggmappen om den inte existerar
    if not os.path.exists('/home/bot/NIT-2.0/bot/logs'):
        os.makedirs('/home/bot/NIT-2.0/bot/logs')

    # Sätt upp filnamn baserat på dagens datum
    log_filename = f'logs/log-{datetime.now().strftime("%Y-%m-%d")}.txt'

    # Sätt upp loggern
    logging.basicConfig(
        level=logging.INFO,  # Sätt standard loggnivå till INFO
        format='%(asctime)s %(levelname)s: %(message)s',  # Syslog-format
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_filename),  # Logga till fil
            logging.StreamHandler()  # Logga till konsolen också (valfritt)
        ]
    )

    logger = logging.getLogger()
    return logger
