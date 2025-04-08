import string
from random import randint, choice, getrandbits

from bulbControlFrontend.models import wizbulb
from django.test import TestCase

class DB_Bulb_Creation_Tests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.nameArray = []; cls.ipArray = []; cls.redArray = []; cls.blueArray = []
        cls.greenArray = []; cls.tempArray = []; cls.stateArray = []
        
        # Populate nameArray
        for x in range(randint(100, 1000)):
            name = "".join(choice(string.ascii_letters) for i in range(randint(3, 15)))
            if name not in cls.nameArray:
                cls.nameArray.append(name)
                
        # Populate ipArray
        for x in range(len(cls.nameArray)):
            cls.ipArray.append(".".join(str(randint(1,254)) for _ in range(4)))
            
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
            
        for name, ip, red, blue, green, temp, state in zip(cls.nameArray, cls.ipArray, cls.redArray, cls.blueArray, cls.greenArray, cls.tempArray, cls.stateArray):
            bulb = wizbulb()
            bulb.bulbName = name
            bulb.bulbIp = ip
            bulb.bulbRed = red
            bulb.bulbBlue = blue
            bulb.bulbGreen = green
            bulb.bulbTemp = temp
            bulb.bulbState = state
            bulb.save()
    
    def test_bulb_creation(self):
        """Test if the bulbs are created correctly"""
            
        for name, ip, red, blue, green, temp, state in zip(self.nameArray, self.ipArray, self.redArray, self.blueArray, self.greenArray, self.tempArray, self.stateArray):
            bulb = wizbulb.objects.get(bulbName = name)
            self.assertEqual(bulb.bulbName, name)
            self.assertEqual(bulb.bulbIp, ip)
            self.assertEqual(bulb.bulbRed, red)
            self.assertEqual(bulb.bulbBlue, blue)
            self.assertEqual(bulb.bulbGreen, green)
            self.assertEqual(bulb.bulbTemp, temp)
            self.assertEqual(bulb.bulbState, state)           
            
        print(f"{len(self.nameArray)} bulbs: Passed!", self)
        
