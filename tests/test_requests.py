"""Unit tests for API requests"""

import json
import inspect
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


class BulbFunctionsTest(TestCase):
    """Test class for testing bulb functions via API"""

    def test_discover_rest_requests(self):
        """test get Discover page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/discover/"
        view = "Discover"

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s page loaded successfully", view)
        self.assertTemplateUsed(response, "index.html")
        LOGGER.debug("Correct template used for %s page", view)

        response = self.client.post(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for POST request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for DELETE request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PUT request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PATCH request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_query_bulb(self):
        """test query bulb"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/queryBulb/"
        view = "Query Bulb"

        post_data = {"ip": LOCAL_IP}
        response = self.client.post(endpoint, post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s response status code is 200", view)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")), {"error": "bulb does not exist"}
        )
        LOGGER.debug("%s response is correct", view)

        post_data = {}
        response = self.client.post(endpoint, post_data, "application/json")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid POST response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid GET response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PUT response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid DELETE response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PATCH response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_toggle_bulb(self):
        """test toggle bulb"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/toggleBulb/"
        view = "Toggle Bulb"

        post_data = {"ip": LOCAL_IP}
        response = self.client.post(endpoint, post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s response status code is 200", view)
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), BULB_QUERY_ERROR_MESSAGE)
        LOGGER.debug("%s response status code is 200", view)

        post_data = {}
        response = self.client.post(endpoint, post_data, "application/json")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid POST response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid GET response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PUT response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid DELETE response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PATCH response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_color_bulb(self):
        """test turn bulb to colour"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/colorBulb/"
        view = "Color Bulb"

        post_data = {"ip": LOCAL_IP, "r": "1", "g": "1", "b": "1", "brightness": "1"}
        response = self.client.post(endpoint, post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s response status code is 200", view)
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), BULB_QUERY_ERROR_MESSAGE)
        LOGGER.debug("%s response status code is 200", view)

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid GET response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PUT response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid DELETE response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PATCH response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_delete_bulb_rest_requests(self):
        """test get faq page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        view = "Delete Bulb"
        endpoint = "/delete/" + LOCAL_IP

        response = self.client.post(endpoint)
        self.assertEqual(response.status_code, 302)
        LOGGER.debug("%s page loaded successfully note: is redirected to crud page", view)
        self.assertRedirects(response, "/crud/")
        LOGGER.debug("Correct template used for CRUD page")

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for GET request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for DELETE request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PUT request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PATCH request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_edit_bulb_rest_requests(self):
        """test edit endpoint"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        view = "Edit Bulb"
        endpoint = "/edit/" + LOCAL_IP

        response = self.client.post(endpoint)
        self.assertEqual(response.status_code, 302)
        LOGGER.debug("%s page loaded successfully, note: is redirect back to crud page", view)
        self.assertRedirects(response, "/crud/")
        LOGGER.debug("Correct template used for CRUD page")

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for GET request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for DELETE request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PUT request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PATCH request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_activate_audio_sync(self):
        """test activate audio sync"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/activateSync/"
        view = "Activate Audio Sync"

        response = self.client.post(endpoint, content_type="text/xml", data="0")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s response status code is 200", view)
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), {"result": True})
        LOGGER.debug("%s response is correct", view)

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid GET response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PUT response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid DELETE response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PATCH response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_stop_audio_sync(self):
        """test stop audio sync"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/stopSync/"
        view = "Stop Audio Sync"

        response = self.client.post(endpoint)
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s response status code is 200", view)
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), {"result": True})
        LOGGER.debug("%s response is correct", view)

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid GET response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PUT response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid DELETE response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PATCH response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_clear_success(self):
        """test clear success message"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/clearSuccess/"
        view = "Clear Success Message"

        response = self.client.post(endpoint)
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s response status code is 200", view)
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), {"result": True})
        LOGGER.debug("%s response is correct", view)

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid GET response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PUT response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid DELETE response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PATCH response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_clear_error(self):
        """test clear error message"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/clearError/"
        view = "Clear Error Message"

        response = self.client.post(endpoint)
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s response status code is 200", view)
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), {"result": True})
        LOGGER.debug("%s response is correct", view)

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid GET response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PUT response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid DELETE response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s invalid PATCH response status code is 404", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")


class EndpointTests(TestCase):
    """Test class for testing api endpoints"""

    def test_index_rest_requests(self):
        """Test the index page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/"
        view = "Index"

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s page loaded successfully", view)
        self.assertTemplateUsed(response, "index.html")
        LOGGER.debug("Correct template used for %s page", view)

        form_data = {"bulb_ip": LOCAL_IP}

        response = self.client.post(endpoint, form_data, "application/json")
        LOGGER.debug("Bulb registration form submitted successfully")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Response status code is 200")
        self.assertTemplateUsed(response, "index.html")
        LOGGER.debug("Correct template used for %s page", view)

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for DELETE request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PUT request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PATCH request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_crud_rest_requests(self):
        """test get crud page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/crud/"
        view = "CRUD"

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s page loaded successfully", view)
        self.assertTemplateUsed(response, "bulb_crud.html")
        LOGGER.debug("Correct template used for CRUD page")

        response = self.client.post(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for POST request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for DELETE request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PUT request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PATCH request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_about_rest_requests(self):
        """test get about page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/about/"
        view = "About"

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s page loaded successfully", view)
        self.assertTemplateUsed(response, "about.html")
        LOGGER.debug("Correct template used for CRUD page")

        response = self.client.post(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for POST request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for DELETE request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PUT request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PATCH request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_faq_rest_requests(self):
        """test get faq page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        endpoint = "/faq/"
        view = "FAQ"

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("%s page loaded successfully", view)
        self.assertTemplateUsed(response, "faq.html")
        LOGGER.debug("Correct template used for CRUD page")

        response = self.client.post(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for POST request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for DELETE request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PUT request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch(endpoint)
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("%s returned not found for PATCH request", view)
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")
