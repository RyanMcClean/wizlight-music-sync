"""DESCRIPTION"""

__author__ = "Ryan McClean"
__contact__ = "https://github.com/RyanMcClean"

import json
import os
import logging
from .models import wizbulb
from .forms import bulbForm
from .helpers import NetworkHandler


def init():
    # Global variables
    global client, context, logger, bulbs, init
    # Global functions
    global separator, messageLoud, messageQuiet, update_bulb_objects, setup_logger
    # Global classes
    global color

    def separator() -> None:
        try:
            print("-" * os.get_terminal_size()[0])
        except OSError:
            print("-" * 5)

    def messageLoud(text, type="text"):
        match type:
            case "text":
                print(str(text))
                logger.info(str(text))
            case "percentage":
                print(str(text), end="\r")
            case "error":
                print(color.RED + str(text) + color.END)
                logger.error(str(text))
            case "fatal error":
                print(color.RED + str(text) + color.END)
                logger.error(str(text))
                exit(1)

    def messageQuiet(*args, **kwargs):
        pass

    def update_bulb_objects():
        # To add a limit to the returned bulb objects the line would read:
        # bulbs = wizbulb.objects.all()[x]
        # where x is the number of bulb objects returned
        bulbs = wizbulb.objects.all()
        context["bulbs"] = []
        for x in bulbs:
            client.update_bulb_objects(x)
            if x.returnJSON() not in context["bulbs"]:
                context["bulbs"].append(x.returnJSON())
            if x.bulbIp in context["ips"]:
                context["ips"].remove(x.bulbIp)

    def setup_logger(name, log_file, level) -> logging.Logger:
        """Setup as many loggers as needed

        Args:
            name (String): _
            log_file (File): Location for log file
            level (int|String): Log level

        Returns:
            logging.Logger: Logger
        """

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        handler = logging.FileHandler(log_file, mode="w")
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    class color:
        PURPLE = "\033[1;35;48m"
        CYAN = "\033[1;36;48m"
        BOLD = "\033[1;37;48m"
        BLUE = "\033[1;34;48m"
        GREEN = "\033[1;32;48m"
        YELLOW = "\033[1;33;48m"
        RED = "\033[1;31;48m"
        BLACK = "\033[1;30;48m"
        UNDERLINE = "\033[4;37;48m"
        END = "\033[1;37;0m"

    client = NetworkHandler()
    context = {
        "regForm": bulbForm(),
        "ips": [],
        "count": 0,
        "bulbs": [],
        "numBulbs": 0,
        "audioDevices": [],
        "error": False,
        "errorMessage": "No error",
    }
    logger = setup_logger("Main Logger", "./django_server.log", logging.DEBUG)
    bulbs = wizbulb.objects.all()

    init = True