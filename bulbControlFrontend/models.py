"""Django models, defines models for the database"""

__author__ = "Ryan McClean"
__contact__ = "https://github.com/RyanMcClean"

import os

from django.core.validators import validate_ipv4_address
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.

class wizbulb(models.Model):
    """Wizbulb object"""

    bulbIp = models.GenericIPAddressField(
        null=False,
        blank=False,
        unique=True,
        protocol='ipv4')
    bulbName = models.CharField(
        max_length=255, 
        null=False,
        blank=False, 
        unique=True, 
        default=None,
        validators=[
            MinLengthValidator(1),
        ])
    bulbState = models.BooleanField(
        auto_created=True, 
        null=True,
        blank=True)
    bulbRed = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(255),
            MinValueValidator(0)
        ])
    bulbGreen = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(255),
            MinValueValidator(0)
        ])
    bulbBlue = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(255),
            MinValueValidator(0)
        ])
    bulbTemp = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])

    def __str__(self) -> str:
        """Returns a summary of wizbulb object

        Returns:
            str: summary of wizbulb object
        """
        try:
            return (
                "-"
                * os.get_terminal_size()[0]
                + f"\nBulb Ip: {self.bulbIp}\nBulb Name: {self.bulbName}\nBulb State: {self.bulbState}"
                f"\nBulb Red: {self.bulbRed}\nBulb Green {self.bulbGreen}\nBulb Blue: {self.bulbBlue}"
                f"\nBulb Temp: {self.bulbTemp}\n" + "-" * os.get_terminal_size()[0]
            )
        except OSError as e:
            return (f"Bulb Ip: {self.bulbIp}\nBulb Name: {self.bulbName}\nBulb State: {self.bulbState}"
                f"\nBulb Red: {self.bulbRed}\nBulb Green {self.bulbGreen}\nBulb Blue: {self.bulbBlue}"
                f"\nBulb Temp: {self.bulbTemp}\n")

    def returnJSON(self) -> dict:
        """JSON dict of fields and values in the object

        Returns:
            dict: JSON dict of fields and values in the object
        """
        return {
            "bulbIp": self.bulbIp,
            "bulbName": self.bulbName,
            "bulbState": self.bulbState,
            "bulbRed": self.bulbRed,
            "bulbGreen": self.bulbGreen,
            "bulbBlue": self.bulbBlue,
            "bulbTemp": self.bulbTemp,
        }

    objects = models.Manager()
