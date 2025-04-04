import string
from random import randint, choice

from django.db import IntegrityError
from bulbControlFrontend.models import wizbulb
from django.test import TestCase
from django.core.exceptions import ValidationError


class DB_Tests(TestCase):
        
    bulbArray = []
    ipArray = []
    for x in range(randint(100, 1000)):
        name = "".join(choice(string.ascii_letters) for i in range(randint(3, 15)))
        if name not in bulbArray:
            bulbArray.append(name)
    for x in range(len(bulbArray)):
        ipArray.append(".".join(str(randint(1,254)) for _ in range(4)))

    @classmethod
    def setUpTestData(cls):
        for x, y in zip(cls.bulbArray, cls.ipArray):
            wizbulb.objects.create(bulbName=x, bulbIp=y)

    def test_set_bulb_name(self):
        """Test if the bulb name is set correctly"""
        print(f"Testing {len(self.bulbArray)} bulbs")
        for x in self.bulbArray:
            bulb = wizbulb.objects.get(bulbName=x)
            self.assertEqual(bulb.bulbName, x)

    def test_set_bulb_ip(self):
        for x, y in zip(self.bulbArray, self.ipArray):
            bulb = wizbulb.objects.get(bulbName=x)
            self.assertEqual(bulb.bulbIp, y)

    def test_set_null_object(self):
        with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed:.*bulb.*"):
            wizbulb.objects.create()

    def test_set_null_bulb_ip(self):
        with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed:.*.bulbIp"):
            wizbulb.objects.create(bulbName="test")

    def test_set_null_bulb_name(self):
        with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed:.*.bulbName"):
            wizbulb.objects.create(bulbIp="192.168.50.1")

    def test_set_null_bulb_name(self):
        bulb = wizbulb()
        bulb.bulbName = ""
        bulb.bulbIp = "192.168.50.6"
        with self.assertRaisesRegex(ValidationError, ".*bulbName.*This field cannot be blank.*"):
            bulb.full_clean()
            bulb.save()

