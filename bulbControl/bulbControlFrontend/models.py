"""Django models, defines models for the database"""

__author__ = "Ryan McClean"
__contact__ = "https://github.com/RyanMcClean"

import os

from django.db import models

# Create your models here.


class wizbulb(models.Model):
    """Wizbulb object"""

    bulbIp = models.CharField(max_length=255, null=True, unique=True)
    bulbName = models.CharField(max_length=255, null=True, unique=True)
    bulbState = models.BooleanField(auto_created=True, null=True)
    bulbRed = models.IntegerField(null=True)
    bulbGreen = models.IntegerField(null=True)
    bulbBlue = models.IntegerField(null=True)
    bulbTemp = models.IntegerField(null=True)

    def __str__(self) -> str:
        """Returns a summary of wizbulb object

        Returns:
            str: summary of wizbulb object
        """
        return (
            "-"
            * os.get_terminal_size()[0]
            + f"\nBulb Ip: {self.bulbIp}\nBulb Name: {self.bulbName}\nBulb State: {self.bulbState}"
            "\nBulb Red: {self.bulbRed}\nBulb Green {self.bulbGreen}\nBulb Blue: {self.bulbBlue}"
            "\nBulb Temp: {self.bulbTemp}\n" + "-" * os.get_terminal_size()[0]
        )

    def returnJSON(self) -> dict:
        """JSON dict of fields and values in the object

        Returns:
            dict: JSON dict of fields and values in the object
        """
        return {
            "BulbIp": self.bulbIp,
            "BulbName": self.bulbName,
            "BulbState": self.bulbState,
            "BulbRed": self.bulbRed,
            "bulbGreen": self.bulbGreen,
            "bulbBlue": self.bulbBlue,
            "bulbTemp": self.bulbTemp,
        }

    objects = models.Manager()
