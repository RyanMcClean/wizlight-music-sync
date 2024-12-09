import random, string
from bulbControlFrontend.models import wizbulb
from django.test import TestCase


class DB_Tests(TestCase):
    bulbArray = []
    for x in range(random.randint(10, 1000)):
        bulbArray.append("".join(random.choice(string.ascii_letters) for i in range(random.randint(3, 15))))

    @classmethod
    def setUpTestData(cls):
        for x in cls.bulbArray:
            wizbulb.objects.create(bulbName=x)

    def test_db(self):
        for x in self.bulbArray:
            bulb = wizbulb.objects.get(bulbName=x)
            self.assertEqual(bulb.bulbName, x)
