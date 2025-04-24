"""Django models, defines models for the database"""

__author__ = "Ryan Urquhart"
__contact__ = "https://github.com/RyanMcClean"

import os
from django.core.validators import (
    MinLengthValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

# Create your models here.


class Wizbulb(models.Model):
    """Wizbulb object"""

    bulb_ip = models.GenericIPAddressField(null=False, blank=False, unique=True, protocol="ipv4")
    bulb_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        default=None,
        validators=[
            MinLengthValidator(1),
        ],
    )
    bulb_state = models.BooleanField(auto_created=True, null=True, blank=True)
    bulb_red = models.IntegerField(
        null=True, blank=True, validators=[MaxValueValidator(255), MinValueValidator(0)]
    )
    bulb_green = models.IntegerField(
        null=True, blank=True, validators=[MaxValueValidator(255), MinValueValidator(0)]
    )
    bulb_blue = models.IntegerField(
        null=True, blank=True, validators=[MaxValueValidator(255), MinValueValidator(0)]
    )
    bulb_temp = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(2000), MaxValueValidator(6500)],
    )

    def __str__(self) -> str:
        """Returns a summary of wizbulb object

        Returns:
            str: summary of wizbulb object
        """
        try:
            return (
                "-" * os.get_terminal_size()[0]
                + f"\nBulb Ip: {self.bulb_ip}\nBulb Name: {self.bulb_name}\nBulb State: {self.bulb_state}"
                f"\nBulb Red: {self.bulb_red}\nBulb Green {self.bulb_green}\nBulb Blue: {self.bulb_blue}"
                f"\nBulb Temp: {self.bulb_temp}\n" + "-" * os.get_terminal_size()[0]
            )
        except OSError:
            return (
                f"Bulb Ip: {self.bulb_ip}\nBulb Name: {self.bulb_name}\nBulb State: {self.bulb_state}"
                f"\nBulb Red: {self.bulb_red}\nBulb Green {self.bulb_green}\nBulb Blue: {self.bulb_blue}"
                f"\nBulb Temp: {self.bulb_temp}\n"
            )

    def return_json(self) -> dict:
        """JSON dict of fields and values in the object

        Returns:
            dict: JSON dict of fields and values in the object
        """
        return {
            "bulb_ip": self.bulb_ip,
            "bulb_name": self.bulb_name,
            "bulb_state": self.bulb_state,
            "bulb_red": self.bulb_red,
            "bulb_green": self.bulb_green,
            "bulb_blue": self.bulb_blue,
            "bulb_temp": self.bulb_temp,
        }

    objects = models.Manager()
