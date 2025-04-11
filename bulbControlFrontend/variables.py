"""DESCRIPTION"""

__author__ = "Ryan McClean"
__contact__ = "https://github.com/RyanMcClean"

import json
import os
import logging
try:
    from .models import wizbulb
    from .forms import bulbForm
    from .helpers import NetworkHandler
    from .audioTesting import getWorkingDeviceList
except:
    from models import wizbulb
    from forms import bulbForm
    from helpers import NetworkHandler
    from audioTesting import getWorkingDeviceList

ready = False

def init():
    # Global variables
    global client, context, logger, bulbs, ready, musicSync
    # Global functions
    global separator, messageLoud, messageQuiet, update_bulb_objects, setup_logger, update_working_audio_devices
    # Global classes
    global color



    ready = False
    musicSync = False

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
        if len(bulbs) > 0 and ready:
            for x in bulbs:
                client.update_bulb_db(x)
                if x.bulbIp not in [y["bulbIp"] for y in context["bulbs"]]:
                    context["bulbs"].append(x.returnJSON())
                if x.bulbIp in context["ips"]:
                    context["ips"].remove(x.bulbIp)
        else:
            context["bulbs"] = []
        # Oneliner to remove duplicates from list of dicts https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
        context["bulbs"] = [dict(x) for x in {tuple(y.items()) for y in context["bulbs"]}]
        context["numBulbs"] = len(context["bulbs"])

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
        "musicSync": musicSync,
    }
    logger = setup_logger("Main Logger", "./test_logs/django_server.log", logging.DEBUG)
    bulbs = wizbulb.objects.all()

    def update_working_audio_devices():
        if context["numBulbs"] > 0 or len(context["bulbs"]) > 0:
            devices = getWorkingDeviceList()
            for device in devices:
                if device not in context["audioDevices"]:
                    context["audioDevices"].append(device)
        context["audioDevices"] = [dict(x) for x in {tuple(y.items()) for y in context["audioDevices"]}]

    ready = True
