"""
conftest.py – Pytest fixtures for Student Feedback Form Selenium tests
DevOps CA2 Project
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_MANAGER = True
except ImportError:
    USE_MANAGER = False


# Absolute path to index.html — works on Windows & Linux
FORM_URL = "file:///" + os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "index.html")
).replace("\\", "/")


@pytest.fixture(scope="function")
def driver():
    """
    Provides a Chrome WebDriver instance.
    Opens the feedback form before each test and quits after.
    """
    options = Options()
    options.add_argument("--headless")          # Run without GUI (CI-friendly)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")

    if USE_MANAGER:
        service = Service(ChromeDriverManager().install())
    else:
        # Fallback: expects chromedriver on PATH
        service = Service()

    drv = webdriver.Chrome(service=service, options=options)
    drv.get(FORM_URL)
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def form_url():
    """Returns the file URL to index.html."""
    return "file:///" + os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "index.html")
    ).replace("\\", "/")
