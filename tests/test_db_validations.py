import string
from random import randint, choice, getrandbits

from django.db import IntegrityError
from bulbControlFrontend.models import wizbulb
from django.test import TestCase
from django.core.exceptions import ValidationError


class DB_Validation_Tests(TestCase):

    def test_invalid_bulb_creation(self):
        """Set invalid bulb name and ip and ensure it raises an appropriate error"""
        bulbArray = []
        ipArray = []
        for x in range(randint(100, 1000)):
            name = "".join(choice(string.ascii_letters) for i in range(randint(3, 15)))
            if name not in bulbArray:
                bulbArray.append(name)
        for x in range(len(bulbArray)):
            ipArray.append(".".join(str(randint(1,254)) for _ in range(4)))
        for x in bulbArray:
            bulb = wizbulb()
            bulb.bulbName = x
            with self.assertRaisesRegex(ValidationError, "bulbIp.*This field cannot be null.*"):
                bulb.full_clean()
                bulb.save()
        for y in ipArray:
            bulb = wizbulb()
            bulb.bulbIp = y
            with self.assertRaisesRegex(ValidationError, "bulbName.*This field cannot be null.*"):
                bulb.full_clean()
                bulb.save()

    def test_set_null_bulb_ip(self):
        with self.assertRaisesRegex(ValidationError, ".*bulbIp.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbName = "test"
            bulb.full_clean()
            bulb.save()
        with self.assertRaisesRegex(ValidationError, ".*bulbIp.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbName = "test"
            bulb.bulbState = bool(getrandbits(1))
            bulb.full_clean()
            bulb.save()
        with self.assertRaisesRegex(ValidationError, ".*bulbIp.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbName = "test"
            bulb.bulbRed = randint(0,255)
            bulb.full_clean()
            bulb.save()
        with self.assertRaisesRegex(ValidationError, ".*bulbIp.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbName = "test"
            bulb.bulbBlue=randint(0,255)
            bulb.full_clean()
            bulb.save()
        with self.assertRaisesRegex(ValidationError, ".*bulbIp.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbName = "test"
            bulb.bulbGreen=randint(0,255)
            bulb.full_clean()
            bulb.save()
        with self.assertRaisesRegex(ValidationError, ".*bulbIp.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbName = "test"
            bulb.bulbTemp=randint(0,100)
            bulb.full_clean()
            bulb.save()
            
    def test_set_null_bulb_name(self):
        with self.assertRaisesRegex(ValidationError, ".*bulbName.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbIp = "192.168.50.1"
            bulb.full_clean()
            bulb.save()
        with self.assertRaisesRegex(ValidationError, ".*bulbName.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbIp = "192.168.50.1"
            bulb.bulbState = bool(getrandbits(1))
            bulb.full_clean()
            bulb.save()
        with self.assertRaisesRegex(ValidationError, ".*bulbName.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbIp = "192.168.50.1"
            bulb.bulbRed = randint(0, 255)
            bulb.full_clean()
            bulb.save()
        with self.assertRaisesRegex(ValidationError, ".*bulbName.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbIp = "192.168.50.1"
            bulb.bulbBlue = randint(0, 255)
            bulb.full_clean()
            bulb.save()
        with self.assertRaisesRegex(ValidationError, ".*bulbName.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbIp = "192.168.50.1"
            bulb.bulbGreen = randint(0, 255)
            bulb.full_clean()
            bulb.save()
        with self.assertRaisesRegex(ValidationError, ".*bulbName.*This field cannot be null.*"):
            bulb = wizbulb()
            bulb.bulbIp = "192.168.50.1"
            bulb.bulbTemp = randint(0, 100)
            bulb.full_clean()
            bulb.save()
            
    def test_set_int_value_invalid(self):
        bulb_array = []
        bulb_array.append(wizbulb(bulbName="Invalid Blue",  bulbIp="192.168.50.1", bulbBlue=randint(256, 1000)))
        bulb_array.append(wizbulb(bulbName="Invalid Red",   bulbIp="192.168.50.1", bulbRed=randint(256, 1000)))
        bulb_array.append(wizbulb(bulbName="Invalid Green", bulbIp="192.168.50.1", bulbGreen=randint(256, 1000)))
        bulb_array.append(wizbulb(bulbName="Invalid Temp",  bulbIp="192.168.50.1", bulbTemp=randint(101, 1000)))
        
        for bulb in bulb_array:
            with self.assertRaisesRegex(ValidationError, ".*bulb(Red|Blue|Green|Temp).*Ensure this value is less than or equal to (100|255).*"):
                bulb.full_clean()
                bulb.save()
            print(bulb.bulbName + ":\tPassed!", self)

    def test_set_invalid_ip(self):
        invalid_ip_bulb_array = []
        for x in range(randint(100, 1000)):
            bulb = wizbulb()
            bulb.bulbName = "Test Bulb"
            bulb.bulbIp = ".".join(str(randint(255,999)) for _ in range(4))
            invalid_ip_bulb_array.append(bulb)
        for bulb in invalid_ip_bulb_array:
            with self.assertRaisesRegex(ValidationError, ".*bulbIp.*Enter a valid IPv4 address.*"):
                bulb.full_clean()
                bulb.save()
        print(str(len(invalid_ip_bulb_array)) + " Tests Passed!", self)
