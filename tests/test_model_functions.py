from django.test import TestCase
from bulbControlFrontend.models import wizbulb

class ModelFunctionTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.bulb = wizbulb()
        cls.bulb.bulbIp = "192.168.0.0"
        cls.bulb.bulbName = "Test Bulb"
        cls.bulb.bulbState = True
        cls.bulb.bulbRed = 255
        cls.bulb.bulbGreen = 255
        cls.bulb.bulbBlue = 255
        cls.bulb.bulbTemp = 5000

    def test_str_method(self):
        """Test the __str__ method of wizbulb"""
        
        self.assertRegex(str(self.bulb), f"^Bulb Ip: {self.bulb.bulbIp}\\nBulb Name: " +
                        f"{self.bulb.bulbName}\\nBulb State: {self.bulb.bulbState}\\nBulb Red: " +
                        f"{self.bulb.bulbRed}\\nBulb Green {self.bulb.bulbGreen}\\nBulb Blue: " +
                        f"{self.bulb.bulbBlue}\\nBulb Temp: {self.bulb.bulbTemp}\\n$")

    def test_json_method(self):
        """Test the returnJSON method of wizbulb"""
        
        expected_json = {
            "bulbIp": self.bulb.bulbIp,
            "bulbName": self.bulb.bulbName,
            "bulbState": self.bulb.bulbState,
            "bulbRed": self.bulb.bulbRed,
            "bulbGreen": self.bulb.bulbGreen,
            "bulbBlue": self.bulb.bulbBlue,
            "bulbTemp": self.bulb.bulbTemp,
        }
        self.assertDictEqual(self.bulb.returnJSON(), expected_json)
