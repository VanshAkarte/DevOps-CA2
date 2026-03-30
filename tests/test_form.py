"""
test_form.py – Selenium Test Cases for Student Feedback Registration Form
DevOps CA2 Project

Test Cases:
  TC1 : Form page opens successfully
  TC2 : Valid data submission shows success banner
  TC3 : Blank form triggers all required-field error messages
  TC4 : Invalid email format shows email error message
  TC5 : Invalid mobile number shows mobile error message
  TC6 : Department dropdown selection works correctly
  TC7 : Submit and Reset buttons function correctly
"""

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# ─── Helpers ────────────────────────────────────────────────────────────────

def js_click(driver, element_id):
    """Click via JavaScript — bypasses ElementClickInterceptedException."""
    driver.execute_script(
        "var el = document.getElementById(arguments[0]);"
        "el.scrollIntoView({block:'center'});"
        "el.click();",
        element_id
    )

def click_submit(driver):
    js_click(driver, "submitBtn")
    time.sleep(0.2)

def click_reset(driver):
    js_click(driver, "resetBtn")
    time.sleep(0.2)

def fill_valid_form(driver):
    """Fill all form fields with valid test data."""
    driver.find_element(By.ID, "studentName").clear()
    driver.find_element(By.ID, "studentName").send_keys("Vansh")
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("vansh@college.edu")
    driver.find_element(By.ID, "mobile").clear()
    driver.find_element(By.ID, "mobile").send_keys("9876543210")
    Select(driver.find_element(By.ID, "department")).select_by_value("CSE")
    driver.execute_script("document.getElementById('genderMale').click();")
    driver.find_element(By.ID, "comments").clear()
    driver.find_element(By.ID, "comments").send_keys(
        "The teaching quality this semester has been outstanding "
        "and I thoroughly enjoyed every single class session."
    )

def get_error_text(driver, error_id):
    return driver.find_element(By.ID, error_id).text.strip()


# ─── TC1: Page Loads ─────────────────────────────────────────────────────────

class TestTC1_PageLoads:
    """TC1 – Verify the form page opens and all key elements are present."""

    def test_page_title(self, driver):
        assert "Student Feedback" in driver.title

    def test_form_visible(self, driver):
        form = driver.find_element(By.ID, "feedbackForm")
        assert form.is_displayed()

    def test_all_fields_present(self, driver):
        for fid in ["studentName", "email", "mobile", "department", "comments"]:
            assert driver.find_element(By.ID, fid).is_displayed(), f"'{fid}' not visible"

    def test_gender_radios_present(self, driver):
        assert len(driver.find_elements(By.NAME, "gender")) == 4

    def test_buttons_present(self, driver):
        assert driver.find_element(By.ID, "submitBtn").is_enabled()
        assert driver.find_element(By.ID, "resetBtn").is_enabled()


# ─── TC2: Valid Submission ───────────────────────────────────────────────────

class TestTC2_ValidSubmission:
    """TC2 – Fill valid data and verify success banner."""

    def test_success_banner_appears(self, driver):
        fill_valid_form(driver)
        click_submit(driver)
        banner = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "successBanner"))
        )
        assert banner.is_displayed()

    def test_success_message_has_name(self, driver):
        fill_valid_form(driver)
        click_submit(driver)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "successBanner")))
        assert "Vansh" in driver.find_element(By.ID, "successMessage").text

    def test_no_errors_on_valid_submit(self, driver):
        fill_valid_form(driver)
        click_submit(driver)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "successBanner")))
        for span in driver.find_elements(By.CLASS_NAME, "error-msg"):
            assert span.text.strip() == ""


# ─── TC3: Blank Form ─────────────────────────────────────────────────────────

class TestTC3_BlankFormErrors:
    """TC3 – Submit empty form and check all error messages."""

    def test_all_errors_appear_on_blank_submit(self, driver):
        click_submit(driver)
        assert get_error_text(driver, "nameError") != "", "Name error missing"
        assert get_error_text(driver, "emailError") != "", "Email error missing"
        assert get_error_text(driver, "mobileError") != "", "Mobile error missing"
        assert get_error_text(driver, "deptError") != "", "Dept error missing"
        assert get_error_text(driver, "genderError") != "", "Gender error missing"
        assert get_error_text(driver, "commentsError") != "", "Comments error missing"

    def test_no_success_on_blank_submit(self, driver):
        click_submit(driver)
        assert not driver.find_element(By.ID, "successBanner").is_displayed()


# ─── TC4: Invalid Email ──────────────────────────────────────────────────────

class TestTC4_InvalidEmail:
    """TC4 – Invalid email formats should show email error."""

    @pytest.mark.parametrize("bad_email", [
        "notanemail", "missing@domain", "@nodomain.com"
    ])
    def test_invalid_email_shows_error(self, driver, bad_email):
        driver.find_element(By.ID, "studentName").send_keys("Test")
        driver.find_element(By.ID, "email").send_keys(bad_email)
        driver.find_element(By.ID, "mobile").send_keys("9876543210")
        Select(driver.find_element(By.ID, "department")).select_by_value("CSE")
        driver.execute_script("document.getElementById('genderMale').click();")
        driver.find_element(By.ID, "comments").send_keys(
            "This is a test feedback comment with enough words in it here."
        )
        click_submit(driver)
        assert get_error_text(driver, "emailError") != "", f"No error for '{bad_email}'"

    def test_valid_email_no_error(self, driver):
        fill_valid_form(driver)
        click_submit(driver)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "successBanner")))
        assert get_error_text(driver, "emailError") == ""


# ─── TC5: Invalid Mobile ─────────────────────────────────────────────────────

class TestTC5_InvalidMobile:
    """TC5 – Invalid mobile numbers should show mobile error."""

    @pytest.mark.parametrize("bad_mobile", [
        "12345", "abcdefghij", "98765abcde"
    ])
    def test_invalid_mobile_shows_error(self, driver, bad_mobile):
        driver.find_element(By.ID, "studentName").send_keys("Test")
        driver.find_element(By.ID, "email").send_keys("test@domain.com")
        driver.find_element(By.ID, "mobile").send_keys(bad_mobile)
        Select(driver.find_element(By.ID, "department")).select_by_value("CSE")
        driver.execute_script("document.getElementById('genderMale').click();")
        driver.find_element(By.ID, "comments").send_keys(
            "This is a test feedback comment with enough words in it here."
        )
        click_submit(driver)
        assert get_error_text(driver, "mobileError") != "", f"No error for '{bad_mobile}'"

    def test_valid_mobile_no_error(self, driver):
        fill_valid_form(driver)
        click_submit(driver)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "successBanner")))
        assert get_error_text(driver, "mobileError") == ""


# ─── TC6: Dropdown Selection ─────────────────────────────────────────────────

class TestTC6_DropdownSelection:
    """TC6 – Department dropdown works correctly."""

    @pytest.mark.parametrize("value,label", [
        ("CSE", "Computer Science"), ("ECE", "Electronics"), ("IT", "Information Technology")
    ])
    def test_department_selectable(self, driver, value, label):
        sel = Select(driver.find_element(By.ID, "department"))
        sel.select_by_value(value)
        assert sel.first_selected_option.get_attribute("value") == value
        assert label in sel.first_selected_option.text

    def test_default_is_empty(self, driver):
        sel = Select(driver.find_element(By.ID, "department"))
        assert sel.first_selected_option.get_attribute("value") == ""

    def test_dept_error_without_selection(self, driver):
        driver.find_element(By.ID, "studentName").send_keys("Test")
        driver.find_element(By.ID, "email").send_keys("test@domain.com")
        driver.find_element(By.ID, "mobile").send_keys("9876543210")
        driver.execute_script("document.getElementById('genderMale').click();")
        driver.find_element(By.ID, "comments").send_keys(
            "This is a test feedback comment with enough words in it here."
        )
        click_submit(driver)
        assert get_error_text(driver, "deptError") != ""


# ─── TC7: Submit and Reset Buttons ───────────────────────────────────────────

class TestTC7_Buttons:
    """TC7 – Submit triggers validation; Reset clears all fields."""

    def test_buttons_enabled(self, driver):
        assert driver.find_element(By.ID, "submitBtn").is_enabled()
        assert driver.find_element(By.ID, "resetBtn").is_enabled()

    def test_reset_clears_all_fields(self, driver):
        driver.find_element(By.ID, "studentName").send_keys("Some Student")
        driver.find_element(By.ID, "email").send_keys("some@email.com")
        driver.find_element(By.ID, "mobile").send_keys("1234567890")
        driver.find_element(By.ID, "comments").send_keys("Some comments here.")
        Select(driver.find_element(By.ID, "department")).select_by_value("CSE")
        driver.execute_script("document.getElementById('genderMale').click();")
        click_reset(driver)
        assert driver.find_element(By.ID, "studentName").get_attribute("value") == ""
        assert driver.find_element(By.ID, "email").get_attribute("value") == ""
        assert driver.find_element(By.ID, "mobile").get_attribute("value") == ""
        assert driver.find_element(By.ID, "comments").get_attribute("value") == ""
        assert Select(driver.find_element(By.ID, "department")).first_selected_option.get_attribute("value") == ""
        for r in driver.find_elements(By.NAME, "gender"):
            assert not r.is_selected()

    def test_submit_valid_shows_success(self, driver):
        fill_valid_form(driver)
        click_submit(driver)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "successBanner")))
        for span in driver.find_elements(By.CLASS_NAME, "error-msg"):
            assert span.text.strip() == ""
