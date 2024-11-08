from django.db import models

# Create your models here.

class wizBulb(models.Model):
    bulbIp = models.CharField(max_length=255, null=True, unique=True)
    bulbName = models.CharField(max_length=255, null=True, unique=True)
    bulbState = models.BooleanField(auto_created=True, null=True)
    bulbRed = models.IntegerField(null=True)
    bulbGreen = models.IntegerField(null=True)
    bulbBlue = models.IntegerField(null=True)
    bulbTemp = models.IntegerField(null=True)
    
    def __str__(self):
        return "-" * 20 + f"\nBulb Ip: %s\nBulb Name: %s\nBulb State: %s\nBulb Red: %s\nBulb Green %s\nBulb Blue: %s\nBulb Temp: %s\n" % (self.bulbIp, self.bulbName
, self.bulbState, self.bulbRed, self.bulbGreen, self.bulbBlue, self.bulbTemp) + "-" * 20

    def returnJSON(self):
        return {
            'BulbIp': self.bulbIp,
            'BulbName': self.bulbName,
            'BulbState': self.bulbState,
            'BulbRed': self.bulbRed,
            'bulbGreen': self.bulbGreen,
            'bulbBlue': self.bulbBlue,
            'bulbTemp': self.bulbTemp,
        }
