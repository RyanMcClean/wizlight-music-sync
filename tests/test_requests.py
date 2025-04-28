"""Unit tests for API requests"""

import json
import logging
from django.test import TestCase
from test_helper import setup_logger

BULB_QUERY_ERROR_MESSAGE = {"error": "could not query bulb"}
BULB_DISCOVERY_ERROR_MESSAGE = (
    "Bulb discovery failed. Please ensure bulbs are connected to the same network as your computer."
)

LOGGER = logging.getLogger(__name__)

# This IP is used in testing to prevent it actually querying a bulb
LOCAL_IP = "127.0.0.1"


class IndexClientTest(TestCase):
    """Test class for testing the api via python requests"""

    def test_get_index(self):
        """Test get the index page"""
        setup_logger(__name__, LOGGER)

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Index page loaded successfully")
        self.assertTemplateUsed(response, "index.html")
        LOGGER.debug("Correct template used for index page")

    def test_bulb_registration_form(self):
        """test bulb form submission"""
        setup_logger(__name__, LOGGER)

        form_data = {"bulb_ip": LOCAL_IP}
        response = self.client.post("/", form_data, "application/json")
        LOGGER.debug("Bulb registration form submitted successfully")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Response status code is 200")

    def test_404_index(self):
        """Test invalid index get for 404 page"""
        setup_logger(__name__, LOGGER)

        response = self.client.delete("/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("404 error page loaded successfully")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 error page")


class BulbFunctionsTest(TestCase):
    """Test class for testing bulb functions via API"""

    def test_get_discover(self):
        """test get discover page"""
        setup_logger(__name__, LOGGER)

        response = self.client.get("/discover/")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Discover page loaded successfully")

    def test_query_bulb(self):
        """test query bulb"""
        setup_logger(__name__, LOGGER)

        post_data = {"ip": LOCAL_IP}
        response = self.client.post("/queryBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Query bulb response status code is 200")
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), BULB_QUERY_ERROR_MESSAGE)
        LOGGER.debug("Query bulb response is correct")

    def test_toggle_bulb(self):
        """test toggle bulb"""
        setup_logger(__name__, LOGGER)

        post_data = {"ip": LOCAL_IP}
        response = self.client.post("/toggleBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Toggle bulb response status code is 200")
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), BULB_QUERY_ERROR_MESSAGE)
        LOGGER.debug("Toggle bulb response status code is 200")

    def test_color_bulb(self):
        """test turn bulb to colour"""
        setup_logger(__name__, LOGGER)

        post_data = {"ip": LOCAL_IP, "r": "1", "g": "1", "b": "1", "brightness": "1"}
        response = self.client.post("/colorBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Color bulb response status code is 200")
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), BULB_QUERY_ERROR_MESSAGE)
        LOGGER.debug("Color bulb response status code is 200")

    def test_toggle_bulb_invalid_post(self):
        """test toggle bulb with invalid POST request"""
        setup_logger(__name__, LOGGER)

        post_data = {}
        response = self.client.post("/toggleBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Toggle bulb invalid POST response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_toggle_bulb_invalid_get(self):
        """test toggle bulb with invalid GET request"""
        setup_logger(__name__, LOGGER)

        response = self.client.get("/toggleBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Toggle bulb invalid GET response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_start_audio_sync(self):
        """test start audio sync"""
        setup_logger(__name__, LOGGER)

        response = self.client.post("/activateSync/", content_type="text/xml", data="0")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Start audio sync response status code is 200")

    def test_stop_audio_sync(self):
        """test stop audio sync"""
        setup_logger(__name__, LOGGER)

        response = self.client.get("/stopSync/")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Stop audio sync response status code is 200")
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), {"result": True})
        LOGGER.debug("Stop audio sync response is correct")
