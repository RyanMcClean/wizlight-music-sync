# pylint: disable = broad-exception-caught
"""Playwright tests to ensure that webpages load correctly, and that navigation works as expected"""

import os
import logging
from playwright.sync_api import sync_playwright, expect
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from test_helper import formatter

LOGGER = logging.getLogger(__name__)


class PlaywrightTests(StaticLiveServerTestCase):
    """Test class for testing using playwright"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        cls.playwright = sync_playwright().start()
        cls.browsers = []
        cls.browsers.append(cls.playwright.chromium.launch())
        cls.browsers.append(cls.playwright.firefox.launch())

    @classmethod
    def tearDownClass(cls):
        for browser in cls.browsers:
            browser.close()
        cls.playwright.stop()
        return super().tearDownClass()

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
        for browser in self.browsers:
            LOGGER.info("Running tests on: %s", browser.browser_type.name)
            page = browser.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_url("**", wait_until="domcontentloaded")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.close()
            LOGGER.debug("Page closed")

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
        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/discover")
            page.wait_for_url("**", wait_until="domcontentloaded")
            page.locator("#find-bulbs-button").wait_for(state="attached")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.close()
            LOGGER.debug("Page closed")

    def test_from_index_to_discover(self):
        """Test navigation from index page to discover page"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_from_index_to_discover.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)
        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}")
            LOGGER.debug("Using browser, %s Page URL is: %s", browser.browser_type.name, page.url)
            page.wait_for_url("**", wait_until="domcontentloaded")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            find_button = page.locator("#find-bulbs-button")
            find_button.click()
            LOGGER.debug(page.url)
            page.wait_for_url("**", wait_until="domcontentloaded")
            url = page.url
            self.assertIn("discover", url)
            LOGGER.debug("URL is: %s", url)
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.close()
            LOGGER.debug("Page closed")

    def test_from_discover_to_index(self):
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_from_discover_to_index.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)
        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/discover")
            page.wait_for_url("**", wait_until="domcontentloaded")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.locator("#home-link").click()
            page.wait_for_url("**", wait_until="domcontentloaded")
            self.assertNotIn("discover", page.url)
            LOGGER.debug("URL is: %s", page.url)
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.close()
            LOGGER.debug("Page closed")

    def test_load_faq(self):
        """Load FAQ page, ensure that telltale elements are visible"""
        # Set up logging for the test
        log_filename = f"test_logs/individual_test_logs/{__name__}/test_from_discover_to_index.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        log_handler = logging.FileHandler(log_filename, "w")
        log_handler.setFormatter(formatter)
        for handler in LOGGER.handlers[:]:
            LOGGER.removeHandler(handler)
        LOGGER.addHandler(log_handler)
        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/faq")
            page.wait_for_url("**", wait_until="domcontentloaded")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            faq_tests(page)
            LOGGER.debug("FAQ tests passed")


def faq_tests(page):
    expect(page.get_by_text("Frequently Asked Questions")).to_be_visible()
    LOGGER.debug("FAQ title is visible")
    expect(page.get_by_text("Technical Questions")).to_be_visible()
    LOGGER.debug("Technical Questions title is visible")
    expect(page.get_by_text("Troubleshooting")).to_be_visible()
    LOGGER.debug("Troubleshooting title is visible")


def navbar_tests(page):
    """Test navbar links, useful helper to reduce code duplication"""
    if page.locator(".navbar-toggler-icon").is_visible():
        page.locator(".navbar-toggler-icon").click()
    expect(page.locator("#home-link")).to_be_visible()
    LOGGER.debug("Home link is visible")
    expect(page.locator("#faq-link")).to_be_visible()
    LOGGER.debug("FAQ link is visible")
    expect(page.locator("#about-link")).to_be_visible()
    LOGGER.debug("About link is visible")
    expect(page.locator("#find-bulbs-button")).to_be_visible()
    LOGGER.debug("Find bulbs button is visible")
    expect(page.locator("#main-title")).to_be_visible()
    LOGGER.debug("Main title is visible")
