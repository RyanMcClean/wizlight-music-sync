from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect
import os


class PlaywrightTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        cls.playwright = sync_playwright().start()
        cls.chromium = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.chromium.close()
        cls.playwright.stop()
        return super().tearDownClass()

    def test_load_index(self):
        chromiumPage = self.chromium.new_page()
        chromiumPage.goto(f"{self.live_server_url}")
        chromiumPage.locator("#find-bulbs-button").wait_for()
        self.assertEqual(chromiumPage.title(), "Bulb Bop")
        expect(chromiumPage.locator("#main-title")).to_be_visible()
        expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible()
        expect(chromiumPage.locator("#home-link")).to_be_visible()
        expect(chromiumPage.locator("#faq-link")).to_be_visible()
        expect(chromiumPage.locator("#about-link")).to_be_visible()

    def test_load_discover(self):
        chromiumPage = self.chromium.new_page()
        chromiumPage.goto(f"{self.live_server_url}/discover")
        chromiumFindButton = chromiumPage.locator("#find-bulbs-button")
        chromiumFindButton.wait_for(timeout=0, state="attached")
        self.assertEqual(chromiumPage.title(), "Bulb Bop")
        expect(chromiumPage.locator("#main-title")).to_be_visible()
        expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible()
        expect(chromiumPage.locator("#home-link")).to_be_visible()
        expect(chromiumPage.locator("#faq-link")).to_be_visible()
        expect(chromiumPage.locator("#about-link")).to_be_visible()

    def test_from_index_to_discover(self):
        chromiumPage = self.chromium.new_page()
        chromiumPage.goto(f"{self.live_server_url}")
        chromiumFindButton = chromiumPage.locator("#find-bulbs-button")
        chromiumFindButton.wait_for(timeout=0, state="attached")
        chromiumFindButton.click()
        chromiumFindButton.wait_for(timeout=0, state="attached")
        url = chromiumPage.url
        print(url)
        self.assertIn("discover", url)
        self.assertEqual(chromiumPage.title(), "Bulb Bop")
        expect(chromiumPage.locator("#main-title")).to_be_visible()
        expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible()
        expect(chromiumPage.locator("#home-link")).to_be_visible()
        expect(chromiumPage.locator("#faq-link")).to_be_visible()
        expect(chromiumPage.locator("#about-link")).to_be_visible()

    def test_from_discover_to_index(self):
        chromiumPage = self.chromium.new_page()
        chromiumPage.goto(f"{self.live_server_url}/discover")
        chromiumPage.locator("#find-bulbs-button").wait_for(timeout=0, state="attached")
        chromiumPage.locator("#home-link").click()
        chromiumPage.locator("#find-bulbs-button").wait_for(timeout=0, state="attached")
        url = chromiumPage.url
        print(url)
        self.assertNotIn("discover", url)
        self.assertEqual(chromiumPage.title(), "Bulb Bop")
        expect(chromiumPage.locator("#main-title")).to_be_visible()
        expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible()
        expect(chromiumPage.locator("#home-link")).to_be_visible()
        expect(chromiumPage.locator("#faq-link")).to_be_visible()
        expect(chromiumPage.locator("#about-link")).to_be_visible()
