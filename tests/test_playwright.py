from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
import os


class PlaywrightTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        cls.playwright = sync_playwright().start()
        cls.chromium = cls.playwright.chromium.launch(headless=False, slow_mo=100)

    @classmethod
    def tearDownClass(cls):
        cls.chromium.close()
        cls.playwright.stop()
        return super().tearDownClass()

    def test_load_index(self):
        chromiumPage = self.chromium.new_page()
        chromiumPage.goto(f"{self.live_server_url}")
        chromiumFindButton = chromiumPage.locator("#find-bulbs-button")
        chromiumFindButton.wait_for()
        self.assertEqual(chromiumPage.title(), "Bulb Bop")

    def test_load_discover(self):
        chromiumPage = self.chromium.new_page()
        chromiumPage.goto(f"{self.live_server_url}/discover")
        chromiumFindButton = chromiumPage.locator("#find-bulbs-button")
        chromiumFindButton.wait_for(timeout=0, state="attached")
        self.assertEqual(chromiumPage.title(), "Bulb Bop")
