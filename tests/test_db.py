import string
from random import randint, choice

from django.db import IntegrityError, transaction
from bulbControlFrontend.models import wizbulb
from django.test import TestCase
from django.core.exceptions import ValidationError


class DB_Tests(TestCase):
        
    @classmethod
    def setUpTestData(cls):
        cls.bulbArray = []
        cls.ipArray = []
        for x in range(randint(100, 1000)):
            name = "".join(choice(string.ascii_letters) for i in range(randint(3, 15)))
            if name not in cls.bulbArray:
                cls.bulbArray.append(name)
        for x in range(len(cls.bulbArray)):
            cls.ipArray.append(".".join(str(randint(1,254)) for _ in range(4)))

    def test_bulb_creation(self):
        """Test if the bulb name and ip are set correctly"""
        for x, y in zip(self.bulbArray, self.ipArray):
            bulb = wizbulb()
            bulb.bulbName = x
            bulb.bulbIp = y
            bulb.save()
        print(f"Testing {len(self.bulbArray)} bulbs", self)
        for x, y in zip(self.bulbArray, self.ipArray):
            bulb = wizbulb.objects.get(bulbName=x)
            self.assertEqual(bulb.bulbName, x)
            self.assertEqual(bulb.bulbIp, y)

    def test_invalid_bulb_creation(self):
        """Set invalid bulb name and ip and ensure it raises an appropriate error"""
        for x in self.bulbArray:
            bulb = wizbulb()
            bulb.bulbName = x
            with self.assertRaisesRegex(ValidationError, "bulbIp.*This field cannot be null.*"):
                bulb.full_clean()
                bulb.save()
        for y in self.ipArray:
            bulb = wizbulb()
            bulb.bulbIp = y
            with self.assertRaisesRegex(ValidationError, "bulbName.*This field cannot be null.*"):
                bulb.full_clean()
                bulb.save()

    def test_set_null_object(self):
        with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed:.*bulb.*"):
            wizbulb.objects.create()

    def test_set_null_bulb_ip(self):
        with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed:.*.bulbIp"):
            wizbulb.objects.create(bulbName="test")

    def test_set_null_bulb_name(self):
        with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed:.*.bulbName"):
            wizbulb.objects.create(bulbIp="192.168.50.1")
