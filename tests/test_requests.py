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


class IndexClientTest(TestCase):
    """Test class for testing the api via python requests"""

    def test_get_index(self):
        """Test get the index page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Index page loaded successfully")
        self.assertTemplateUsed(response, "index.html")
        LOGGER.debug("Correct template used for index page")

    def test_bulb_registration_form(self):
        """test bulb form submission"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        form_data = {"bulb_ip": LOCAL_IP}
        response = self.client.post("/", form_data, "application/json")
        LOGGER.debug("Bulb registration form submitted successfully")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Response status code is 200")

    def test_404_index(self):
        """Test invalid index get for 404 page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        response = self.client.delete("/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Index returned not found for DELETE request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put("/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Index returned not found for PUT request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch("/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Index returned not found for PATCH request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")


class BulbFunctionsTest(TestCase):
    """Test class for testing bulb functions via API"""

    def test_discover_rest_requests(self):
        """test get Discover page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        response = self.client.get("/discover/")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Discover page loaded successfully")
        self.assertTemplateUsed(response, "index.html")
        LOGGER.debug("Correct template used for Discover page")

        response = self.client.post("/discover/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Discover returned not found for POST request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete("/discover/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Discover returned not found for DELETE request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put("/discover/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Discover returned not found for PUT request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch("/discover/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Discover returned not found for PATCH request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_query_bulb(self):
        """test query bulb"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        post_data = {"ip": LOCAL_IP}
        response = self.client.post("/queryBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Query bulb response status code is 200")
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")), {"error": "bulb does not exist"}
        )
        LOGGER.debug("Query bulb response is correct")

        post_data = {}
        response = self.client.post("/queryBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Query bulb invalid POST response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.get("/queryBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Query bulb invalid GET response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put("/queryBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Query bulb invalid PUT response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete("/queryBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Query bulb invalid DELETE response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch("/queryBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Query bulb invalid PATCH response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_toggle_bulb(self):
        """test toggle bulb"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        post_data = {"ip": LOCAL_IP}
        response = self.client.post("/toggleBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Toggle bulb response status code is 200")
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), BULB_QUERY_ERROR_MESSAGE)
        LOGGER.debug("Toggle bulb response status code is 200")

        post_data = {}
        response = self.client.post("/toggleBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Toggle bulb invalid POST response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.get("/toggleBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Toggle bulb invalid GET response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put("/toggleBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Toggle bulb invalid PUT response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete("/toggleBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Toggle bulb invalid DELETE response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch("/toggleBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Toggle bulb invalid PATCH response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_color_bulb(self):
        """test turn bulb to colour"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        post_data = {"ip": LOCAL_IP, "r": "1", "g": "1", "b": "1", "brightness": "1"}
        response = self.client.post("/colorBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Color bulb response status code is 200")
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), BULB_QUERY_ERROR_MESSAGE)
        LOGGER.debug("Color bulb response status code is 200")

        response = self.client.get("/colorBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Color bulb invalid GET response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put("/colorBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Color bulb invalid PUT response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete("/colorBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Color bulb invalid DELETE response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch("/colorBulb/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Color bulb invalid PATCH response status code is 404")
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

    def test_start_audio_sync(self):
        """test start audio sync"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        response = self.client.post("/activateSync/", content_type="text/xml", data="0")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Start audio sync response status code is 200")

        response = self.client.get("/activateSync/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Activate Sync invalid GET response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put("/activateSync/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Activate Sync invalid PUT response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete("/activateSync/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Activate Sync invalid DELETE response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch("/activateSync/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Activate Sync invalid PATCH response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_stop_audio_sync(self):
        """test stop audio sync"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        response = self.client.post("/stopSync/")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("Stop audio sync response status code is 200")
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), {"result": True})
        LOGGER.debug("Stop audio sync response is correct")

        response = self.client.get("/stopSync/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Stop Sync invalid GET response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put("/stopSync/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Stop Sync invalid PUT response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete("/stopSync/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Stop Sync invalid DELETE response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch("/stopSync/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("Stop Sync invalid PATCH response status code is 404")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")


class EndpointTests(TestCase):
    """Test class for testing api endpoints"""

    def test_crud_rest_requests(self):
        """test get crud page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        response = self.client.get("/crud/")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("CRUD page loaded successfully")
        self.assertTemplateUsed(response, "bulb_crud.html")
        LOGGER.debug("Correct template used for CRUD page")

        response = self.client.post("/crud/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("CRUD returned not found for POST request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete("/crud/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("CRUD returned not found for DELETE request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put("/crud/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("CRUD returned not found for PUT request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch("/crud/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("CRUD returned not found for PATCH request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_about_rest_requests(self):
        """test get about page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("About page loaded successfully")
        self.assertTemplateUsed(response, "about.html")
        LOGGER.debug("Correct template used for CRUD page")

        response = self.client.post("/about/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("About returned not found for POST request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete("/about/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("About returned not found for DELETE request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put("/about/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("About returned not found for PUT request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch("/about/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("About returned not found for PATCH request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

    def test_faq_rest_requests(self):
        """test get faq page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        response = self.client.get("/faq/")
        self.assertEqual(response.status_code, 200)
        LOGGER.debug("FAQ page loaded successfully")
        self.assertTemplateUsed(response, "faq.html")
        LOGGER.debug("Correct template used for CRUD page")

        response = self.client.post("/faq/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("FAQ returned not found for POST request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.delete("/faq/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("FAQ returned not found for DELETE request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.put("/faq/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("FAQ returned not found for PUT request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")

        response = self.client.patch("/faq/")
        self.assertEqual(response.status_code, 404)
        LOGGER.debug("FAQ returned not found for PATCH request")
        self.assertTemplateUsed(response, "404.html")
        LOGGER.debug("Correct template used for 404 page")
