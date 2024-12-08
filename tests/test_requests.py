from django.test import TestCase


class IndexClientTest(TestCase):
    def test_index_django(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
