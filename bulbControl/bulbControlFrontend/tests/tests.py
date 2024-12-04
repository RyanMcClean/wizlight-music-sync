from django.test import TestCase
from ..models import wizbulb


class wizbulbTestCase(TestCase):
    def setUpTestData(self):
        testIp = "192.168.50.252"
        testName = "test name"
        testState = False
        testRed = 0
        testGreen = 0
        testBlue = 0
        testTemp = 0
        wizbulb.objects.create(
            bulbIp=testIp,
            bulbName=testName,
            bulbState=testState,
            bulbRed=testRed,
            bulbGreen=testGreen,
            bulbBlue=testBlue,
            bulbTemp=testTemp,
        )

    def test_bulb_creation(self):
        bulbString = wizbulb.objects.get(name="test name")
        self.assertEqual()
