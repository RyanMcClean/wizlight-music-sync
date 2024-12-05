from django.test import TestCase


class MyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData")

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_my_first_method(self):
        print("test_my_first_method")
        self.assertTrue(True)

    def test_my_second_method(self):
        print("test_my_second_method")
        self.assertFalse(True)
