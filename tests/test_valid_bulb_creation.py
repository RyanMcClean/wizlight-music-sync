"""Unit tests to ensure that bulbs are created correctly in the database"""

import string
import logging
import inspect
from random import randint, choice, getrandbits
from django.test import TestCase
from test_helper import setup_logger
from bulb_control_frontend.models import Wizbulb

LOGGER = logging.getLogger(__name__)


class DBBulbCreationTests(TestCase):
    """Test class for bulb creation in database"""

    @classmethod
    def setUpTestData(cls):
        cls.nameArray = []
        cls.ipArray = []
        cls.redArray = []
        cls.blueArray = []
        cls.greenArray = []
        cls.tempArray = []
        cls.stateArray = []

        # Populate nameArray
        for _ in range(randint(100, 1000)):
            name = "".join(choice(string.ascii_letters) for i in range(randint(3, 15)))
            if name not in cls.nameArray:
                cls.nameArray.append(name)

        # Populate ipArray
        for _ in range(len(cls.nameArray)):
            cls.ipArray.append(".".join(str(randint(1, 254)) for _ in range(4)))

        # Populate redArray
        for _ in range(len(cls.nameArray)):
            cls.redArray.append(randint(0, 255))

        # Populate blueArray
        for _ in range(len(cls.nameArray)):
            cls.blueArray.append(randint(0, 255))

        # Populate greenArray
        for _ in range(len(cls.nameArray)):
            cls.greenArray.append(randint(0, 255))

        # Populate tempArray
        for _ in range(len(cls.nameArray)):
            cls.tempArray.append(randint(2000, 6500))

        # Populate stateArray
        for _ in range(len(cls.nameArray)):
            cls.stateArray.append(bool(getrandbits(1)))

        for name, ip, red, blue, green, temp, state in zip(
            cls.nameArray,
            cls.ipArray,
            cls.redArray,
            cls.blueArray,
            cls.greenArray,
            cls.tempArray,
            cls.stateArray,
        ):
            bulb = Wizbulb()
            bulb.bulb_name = name
            bulb.bulb_ip = ip
            bulb.bulb_red = red
            bulb.bulb_blue = blue
            bulb.bulb_green = green
            bulb.bulb_temp = temp
            bulb.bulb_state = state
            bulb.full_clean()
            bulb.save()

    def test_bulb_creation(self):
        """Test if the bulbs are created correctly"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        for name, ip, red, blue, green, temp, state in zip(
            self.nameArray,
            self.ipArray,
            self.redArray,
            self.blueArray,
            self.greenArray,
            self.tempArray,
            self.stateArray,
        ):
            bulb = Wizbulb.objects.get(bulb_name=name)
            self.assertEqual(bulb.bulb_name, name)
            self.assertEqual(bulb.bulb_ip, ip)
            self.assertEqual(bulb.bulb_red, red)
            self.assertEqual(bulb.bulb_blue, blue)
            self.assertEqual(bulb.bulb_green, green)
            self.assertEqual(bulb.bulb_temp, temp)
            self.assertEqual(bulb.bulb_state, state)

        LOGGER.debug("All bulbs created successfully")
