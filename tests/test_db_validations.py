# pylint: disable = broad-exception-caught, anomalous-backslash-in-string
"""Unit tests for the Wizbulb model to ensure that invalid data is not accepted by the database."""

import string
from random import randint, choice, getrandbits
import logging
import os
from django.test import TestCase
from django.core.exceptions import ValidationError
from test_helper import formatter
from bulb_control_frontend.models import Wizbulb

LOGGER = logging.getLogger(__name__)


class DBValidationTests(TestCase):
    """Test class for Wizbulb model validation"""

    def test_invalid_bulb_creation(self):
        """Set invalid bulb name and ip and ensure it raises an appropriate error"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_invalid_bulb_creation.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)

        bulb_array = []
        ip_array = []
        # Step 1, Fill bulb array with random names
        for x in range(randint(100, 1000)):
            name = "".join(choice(string.ascii_letters) for i in range(randint(3, 15)))
            if name not in bulb_array:
                bulb_array.append(name)
        LOGGER.debug("Bulb names array of length: %s", len(bulb_array))
        # Step 2, Fill ip array with random ips
        for x in range(len(bulb_array)):
            ip_array.append(".".join(str(randint(1, 254)) for _ in range(4)))
        # Step 3, Create bulbs with only names and ensure it raises an error
        for x in bulb_array:
            bulb = Wizbulb()
            bulb.bulb_name = x
            with self.assertRaisesRegex(
                ValidationError, "{'bulb_ip': \['This field cannot be null\.'\]}"
            ):
                bulb.full_clean()
                bulb.save()
        LOGGER.debug("Bulb creation for bulb array failed as expected")
        # Step 4, Create bulbs with only ips and ensure it raises an error
        for y in ip_array:
            bulb = Wizbulb()
            bulb.bulb_ip = y
            with self.assertRaisesRegex(
                ValidationError, "{'bulb_name': \['This field cannot be null\.'\]}"
            ):
                bulb.full_clean()
                bulb.save()
        LOGGER.debug("Bulb creation for ip array failed as expected")

    def test_set_null_bulb_ip(self):
        """Set null bulb ip and ensure it raises an appropriate error"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_null_bulb_ip.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)

        # Step 1, attempt to create bulb with only a name
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_ip': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_name = "test"
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only a name failed as expected")
        # Step 2, attempt to create bulb with only a name and a state
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_ip': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_name = "test"
            bulb.bulb_state = bool(getrandbits(1))
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only a name and state failed as expected")
        # Step 3, attempt to create bulb with only a name and a red value
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_ip': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_name = "test"
            bulb.bulb_red = randint(0, 255)
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only a name and red value failed as expected")
        # Step 4, attempt to create bulb with only a name and a blue value
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_ip': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_name = "test"
            bulb.bulb_blue = randint(0, 255)
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only a name and blue value failed as expected")
        # Step 5, attempt to create bulb with only a name and a green value
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_ip': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_name = "test"
            bulb.bulb_green = randint(0, 255)
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only a name and green value failed as expected")
        # Step 6, attempt to create bulb with only a name and a temp value
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_ip': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_name = "test"
            bulb.bulb_temp = randint(2000, 6500)
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only a name and temp value failed as expected")

    def test_set_null_bulb_name(self):
        """Set null bulb name and ensure it raises the appropriate error"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_null_bulb_name.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)

        # Step 1, attempt to create bulb with only an ip
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_name': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_ip = "192.168.50.1"
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only an ip failed as expected")
        # Step 2, attempt to create bulb with only an ip and a state
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_name': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_ip = "192.168.50.1"
            bulb.bulb_state = bool(getrandbits(1))
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only an ip and state failed as expected")
        # Step 3, attempt to create bulb with only an ip and a red value
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_name': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_ip = "192.168.50.1"
            bulb.bulb_red = randint(0, 255)
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only an ip and red value failed as expected")
        # Step 4, attempt to create bulb with only an ip and a blue value
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_name': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_ip = "192.168.50.1"
            bulb.bulb_blue = randint(0, 255)
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only an ip and blue value failed as expected")
        # Step 5, attempt to create bulb with only an ip and a green value
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_name': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_ip = "192.168.50.1"
            bulb.bulb_green = randint(0, 255)
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only an ip and green value failed as expected")
        # Step 6, attempt to create bulb with only an ip and a temp value
        with self.assertRaisesRegex(
            ValidationError, "{'bulb_name': \['This field cannot be null\.'\]}"
        ):
            bulb = Wizbulb()
            bulb.bulb_ip = "192.168.50.1"
            bulb.bulb_temp = randint(2000, 6500)
            bulb.full_clean()
            bulb.save()
        LOGGER.debug("Bulb creation with only an ip and temp value failed as expected")

    def test_set_int_value_invalid(self):
        """Set invalid int values for bulb and ensure appropriate errors are raised"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_int_value_invalid.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)

        bulb_array = []
        # Step 1, Create array of bulbs that have invalid int attribute values
        bulb_array.append(
            Wizbulb(
                bulb_name="Invalid Blue",
                bulb_ip="192.168.50.1",
                bulb_blue=randint(256, 1000),
            )
        )
        bulb_array.append(
            Wizbulb(
                bulb_name="Invalid Red",
                bulb_ip="192.168.50.1",
                bulb_red=randint(256, 1000),
            )
        )
        bulb_array.append(
            Wizbulb(
                bulb_name="Invalid Green",
                bulb_ip="192.168.50.1",
                bulb_green=randint(256, 1000),
            )
        )
        bulb_array.append(
            Wizbulb(
                bulb_name="Invalid Temp",
                bulb_ip="192.168.50.1",
                bulb_temp=randint(0, 199),
            )
        )
        # Step 2, attempt to create bulbs with invalid int values and ensure it raises an error
        for bulb in bulb_array:
            with self.assertRaisesRegex(
                ValidationError,
                "{'bulb_(red|blue|green|temp)': \['Ensure this value is "
                + "(less|greater) than or equal to (2000|255)\.'\]}",
            ):
                bulb.full_clean()
                bulb.save()
            print(bulb.bulb_name + ":\tPassed!", self)
        LOGGER.debug("Bulb creations with invalid int values failed as expected")

    def test_set_invalid_ip(self):
        """Set invalid ip values for bulb and ensure appropriate errors are raised"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_invalid_ip.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)

        invalid_ip_bulb_array = []
        for _ in range(randint(100, 1000)):
            bulb = Wizbulb()
            bulb.bulb_name = "Test Bulb"
            bulb.bulb_ip = ".".join(str(randint(255, 999)) for _ in range(4))
            invalid_ip_bulb_array.append(bulb)
        LOGGER.debug("Invalid IP bulb array of length: %s", len(invalid_ip_bulb_array))
        for bulb in invalid_ip_bulb_array:
            with self.assertRaisesRegex(
                ValidationError, "{'bulb_ip': \['Enter a valid IPv4 address\.'\]}"
            ):
                bulb.full_clean()
                bulb.save()
        print(str(len(invalid_ip_bulb_array)) + " Tests Passed!", self)
        LOGGER.debug("Bulb creations with invalid IPs failed as expected")
