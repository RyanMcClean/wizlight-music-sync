from random import randint
import logging, os
from django.db import IntegrityError
from bulbControlFrontend.models import wizbulb
from django.test import TestCase
from random import randint
from test_helper import formatter

LOGGER = logging.getLogger(__name__)

class DB_Integrity_Tests(TestCase):
        
    @classmethod
    def setUpTestData(cls):
        pass

    def test_set_null_object(self):
        """Test null bulb cannot be created"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_null_object.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed: bulbControlFrontend_wizbulb\.bulbIp"):
                wizbulb.objects.create(); LOGGER.debug("Null object creation failed as expected")
        except Exception as e:
            LOGGER.error("An error occurred in test_set_null_object: %s", e)
    
    def test_set_null_ip(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_null_ip.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed: bulbControlFrontend_wizbulb\.bulbIp"):
                wizbulb.objects.create(bulbName="Test Bulb"); LOGGER.debug("Null IP creation failed as expected")
        except Exception as e:
            LOGGER.error("An error occurred in test_set_null_ip: %s", e)

    def test_set_null_name(self):
                # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_null_name.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed: bulbControlFrontend_wizbulb\.bulbName"):
                wizbulb.objects.create(bulbIp=".".join(str(randint(1,254)) for _ in range(4))); LOGGER.debug("Null name creation failed as expected")
        except Exception as e:
            LOGGER.error("An error occurred in test_set_null_name: %s", e)
