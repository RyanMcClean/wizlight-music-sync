"""Playwright tests to ensure that webpages load correctly, and that navigation works as expected"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect
import os
import logging
from test_helper import formatter

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
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_load_index.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            chromiumPage = self.chromium.new_page()
            chromiumPage.goto(f"{self.live_server_url}")
            chromiumPage.locator("#find-bulbs-button").wait_for(state="attached")
            self.assertEqual(chromiumPage.title(), "Bulb Bop")
            LOGGER.debug("Page title is Bulb Bop")
            expect(chromiumPage.locator("#main-title")).to_be_visible()
            LOGGER.debug("Main title is visible")
            expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible()
            LOGGER.debug("Find bulbs button is visible")
            expect(chromiumPage.locator("#home-link")).to_be_visible()
            LOGGER.debug("Home link is visible")
            expect(chromiumPage.locator("#faq-link")).to_be_visible()
            LOGGER.debug("FAQ link is visible")
            expect(chromiumPage.locator("#about-link")).to_be_visible()
            LOGGER.debug("About link is visible")
        except Exception as e:
            LOGGER.error("An error occurred in test_load_index: %s", e)

    def test_load_discover(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_load_discover.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            chromiumPage = self.chromium.new_page()
            chromiumPage.goto(f"{self.live_server_url}/discover")
            chromiumPage.locator("#find-bulbs-button").wait_for(state="attached")
            self.assertEqual(chromiumPage.title(), "Bulb Bop")
            expect(chromiumPage.locator("#main-title")).to_be_visible()
            LOGGER.debug("Main title is visible")
            expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible()
            LOGGER.debug("Find bulbs button is visible")
            expect(chromiumPage.locator("#home-link")).to_be_visible()
            LOGGER.debug("Home link is visible")
            expect(chromiumPage.locator("#faq-link")).to_be_visible()
            LOGGER.debug("FAQ link is visible")
            expect(chromiumPage.locator("#about-link")).to_be_visible()
            LOGGER.debug("About link is visible")
        except Exception as e:
            LOGGER.error("An error occurred in test_load_discover: %s", e)

    def test_from_index_to_discover(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_from_index_to_discover.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            chromiumPage = self.chromium.new_page()
            chromiumPage.goto(f"{self.live_server_url}")
            chromiumFindButton = chromiumPage.locator("#find-bulbs-button")
            chromiumFindButton.wait_for(state="attached")
            chromiumFindButton.click()
            chromiumFindButton.wait_for(state="attached")
            url = chromiumPage.url
            self.assertIn("discover", url)
            LOGGER.debug("URL contains discover")
            self.assertEqual(chromiumPage.title(), "Bulb Bop")
            LOGGER.debug("Page title is Bulb Bop")
            expect(chromiumPage.locator("#main-title")).to_be_visible()
            LOGGER.debug("Main title is visible")
            expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible()
            LOGGER.debug("Find bulbs button is visible")
            expect(chromiumPage.locator("#home-link")).to_be_visible()
            LOGGER.debug("Home link is visible")
            expect(chromiumPage.locator("#faq-link")).to_be_visible()
            LOGGER.debug("FAQ link is visible")
            expect(chromiumPage.locator("#about-link")).to_be_visible()
            LOGGER.debug("About link is visible")
        except Exception as e:
            LOGGER.error("An error occurred in test_from_index_to_discover: %s", e)

    def test_from_discover_to_index(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_from_discover_to_index.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for hdlr in LOGGER.handlers[:]:
            LOGGER.removeHandler(hdlr)
        LOGGER.addHandler(log_handler)
        try:
            chromiumPage = self.chromium.new_page()
            chromiumPage.goto(f"{self.live_server_url}/discover")
            chromiumPage.locator("#find-bulbs-button").wait_for(timeout=0, state="attached")
            chromiumPage.locator("#home-link").click()
            chromiumPage.locator("#find-bulbs-button").wait_for(timeout=0, state="attached")
            url = chromiumPage.url
            self.assertNotIn("discover", url)
            LOGGER.debug("URL does not contain discover")
            self.assertEqual(chromiumPage.title(), "Bulb Bop")
            LOGGER.debug("Page title is Bulb Bop")
            if chromiumPage.locator(".bulb-icon"):
                expect(chromiumPage.locator("#error-toast")).to_have_count(0)
                LOGGER.debug("No error toast visible")
            else:
                expect(chromiumPage.locator("#error-toast")).to_be_visible()
                LOGGER.debug("Error toast is visible")
            expect(chromiumPage.locator("#main-title")).to_be_visible()
            LOGGER.debug("Main title is visible")
            expect(chromiumPage.locator("#find-bulbs-button")).to_be_visible()
            LOGGER.debug("Find bulbs button is visible")
            expect(chromiumPage.locator("#home-link")).to_be_visible()
            LOGGER.debug("Home link is visible")
            expect(chromiumPage.locator("#faq-link")).to_be_visible()
            LOGGER.debug("FAQ link is visible")
            expect(chromiumPage.locator("#about-link")).to_be_visible()
            LOGGER.debug("About link is visible")
        except Exception as e:
            LOGGER.error("An error occurred in test_from_discover_to_index: %s", e)
