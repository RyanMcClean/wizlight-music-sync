"""Helper functions for testing"""

import logging
import os

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)-8s - %(message)-30s - ( %(filename)s : %(lineno)s )"
)


def setup_logger(class_name, name, logger):
    """Used to setup the logger in tests, helpful to reduce duplicated code"""
    # Set up logging for the test
    log_filename = f"test_logs/individual_test_logs/{class_name}/{name}.log"
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)
    log_handler = logging.FileHandler(log_filename, "w")
    log_handler.setFormatter(formatter)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    logger.addHandler(log_handler)
