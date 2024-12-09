from bulbControlFrontend.models import wizbulb
from django.test import TestCase


class DB_Tests(TestCase):
    bulbOneName = "Test One"
    bulbTwoName = "Test Two"

    @classmethod
    def setUpTestData(cls):
        wizbulb.objects.create(bulbName=cls.bulbOneName)
        wizbulb.objects.create(bulbName=cls.bulbTwoName)

    def test_db(self):
        bulbOne = wizbulb.objects.get(bulbName=self.bulbOneName)
        bulbTwo = wizbulb.objects.get(bulbName=self.bulbTwoName)
        self.assertEqual(bulbOne.bulbName, self.bulbOneName)
        self.assertEqual(bulbTwo.bulbName, self.bulbTwoName)
