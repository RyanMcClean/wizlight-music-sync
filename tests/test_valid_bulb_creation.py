"""Unit tests to ensure that bulbs are created correctly in the database"""

import string
from random import randint, choice, getrandbits

from bulb_control_frontend.models import Wizbulb
from django.test import TestCase


class DB_Bulb_Creation_Tests(TestCase):

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
        for x in range(randint(100, 1000)):
            name = "".join(choice(string.ascii_letters) for i in range(randint(3, 15)))
            if name not in cls.nameArray:
                cls.nameArray.append(name)

        # Populate ipArray
        for x in range(len(cls.nameArray)):
            cls.ipArray.append(".".join(str(randint(1, 254)) for _ in range(4)))

        # Populate redArray
        for x in range(len(cls.nameArray)):
            cls.redArray.append(randint(0, 255))

        # Populate blueArray
        for x in range(len(cls.nameArray)):
            cls.blueArray.append(randint(0, 255))

        # Populate greenArray
        for x in range(len(cls.nameArray)):
            cls.greenArray.append(randint(0, 255))

        # Populate tempArray
        for x in range(len(cls.nameArray)):
            cls.tempArray.append(randint(0, 100))

        # Populate stateArray
        for x in range(len(cls.nameArray)):
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
            bulb.save()

    def test_bulb_creation(self):
        """Test if the bulbs are created correctly"""

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

        print(f"{len(self.nameArray)} bulbs: Passed!", self)
