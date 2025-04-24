from django.test import TestCase
from bulbControlFrontend.models import wizbulb
import logging, os
from test_helper import formatter

LOGGER = logging.getLogger(__name__)


class ModelFunctionTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.bulb = wizbulb()
        cls.bulb.bulbIp = "192.168.0.0"
        cls.bulb.bulbName = "Test Bulb"
        cls.bulb.bulbState = True
        cls.bulb.bulbRed = 255
        cls.bulb.bulbGreen = 255
        cls.bulb.bulbBlue = 255
        cls.bulb.bulbTemp = 5000

    def test_str_method(self):
        """Test the __str__ method of wizbulb"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_invalid_bulb_creation.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            self.assertRegex(
                str(self.bulb),
                f"^Bulb Ip: {self.bulb.bulbIp}\\nBulb Name: "
                + f"{self.bulb.bulbName}\\nBulb State: {self.bulb.bulbState}\\nBulb Red: "
                + f"{self.bulb.bulbRed}\\nBulb Green {self.bulb.bulbGreen}\\nBulb Blue: "
                + f"{self.bulb.bulbBlue}\\nBulb Temp: {self.bulb.bulbTemp}\\n$",
            )
            LOGGER.debug("String representation of wizbulb is correct")
        except Exception as e:
            LOGGER.error("An error occurred in test_str_method: %s", e)

    def test_json_method(self):
        """Test the returnJSON method of wizbulb"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_invalid_bulb_creation.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            expected_json = {
                "bulbIp": self.bulb.bulbIp,
                "bulbName": self.bulb.bulbName,
                "bulbState": self.bulb.bulbState,
                "bulbRed": self.bulb.bulbRed,
                "bulbGreen": self.bulb.bulbGreen,
                "bulbBlue": self.bulb.bulbBlue,
                "bulbTemp": self.bulb.bulbTemp,
            }
            self.assertDictEqual(self.bulb.returnJSON(), expected_json)
            LOGGER.debug("JSON representation of wizbulb is correct")
        except Exception as e:
            LOGGER.error("An error occurred in test_json_method: %s", e)
