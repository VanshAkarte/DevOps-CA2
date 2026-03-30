"""
conftest.py – Pytest fixtures for Student Feedback Form Selenium tests
DevOps CA2 Project
"""
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_MANAGER = True
except ImportError:
    USE_MANAGER = False


# Build absolute file:// URL to index.html
_root = Path(__file__).resolve().parent.parent
FORM_URL_STR = "file:///" + str(_root / "index.html").replace("\\", "/")


@pytest.fixture(scope="session")
def driver():
    """
    Session-scoped Chrome WebDriver — ONE browser for ALL tests (fast!).
    Browser opens visually so you can watch tests run.
    """
    options = Options()
    # NOTE: Browser opens visually (no headless).
    # For Jenkins/CI, uncomment: options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--allow-file-access-from-files")
    options.add_argument("--disable-web-security")
    options.add_argument("--window-size=1400,2000")
    options.add_argument("--start-maximized")

    if USE_MANAGER:
        service = Service(ChromeDriverManager().install())
    else:
        service = Service()

    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(3)
    yield drv
    drv.quit()


@pytest.fixture(autouse=True)
def load_page(driver):
    """Before EVERY test: reload the form and wait until it's fully rendered."""
    driver.get(FORM_URL_STR)
    # Wait until the form element is actually visible (CSS loaded, DOM ready)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "feedbackForm"))
    )
