# pylint: disable = broad-exception-caught
"""Playwright tests to ensure that webpages load correctly, and that navigation works as expected"""

import os
import logging
from playwright.sync_api import sync_playwright, expect
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import pytest
from test_helper import formatter

LOGGER = logging.getLogger(__name__)


class PlaywrightTests(StaticLiveServerTestCase):
    """Test class for testing using playwright"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        cls.playwright = sync_playwright().start()
        cls.browser = []
        cls.browser.append(cls.playwright.chromium.launch())
        cls.browser.append(cls.playwright.firefox.launch())
        cls.browser.append(cls.playwright.webkit.launch())

    @classmethod
    def tearDownClass(cls):
        for browser in cls.browser:
            browser.close()
        cls.playwright.stop()
        return super().tearDownClass()

    @pytest.mark.django_db
    def test_load_index(self):
        """Load index page, and check that telltale elements are visible"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_load_index.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)
        for browser in self.browser:
            LOGGER.info("Running tests on: %s", browser.browser_type.name)
            page = browser.new_page()
            page.goto(f"{self.live_server_url}")
            page.locator("#find-bulbs-button").wait_for(state="attached")
            if page.locator(".navbar-toggler-icon").is_visible():
                page.locator(".navbar-toggler-icon").click()
            self.assertEqual(page.title(), "Bulb Bop")
            LOGGER.debug("Page title is Bulb Bop")
            expect(page.locator("#main-title")).to_be_visible()
            LOGGER.debug("Main title is visible")
            expect(page.locator("#find-bulbs-button")).to_be_visible()
            LOGGER.debug("Find bulbs button is visible")
            expect(page.locator("#home-link")).to_be_visible()
            LOGGER.debug("Home link is visible")
            expect(page.locator("#faq-link")).to_be_visible()
            LOGGER.debug("FAQ link is visible")
            expect(page.locator("#about-link")).to_be_visible()
            LOGGER.debug("About link is visible")

    @pytest.mark.django_db
    def test_load_discover(self):
        """Load discover page, and check that all telltale elements are visible"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_load_discover.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)
        for browser in self.browser:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/discover")
            page.locator("#find-bulbs-button").wait_for(state="attached")
            if page.locator(".navbar-toggler-icon").is_visible():
                page.locator(".navbar-toggler-icon").click()
            self.assertEqual(page.title(), "Bulb Bop")
            expect(page.locator("#main-title")).to_be_visible()
            LOGGER.debug("Main title is visible")
            expect(page.locator("#find-bulbs-button")).to_be_visible()
            LOGGER.debug("Find bulbs button is visible")
            expect(page.locator("#home-link")).to_be_visible()
            LOGGER.debug("Home link is visible")
            expect(page.locator("#faq-link")).to_be_visible()
            LOGGER.debug("FAQ link is visible")
            expect(page.locator("#about-link")).to_be_visible()
            LOGGER.debug("About link is visible")

    @pytest.mark.django_db
    def test_from_index_to_discover(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_from_index_to_discover.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)
        for browser in self.browser:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}")
            find_button = page.locator("#find-bulbs-button")
            find_button.wait_for(state="attached")
            if page.locator(".navbar-toggler-icon").is_visible():
                page.locator(".navbar-toggler-icon").click()
            find_button.click()
            find_button.wait_for(state="attached")
            url = page.url
            self.assertIn("discover", url)
            if page.locator(".navbar-toggler-icon").is_visible():
                page.locator(".navbar-toggler-icon").click()
            LOGGER.debug("URL is: %s", url)
            self.assertEqual(page.title(), "Bulb Bop")
            LOGGER.debug("Page title is Bulb Bop")
            expect(page.locator("#main-title")).to_be_visible()
            LOGGER.debug("Main title is visible")
            expect(page.locator("#find-bulbs-button")).to_be_visible()
            LOGGER.debug("Find bulbs button is visible")
            expect(page.locator("#home-link")).to_be_visible()
            LOGGER.debug("Home link is visible")
            expect(page.locator("#faq-link")).to_be_visible()
            LOGGER.debug("FAQ link is visible")
            expect(page.locator("#about-link")).to_be_visible()
            LOGGER.debug("About link is visible")

    @pytest.mark.django_db
    def test_from_discover_to_index(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_from_discover_to_index.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)
        for browser in self.browser:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/discover")
            page.locator("#find-bulbs-button").wait_for(state="attached")
            if page.locator(".navbar-toggler-icon").is_visible():
                page.locator(".navbar-toggler-icon").click()
            page.locator("#home-link").click()
            page.locator("#find-bulbs-button").wait_for(state="attached")
            if page.locator(".navbar-toggler-icon").is_visible():
                page.locator(".navbar-toggler-icon").click()
            url = page.url
            self.assertNotIn("discover", url)
            LOGGER.debug("URL does not contain discover")
            self.assertEqual(page.title(), "Bulb Bop")
            LOGGER.debug("Page title is: %s", page.title())
            expect(page.locator("#main-title")).to_be_visible()
            LOGGER.debug("Main title is visible")
            expect(page.locator("#find-bulbs-button")).to_be_visible()
            LOGGER.debug("Find bulbs button is visible")
            expect(page.locator("#home-link")).to_be_visible()
            LOGGER.debug("Home link is visible")
            expect(page.locator("#faq-link")).to_be_visible()
            LOGGER.debug("FAQ link is visible")
            expect(page.locator("#about-link")).to_be_visible()
            LOGGER.debug("About link is visible")
