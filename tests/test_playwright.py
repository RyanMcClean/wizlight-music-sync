# pylint: disable = broad-exception-caught
"""Playwright tests to ensure that webpages load correctly, and that navigation works as expected"""

import os
import logging
import inspect
from playwright.sync_api import sync_playwright, expect
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from test_helper import setup_logger

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
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
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
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/discover")
            LOGGER.debug("Using browser, %s Page URL is: %s", browser.browser_type.name, page.url)
            page.wait_for_url("**", wait_until="domcontentloaded")
            page.locator("#find-bulbs-button").wait_for(state="attached")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.close()
            LOGGER.debug("Page closed")

    def test_from_index_to_discover(self):
        """Test navigation from index page to discover page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)
        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}")
            LOGGER.debug("Using browser, %s Page URL is: %s", browser.browser_type.name, page.url)
            page.wait_for_url("**", wait_until="domcontentloaded")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.locator("#find-bulbs-button").click()
            LOGGER.debug(page.url)
            page.wait_for_url("**", wait_until="domcontentloaded")
            self.assertIn("discover", page.url)
            LOGGER.debug("URL is: %s", page.url)
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.close()
            LOGGER.debug("Page closed")

    def test_from_discover_to_index(self):
        """Test navigation from discover page to index page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/discover")
            LOGGER.debug("Using browser, %s Page URL is: %s", browser.browser_type.name, page.url)
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
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/faq")
            LOGGER.debug("Using browser, %s Page URL is: %s", browser.browser_type.name, page.url)
            page.wait_for_url("**", wait_until="domcontentloaded")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            faq_tests(self, page)
            LOGGER.debug("FAQ tests passed")

    def test_from_index_to_faq(self):
        """Test navigation from index page to faq page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}")
            LOGGER.debug("Using browser, %s Page URL is: %s", browser.browser_type.name, page.url)
            page.wait_for_url("**", wait_until="domcontentloaded")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.locator("#faq-link").click()
            page.wait_for_url("**", wait_until="domcontentloaded")
            self.assertIn("faq", page.url)
            LOGGER.debug("URL is: %s", page.url)
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            faq_tests(self, page)
            LOGGER.debug("About tests passed")
            page.close()
            LOGGER.debug("Page closed")

    def test_from_faq_to_index(self):
        """Test navigation from faq page to index page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/faq")
            LOGGER.debug("Using browser, %s Page URL is: %s", browser.browser_type.name, page.url)
            page.wait_for_url("**", wait_until="domcontentloaded")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            faq_tests(self, page)
            LOGGER.debug("About tests passed")
            page.locator("#home-link").click()
            page.wait_for_url("**", wait_until="domcontentloaded")
            self.assertNotIn("faq", page.url)
            LOGGER.debug("URL is: %s", page.url)
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.close()
            LOGGER.debug("Page closed")

    def test_load_about(self):
        """Load about page, ensure that the telltale elements are visible"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/about")
            LOGGER.debug("Using browser, %s Page URL is: %s", browser.browser_type.name, page.url)
            page.wait_for_url("**", wait_until="domcontentloaded")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            about_tests(self, page)
            LOGGER.debug("About tests passed")

    def test_from_index_to_about(self):
        """Test navigation from index page to about page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}")
            LOGGER.debug("Using browser, %s Page URL is: %s", browser.browser_type.name, page.url)
            page.wait_for_url("**", wait_until="domcontentloaded")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.locator("#about-link").click()
            page.wait_for_url("**", wait_until="domcontentloaded")
            self.assertIn("about", page.url)
            LOGGER.debug("URL is: %s", page.url)
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            about_tests(self, page)
            LOGGER.debug("About tests passed")
            page.close()
            LOGGER.debug("Page closed")

    def test_from_about_to_index(self):
        """Test navigation from about page to index page"""
        setup_logger(__name__, inspect.currentframe().f_code.co_name, LOGGER)

        for browser in self.browsers:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/about")
            LOGGER.debug("Using browser, %s Page URL is: %s", browser.browser_type.name, page.url)
            page.wait_for_url("**", wait_until="domcontentloaded")
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            about_tests(self, page)
            LOGGER.debug("About tests passed")
            page.locator("#home-link").click()
            page.wait_for_url("**", wait_until="domcontentloaded")
            self.assertNotIn("about", page.url)
            LOGGER.debug("URL is: %s", page.url)
            navbar_tests(page)
            LOGGER.debug("Navbar tests passed")
            page.close()
            LOGGER.debug("Page closed")


def about_tests(self, page):
    """Test about page, useful helper to reduce code duplication"""
    self.assertIn("about", page.url)
    LOGGER.debug("URL is: %s", page.url)
    expect(page.locator("h1").get_by_text("About")).to_be_visible()
    LOGGER.debug("About title is visible")
    expect(page.get_by_text("The Project")).to_be_visible()
    LOGGER.debug("The Project subtitle is visible")
    expect(page.get_by_text("The Author")).to_be_visible()
    LOGGER.debug("The Author subtitle is visible")


def faq_tests(self, page):
    """Test FAQ page, useful helper to reduce code duplication"""
    self.assertIn("faq", page.url)
    LOGGER.debug("URL is: %s", page.url)
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
