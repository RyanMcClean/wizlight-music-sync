from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect
import os
import logging

LOGGER = logging.getLogger(__name__)


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
        chromiumPage.locator("#find-bulbs-button").wait_for(state='attached')
        self.assertEqual(chromiumPage.title(), "Bulb Bop")
        expect(chromiumPage.locator("#main-title")).to_be_visible(); LOGGER.debug("Checked visibility of #main-title")
        expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible(); LOGGER.debug("Checked visibility of #find-bulbs-button")
        expect(chromiumPage.locator("#home-link")).to_be_visible(); LOGGER.debug("Checked visibility of #home-link")
        expect(chromiumPage.locator("#faq-link")).to_be_visible(); LOGGER.debug("Checked visibility of #faq-link")
        expect(chromiumPage.locator("#about-link")).to_be_visible(); LOGGER.debug("Checked visibility of #about-link")

    def test_load_discover(self):
        chromiumPage = self.chromium.new_page()
        chromiumPage.goto(f"{self.live_server_url}/discover")
        chromiumPage.locator("#find-bulbs-button").wait_for(state='attached')
        self.assertEqual(chromiumPage.title(), "Bulb Bop")
        expect(chromiumPage.locator("#main-title")).to_be_visible(); LOGGER.debug("Checked visibility of #main-title")
        expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible(); LOGGER.debug("Checked visibility of #find-bulbs-button")
        expect(chromiumPage.locator("#home-link")).to_be_visible(); LOGGER.debug("Checked visibility of #home-link")
        expect(chromiumPage.locator("#faq-link")).to_be_visible(); LOGGER.debug("Checked visibility of #faq-link")
        expect(chromiumPage.locator("#about-link")).to_be_visible(); LOGGER.debug("Checked visibility of #about-link")

    def test_from_index_to_discover(self):
        chromiumPage = self.chromium.new_page()
        chromiumPage.goto(f"{self.live_server_url}")
        chromiumFindButton = chromiumPage.locator("#find-bulbs-button")
        chromiumFindButton.wait_for(state="attached")
        chromiumFindButton.click()
        chromiumFindButton.wait_for(state="attached")
        url = chromiumPage.url
        self.assertIn("discover", url)
        self.assertEqual(chromiumPage.title(), "Bulb Bop")
        expect(chromiumPage.locator("#main-title")).to_be_visible(); LOGGER.debug("Checked visibility of #main-title")
        expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible(); LOGGER.debug("Checked visibility of #find-bulbs-button")
        expect(chromiumPage.locator("#home-link")).to_be_visible(); LOGGER.debug("Checked visibility of #home-link")
        expect(chromiumPage.locator("#faq-link")).to_be_visible(); LOGGER.debug("Checked visibility of #faq-link")
        expect(chromiumPage.locator("#about-link")).to_be_visible(); LOGGER.debug("Checked visibility of #about-link")

    def test_from_discover_to_index(self):
        chromiumPage = self.chromium.new_page()
        chromiumPage.goto(f"{self.live_server_url}/discover"); LOGGER.debug("Page URL: %s", chromiumPage.url)
        chromiumPage.locator("#find-bulbs-button").wait_for(timeout=0, state="attached"); LOGGER.debug("Find bulbs button found")
        chromiumPage.locator("#home-link").click(); LOGGER.debug("Home link clicked")
        chromiumPage.locator("#find-bulbs-button").wait_for(timeout=0, state="attached"); LOGGER.debug("Find bulbs button found")
        url = chromiumPage.url; LOGGER.debug("Page URL: %s", url)
        self.assertNotIn("discover", url); LOGGER.debug("Discover not found in URL")
        self.assertEqual(chromiumPage.title(), "Bulb Bop"); LOGGER.debug("Page title is Bulb Bop")
        if chromiumPage.locator(".bulb-icon"):
            expect(chromiumPage.locator("#error-toast")).to_have_count(0); LOGGER.debug("No error toast found")
        else:
            expect(chromiumPage.locator("#error-toast")).to_be_visible(); LOGGER.debug("Error toast found")
        expect(chromiumPage.locator("#main-title")).to_be_visible(); LOGGER.debug("Checked visibility of #main-title")
        expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible(); LOGGER.debug("Checked visibility of #find-bulbs-button")
        expect(chromiumPage.locator("#home-link")).to_be_visible(); LOGGER.debug("Checked visibility of #home-link")
        expect(chromiumPage.locator("#faq-link")).to_be_visible(); LOGGER.debug("Checked visibility of #faq-link")
        expect(chromiumPage.locator("#about-link")).to_be_visible(); LOGGER.debug("Checked visibility of #about-link")
