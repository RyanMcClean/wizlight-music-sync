from django.test import TestCase
import json

bulbQueryErrorMessage = {"error": "could not query bulb"}
bulbDiscoveryErrorMessage = (
    "Bulb discovery failed. Please ensure bulbs are connected to the same network as your computer."
)

# This IP is used in testing to prevent it actually querying a bulb
localIp = "127.0.0.1"


class IndexClientTest(TestCase):
    def test_get_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_post_index(self):
        response = self.client.post("/", {"discover": ""}, "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["errorMessage"], bulbDiscoveryErrorMessage)

    def test_bulb_registration_form(self):
        form_data = {"bulbIp": localIp}
        response = self.client.post("/", form_data, "application/json")
        self.assertEqual(response.status_code, 200)


class BulbFunctionsTest(TestCase):
    def test_query_bulb(self):
        post_data = {"ip": localIp}
        response = self.client.post("/queryBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), bulbQueryErrorMessage)

    def test_toggle_bulb(self):
        post_data = {"ip": localIp}
        response = self.client.post("/toggleBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), bulbQueryErrorMessage)

    def test_color_bulb(self):
        post_data = {"ip": localIp, "r": "1", "g": "1", "b": "1", "brightness": "1"}
        response = self.client.post("/colorBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(json.loads(response.content.decode("utf-8")), bulbQueryErrorMessage)

    def test_toggle_bulb_invalid_POST(self):
        post_data = {}
        response = self.client.post("/toggleBulb/", post_data, "application/json")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_toggle_bulb_invalid_GET(self):
        response = self.client.get("/toggleBulb/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
