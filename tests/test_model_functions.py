# pylint: disable = broad-exception-caught
"""Unit tests for WizBulb models, tests that their user created functions work as expected."""

import logging
import os
from django.test import TestCase
from test_helper import formatter
from bulb_control_frontend.models import Wizbulb


LOGGER = logging.getLogger(__name__)


class ModelFunctionTests(TestCase):
    """Test the Wizbulb model functions."""

    @classmethod
    def setUpTestData(cls):
        cls.bulb = Wizbulb()
        cls.bulb.bulb_ip = "192.168.0.0"
        cls.bulb.bulb_name = "Test Bulb"
        cls.bulb.bulb_state = True
        cls.bulb.bulb_red = 255
        cls.bulb.bulb_green = 255
        cls.bulb.bulb_blue = 255
        cls.bulb.bulb_temp = 5000

    def test_str_method(self):
        """Test the __str__ method of Wizbulb"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_invalid_bulb_creation.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)

        self.assertRegex(
            str(self.bulb),
            f"^Bulb Ip: {self.bulb.bulb_ip}\\nBulb Name: "
            + f"{self.bulb.bulb_name}\\nBulb State: {self.bulb.bulb_state}\\nBulb Red: "
            + f"{self.bulb.bulb_red}\\nBulb Green {self.bulb.bulb_green}\\nBulb Blue: "
            + f"{self.bulb.bulb_blue}\\nBulb Temp: {self.bulb.bulb_temp}\\n$",
        )
        LOGGER.debug("String representation of Wizbulb is correct")

    def test_json_method(self):
        """Test the returnJSON method of Wizbulb"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_invalid_bulb_creation.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)

        expected_json = {
            "bulb_ip": self.bulb.bulb_ip,
            "bulb_name": self.bulb.bulb_name,
            "bulb_state": self.bulb.bulb_state,
            "bulb_red": self.bulb.bulb_red,
            "bulb_green": self.bulb.bulb_green,
            "bulb_blue": self.bulb.bulb_blue,
            "bulb_temp": self.bulb.bulb_temp,
        }
        self.assertDictEqual(self.bulb.return_json(), expected_json)
        LOGGER.debug("JSON representation of Wizbulb is correct")
