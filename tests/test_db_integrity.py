# pylint: disable = broad-exception-caught, anomalous-backslash-in-string
"""Test database for integrity,
add models directly to database,
should pass or fail depending on table restrictions
"""

from random import randint
import logging
from django.db import IntegrityError
from django.test import TestCase
from test_helper import setup_logger
from bulb_control_frontend.models import Wizbulb


LOGGER = logging.getLogger(__name__)


class DBIntegrityTests(TestCase):
    """Test database integrity"""

    @classmethod
    def setUpTestData(cls):
        pass

    def test_set_null_object(self):
        """Test null bulb cannot be set"""
        setup_logger(__name__, LOGGER)

        with self.assertRaisesRegex(
            IntegrityError,
            "NOT NULL constraint failed: bulb_control_frontend_wizbulb\.bulb_ip",
        ):
            Wizbulb.objects.create()
            LOGGER.debug("Null object creation failed as expected")

    def test_set_null_ip(self):
        """Test null ip cannot be set"""
        setup_logger(__name__, LOGGER)

        with self.assertRaisesRegex(
            IntegrityError,
            "NOT NULL constraint failed: bulb_control_frontend_wizbulb\.bulb_ip",
        ):
            Wizbulb.objects.create(bulb_name="Test Bulb")
            LOGGER.debug("Null IP creation failed as expected")

    def test_set_null_name(self):
        """Test null name cannot be set"""
        setup_logger(__name__, LOGGER)

        with self.assertRaisesRegex(
            IntegrityError,
            "NOT NULL constraint failed: bulb_control_frontend_wizbulb\.bulb_name",
        ):
            Wizbulb.objects.create(bulb_ip=".".join(str(randint(1, 254)) for _ in range(4)))
            LOGGER.debug("Null name creation failed as expected")

    def test_set_valid_bulb(self):
        """Test valid bulbs can be set, used as a control for the above tests"""
        setup_logger(__name__, LOGGER)

        Wizbulb.objects.create(
            bulb_name="Test Bulb",
            bulb_ip=".".join(str(randint(1, 254)) for _ in range(4)),
            bulb_red=randint(0, 255),
            bulb_green=randint(0, 255),
            bulb_blue=randint(0, 255),
            bulb_temp=randint(2000, 6500),
            bulb_state=True,
        )
        LOGGER.debug("Valid bulb creation passed")
