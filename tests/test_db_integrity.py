import string
from random import randint, choice, getrandbits

from django.db import IntegrityError
from bulbControlFrontend.models import wizbulb
from django.test import TestCase
from django.core.exceptions import ValidationError
from random import randint

class DB_Integrity_Tests(TestCase):
        
    @classmethod
    def setUpTestData(cls):
        pass

    def test_set_null_object(self):
        """Test null bulb cannot be created"""
        with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed: bulbControlFrontend_wizbulb\.bulbIp"):
            wizbulb.objects.create()
    
    def test_set_null_ip(self):
        with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed: bulbControlFrontend_wizbulb\.bulbIp"):
            wizbulb.objects.create(bulbName="Test Bulb")

    def test_set_null_name(self):
        with self.assertRaisesRegex(IntegrityError, "NOT NULL constraint failed: bulbControlFrontend_wizbulb\.bulbName"):
            wizbulb.objects.create(bulbIp=".".join(str(randint(1,254)) for _ in range(4)))
