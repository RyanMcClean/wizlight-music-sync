# pylint: disable = broad-exception-caught
"""Unit tests for WizBulb models, tests that their user created functions work as expected."""

import logging
import inspect
from django.test import TestCase
from test_helper import setup_logger
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
        cls.bulb.bulb_brightness = 100

    def test_str_method(self):
        """Test the __str__ method of Wizbulb"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        self.assertRegex(
            str(self.bulb),
            f"^Bulb Ip: {self.bulb.bulb_ip}\\nBulb Name: "
            + f"{self.bulb.bulb_name}\\nBulb State: {self.bulb.bulb_state}\\nBulb Red: "
            + f"{self.bulb.bulb_red}\\nBulb Green {self.bulb.bulb_green}\\nBulb Blue: "
            + f"{self.bulb.bulb_blue}\\nBulb Temp: {self.bulb.bulb_temp}\\nBulb Brightness: "
            + f"{self.bulb.bulb_brightness}",
        )
        LOGGER.debug("String representation of Wizbulb is correct")

    def test_json_method(self):
        """Test the returnJSON method of Wizbulb"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        expected_json = {
            "bulb_ip": self.bulb.bulb_ip,
            "bulb_name": self.bulb.bulb_name,
            "bulb_state": self.bulb.bulb_state,
            "bulb_red": self.bulb.bulb_red,
            "bulb_green": self.bulb.bulb_green,
            "bulb_blue": self.bulb.bulb_blue,
            "bulb_temp": self.bulb.bulb_temp,
            "bulb_brightness": self.bulb.bulb_brightness,
        }
        self.assertDictEqual(self.bulb.return_json(), expected_json)
        LOGGER.debug("JSON representation of Wizbulb is correct")
