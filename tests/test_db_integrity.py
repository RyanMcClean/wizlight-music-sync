# pylint: disable = broad-exception-caught, anomalous-backslash-in-string
"""Test database for integrity,
add models directly to database,
should pass or fail depending on table restrictions
"""

from random import randint
import logging
import os
from django.db import IntegrityError
from django.test import TestCase
from test_helper import formatter
from bulb_control_frontend.models import Wizbulb


LOGGER = logging.getLogger(__name__)


class DBIntegrityTests(TestCase):
    """Test database integrity"""

    @classmethod
    def setUpTestData(cls):
        pass

    def test_set_null_object(self):
        """Test null bulb cannot be set"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_null_object.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)

        with self.assertRaisesRegex(
            IntegrityError,
            "NOT NULL constraint failed: bulb_control_frontend_wizbulb\.bulb_ip",
        ):
            Wizbulb.objects.create()
            LOGGER.debug("Null object creation failed as expected")

    def test_set_null_ip(self):
        """Test null ip cannot be set"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_null_ip.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)

        with self.assertRaisesRegex(
            IntegrityError,
            "NOT NULL constraint failed: bulb_control_frontend_wizbulb\.bulb_ip",
        ):
            Wizbulb.objects.create(bulb_name="Test Bulb")
            LOGGER.debug("Null IP creation failed as expected")

    def test_set_null_name(self):
        """Test null name cannot be set"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_set_null_name.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)

        with self.assertRaisesRegex(
            IntegrityError,
            "NOT NULL constraint failed: bulb_control_frontend_wizbulb\.bulb_name",
        ):
            Wizbulb.objects.create(bulb_ip=".".join(str(randint(1, 254)) for _ in range(4)))
            LOGGER.debug("Null name creation failed as expected")
