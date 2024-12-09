from django.test import TestCase


class IndexClientTest(TestCase):
    def test_get_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_post_index(self):
        response = self.client.post("/", {"discover": True})
        self.assertEqual(response.status_code, 200)

    def test_bulb_registration_form(self):
        form_data = {"bulbIp": "192.168.50.80"}
        response = self.client.post("/", form_data)
        self.assertEqual(response.status_code, 200)

    def test_toggle_bulb(self):
        post_data = {"ip": "192.168.50.80"}
        response = self.client.post("/toggleBulb/", post_data)
        self.assertEqual(response.status_code, 200)

    def test_color_bulb(self):
        post_data = {"ip": "192.168.50.80", "r": "1", "g": "1", "b": "1", "brightness": "1"}
        response = self.client.post("/colorBulb/", post_data)
        self.assertEqual(response.status_code, 200)
