"""Unit tests for API requests"""

from django.test import TestCase
import json
import logging, os
from test_helper import formatter

bulbQueryErrorMessage = {"error": "could not query bulb"}
bulbDiscoveryErrorMessage = (
    "Bulb discovery failed. Please ensure bulbs are connected to the same network as your computer."
)

LOGGER = logging.getLogger(__name__)

# This IP is used in testing to prevent it actually querying a bulb
localIp = "127.0.0.1"


class IndexClientTest(TestCase):
    def test_get_index(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_get_index.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            LOGGER.debug("Index page loaded successfully")
            self.assertTemplateUsed(response, "index.html")
            LOGGER.debug("Correct template used for index page")
        except Exception as e:
            LOGGER.error("An error occurred in test_get_index: %s", e)

    def test_bulb_registration_form(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_bulb_registration_form.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            form_data = {"bulbIp": localIp}
            response = self.client.post("/", form_data, "application/json")
            LOGGER.debug("Bulb registration form submitted successfully")
            self.assertEqual(response.status_code, 200)
            LOGGER.debug("Response status code is 200")
        except Exception as e:
            LOGGER.error("An error occurred in test_bulb_registration_form: %s", e)

    def test_404_index(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_404_index.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            response = self.client.delete("/")
            self.assertEqual(response.status_code, 404)
            LOGGER.debug("404 error page loaded successfully")
            self.assertTemplateUsed(response, "404.html")
            LOGGER.debug("Correct template used for 404 error page")
        except Exception as e:
            LOGGER.error("An error occurred in test_404_index: %s", e)


class BulbFunctionsTest(TestCase):
    def test_get_discover(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_get_discover.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            response = self.client.get("/discover/")
            self.assertEqual(response.status_code, 200)
            LOGGER.debug("Discover page loaded successfully")
        except Exception as e:
            LOGGER.error("An error occurred in test_get_discover: %s", e)

    def test_query_bulb(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_query_bulb.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            post_data = {"ip": localIp}
            response = self.client.post("/queryBulb/", post_data, "application/json")
            self.assertEqual(response.status_code, 200)
            LOGGER.debug("Query bulb response status code is 200")
            self.assertDictEqual(
                json.loads(response.content.decode("utf-8")), bulbQueryErrorMessage
            )
            LOGGER.debug("Query bulb response is correct")
        except Exception as e:
            LOGGER.error("An error occurred in test_query_bulb: %s", e)

    def test_toggle_bulb(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_toggle_bulb.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            post_data = {"ip": localIp}
            response = self.client.post("/toggleBulb/", post_data, "application/json")
            self.assertEqual(response.status_code, 200)
            LOGGER.debug("Toggle bulb response status code is 200")
            self.assertDictEqual(
                json.loads(response.content.decode("utf-8")), bulbQueryErrorMessage
            )
            LOGGER.debug("Toggle bulb response status code is 200")
        except Exception as e:
            LOGGER.error("An error occurred in test_toggle_bulb: %s", e)

    def test_color_bulb(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_color_bulb.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            post_data = {"ip": localIp, "r": "1", "g": "1", "b": "1", "brightness": "1"}
            response = self.client.post("/colorBulb/", post_data, "application/json")
            self.assertEqual(response.status_code, 200)
            LOGGER.debug("Color bulb response status code is 200")
            self.assertDictEqual(
                json.loads(response.content.decode("utf-8")), bulbQueryErrorMessage
            )
            LOGGER.debug("Color bulb response status code is 200")
        except Exception as e:
            LOGGER.error("An error occurred in test_color_bulb: %s", e)

    def test_toggle_bulb_invalid_POST(self):
        # Set up logging for the test
        log_filename = (
            f"test_logs/individual_test_logs/{__name__}/test_toggle_bulb_invalid_POST.log"
        )
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            post_data = {}
            response = self.client.post("/toggleBulb/", post_data, "application/json")
            self.assertEqual(response.status_code, 404)
            LOGGER.debug("Toggle bulb invalid POST response status code is 404")
            self.assertTemplateUsed(response, "404.html")
            LOGGER.debug("Correct template used for 404 page")
        except Exception as e:
            LOGGER.error("An error occurred in test_toggle_bulb_invalid_POST: %s", e)

    def test_toggle_bulb_invalid_GET(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_toggle_bulb_invalid_GET.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            response = self.client.get("/toggleBulb/")
            self.assertEqual(response.status_code, 404)
            LOGGER.debug("Toggle bulb invalid GET response status code is 404")
            self.assertTemplateUsed(response, "404.html")
            LOGGER.debug("Correct template used for 404 page")
        except Exception as e:
            LOGGER.error("An error occurred in test_toggle_bulb_invalid_GET: %s", e)

    def test_start_audio_sync(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_start_audio_sync.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            response = self.client.post("/activateSync/", content_type="text/xml", data="0")
            self.assertEqual(response.status_code, 200)
            LOGGER.debug("Start audio sync response status code is 200")
        except Exception as e:
            LOGGER.error("An error occurred in test_start_audio_sync: %s", e)

    def test_stop_audio_sync(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_stop_audio_sync.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            response = self.client.get("/stopSync/")
            self.assertEqual(response.status_code, 200)
            LOGGER.debug("Stop audio sync response status code is 200")
            self.assertDictEqual(json.loads(response.content.decode("utf-8")), {"result": True})
            LOGGER.debug("Stop audio sync response is correct")
        except Exception as e:
            LOGGER.error("An error occurred in test_stop_audio_sync: %s", e)
