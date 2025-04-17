import string
from random import randint, choice, getrandbits
import logging, os
from bulbControlFrontend.models import wizbulb
from django.test import TestCase
from django.core.exceptions import ValidationError
from test_helper import formatter

LOGGER = logging.getLogger(__name__)

class DB_Validation_Tests(TestCase):

    def test_invalid_bulb_creation(self):
        """Set invalid bulb name and ip and ensure it raises an appropriate error"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_invalid_bulb_creation.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            bulbArray = []
            ipArray = []
            # Step 1, Fill bulb array with random names
            for x in range(randint(100, 1000)):
                name = "".join(choice(string.ascii_letters) for i in range(randint(3, 15)))
                if name not in bulbArray:
                    bulbArray.append(name)
            LOGGER.debug("Bulb names array of length: %s", len(bulbArray))
            # Step 2, Fill ip array with random ips
            for x in range(len(bulbArray)):
                ipArray.append(".".join(str(randint(1,254)) for _ in range(4)))
            # Step 3, Create bulbs with only names and ensure it raises an error
            for x in bulbArray:
                bulb = wizbulb()
                bulb.bulbName = x
                with self.assertRaisesRegex(ValidationError, "{'bulbIp': \['This field cannot be null\.'\]}"):
                    bulb.full_clean()
                    bulb.save()
            LOGGER.debug("Bulb creation for bulb array failed as expected")
            # Step 4, Create bulbs with only ips and ensure it raises an error
            for y in ipArray:
                bulb = wizbulb()
                bulb.bulbIp = y
                with self.assertRaisesRegex(ValidationError, "{'bulbName': \['This field cannot be null\.'\]}"):
                    bulb.full_clean()
                    bulb.save()
            LOGGER.debug("Bulb creation for ip array failed as expected")
        except Exception as e:
            LOGGER.error("An error occurred in test_invalid_bulb_creation: %s", e)

    def test_set_null_bulb_ip(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_null_bulb_ip.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            # Step 1, attempt to create bulb with only a name
            with self.assertRaisesRegex(ValidationError, "{'bulbIp': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbName = "test"
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only a name failed as expected")
            # Step 2, attempt to create bulb with only a name and a state
            with self.assertRaisesRegex(ValidationError, "{'bulbIp': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbName = "test"
                bulb.bulbState = bool(getrandbits(1))
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only a name and state failed as expected")
            # Step 3, attempt to create bulb with only a name and a red value
            with self.assertRaisesRegex(ValidationError, "{'bulbIp': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbName = "test"
                bulb.bulbRed = randint(0,255)
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only a name and red value failed as expected")
            # Step 4, attempt to create bulb with only a name and a blue value
            with self.assertRaisesRegex(ValidationError, "{'bulbIp': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbName = "test"
                bulb.bulbBlue=randint(0,255)
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only a name and blue value failed as expected")
            # Step 5, attempt to create bulb with only a name and a green value
            with self.assertRaisesRegex(ValidationError, "{'bulbIp': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbName = "test"
                bulb.bulbGreen=randint(0,255)
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only a name and green value failed as expected")
            # Step 6, attempt to create bulb with only a name and a temp value
            with self.assertRaisesRegex(ValidationError, "{'bulbIp': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbName = "test"
                bulb.bulbTemp=randint(2000, 6500)
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only a name and temp value failed as expected")
        except Exception as e:
            LOGGER.error("An error occurred in test_set_null_bulb_ip: %s", e)
            
    def test_set_null_bulb_name(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_null_bulb_name.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            # Step 1, attempt to create bulb with only an ip
            with self.assertRaisesRegex(ValidationError, "{'bulbName': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbIp = "192.168.50.1"
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only an ip failed as expected")
            # Step 2, attempt to create bulb with only an ip and a state
            with self.assertRaisesRegex(ValidationError, "{'bulbName': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbIp = "192.168.50.1"
                bulb.bulbState = bool(getrandbits(1))
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only an ip and state failed as expected")
            # Step 3, attempt to create bulb with only an ip and a red value
            with self.assertRaisesRegex(ValidationError, "{'bulbName': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbIp = "192.168.50.1"
                bulb.bulbRed = randint(0, 255)
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only an ip and red value failed as expected")
            # Step 4, attempt to create bulb with only an ip and a blue value
            with self.assertRaisesRegex(ValidationError, "{'bulbName': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbIp = "192.168.50.1"
                bulb.bulbBlue = randint(0, 255)
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only an ip and blue value failed as expected")
            # Step 5, attempt to create bulb with only an ip and a green value
            with self.assertRaisesRegex(ValidationError, "{'bulbName': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbIp = "192.168.50.1"
                bulb.bulbGreen = randint(0, 255)
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only an ip and green value failed as expected")
            # Step 6, attempt to create bulb with only an ip and a temp value
            with self.assertRaisesRegex(ValidationError, "{'bulbName': \['This field cannot be null\.'\]}"):
                bulb = wizbulb()
                bulb.bulbIp = "192.168.50.1"
                bulb.bulbTemp = randint(2000, 6500)
                bulb.full_clean()
                bulb.save()
            LOGGER.debug("Bulb creation with only an ip and temp value failed as expected")
        except Exception as e:
            LOGGER.error("An error occurred in test_set_null_bulb_name: %s", e)
            
    def test_set_int_value_invalid(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_int_value_invalid.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            bulb_array = []
            # Step 1, Create array of bulbs that have invalid int attribute values
            bulb_array.append(wizbulb(bulbName="Invalid Blue",  bulbIp="192.168.50.1", bulbBlue=randint(256, 1000)))
            bulb_array.append(wizbulb(bulbName="Invalid Red",   bulbIp="192.168.50.1", bulbRed=randint(256, 1000)))
            bulb_array.append(wizbulb(bulbName="Invalid Green", bulbIp="192.168.50.1", bulbGreen=randint(256, 1000)))
            bulb_array.append(wizbulb(bulbName="Invalid Temp",  bulbIp="192.168.50.1", bulbTemp=randint(0, 199)))
            # Step 2, attempt to create bulbs with invalid int values and ensure it raises an error
            for bulb in bulb_array:
                with self.assertRaisesRegex(ValidationError, "{'bulb(Red|Blue|Green|Temp)': \['Ensure this value is (less|greater) than or equal to (2000|255)\.'\]}"):
                    bulb.full_clean()
                    bulb.save()
                print(bulb.bulbName + ":\tPassed!", self)
            LOGGER.debug("Bulb creations with invalid int values failed as expected")
        except Exception as e:
            LOGGER.error("An error occurred in test_set_int_value_invalid: %s", e)

    def test_set_invalid_ip(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_invalid_ip.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            invalid_ip_bulb_array = []
            for x in range(randint(100, 1000)):
                bulb = wizbulb()
                bulb.bulbName = "Test Bulb"
                bulb.bulbIp = ".".join(str(randint(255,999)) for _ in range(4))
                invalid_ip_bulb_array.append(bulb)
            LOGGER.debug("Invalid IP bulb array of length: %s", len(invalid_ip_bulb_array))
            for bulb in invalid_ip_bulb_array:
                with self.assertRaisesRegex(ValidationError, "{'bulbIp': \['Enter a valid IPv4 address\.'\]}"):
                    bulb.full_clean()
                    bulb.save()
            print(str(len(invalid_ip_bulb_array)) + " Tests Passed!", self)
            LOGGER.debug("Bulb creations with invalid IPs failed as expected")
        except Exception as e:
            LOGGER.error("An error occurred in test_set_invalid_ip: %s", e)
