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

def wait_for(driver, by, locator, timeout=10):
    """Wait until an element is present and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, locator))
    )


def fill_valid_form(driver):
    """Fill all form fields with valid test data."""
    driver.find_element(By.ID, "studentName").clear()
    driver.find_element(By.ID, "studentName").send_keys("Jeevan Kumar")

    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("jeevan.kumar@college.edu")

    driver.find_element(By.ID, "mobile").clear()
    driver.find_element(By.ID, "mobile").send_keys("9876543210")

    select = Select(driver.find_element(By.ID, "department"))
    select.select_by_value("CSE")

    driver.find_element(By.ID, "genderMale").click()

    driver.find_element(By.ID, "comments").clear()
    driver.find_element(By.ID, "comments").send_keys(
        "The teaching quality this semester has been outstanding "
        "and I thoroughly enjoyed every class session."
    )


# ─── TC1: Page Loads ─────────────────────────────────────────────────────────

class TestTC1_PageLoads:
    """TC1 – Verify the form page opens and key elements are present."""

    def test_page_title_contains_student_feedback(self, driver):
        assert "Student Feedback" in driver.title, (
            f"Expected 'Student Feedback' in title but got: '{driver.title}'"
        )

    def test_form_element_present(self, driver):
        form = driver.find_element(By.ID, "feedbackForm")
        assert form is not None and form.is_displayed()

    def test_all_required_fields_present(self, driver):
        field_ids = ["studentName", "email", "mobile", "department", "comments"]
        for fid in field_ids:
            el = driver.find_element(By.ID, fid)
            assert el.is_displayed(), f"Field '{fid}' is not visible on the page."

    def test_gender_radio_buttons_present(self, driver):
        radios = driver.find_elements(By.NAME, "gender")
        assert len(radios) == 4, f"Expected 4 gender options, found {len(radios)}"

    def test_submit_and_reset_buttons_present(self, driver):
        submit_btn = driver.find_element(By.ID, "submitBtn")
        reset_btn  = driver.find_element(By.ID, "resetBtn")
        assert submit_btn.is_displayed() and reset_btn.is_displayed()


# ─── TC2: Valid Submission ───────────────────────────────────────────────────

class TestTC2_ValidSubmission:
    """TC2 – Fill all fields with valid data and verify success banner appears."""

    def test_success_banner_appears_after_valid_submit(self, driver):
        fill_valid_form(driver)
        driver.find_element(By.ID, "submitBtn").click()

        banner = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "successBanner"))
        )
        assert banner.is_displayed(), "Success banner did not appear after valid submission."

    def test_success_message_contains_student_name(self, driver):
        fill_valid_form(driver)
        driver.find_element(By.ID, "submitBtn").click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "successBanner"))
        )
        msg = driver.find_element(By.ID, "successMessage").text
        assert "Jeevan Kumar" in msg, f"Success message did not mention student name. Got: '{msg}'"

    def test_no_error_messages_on_valid_submission(self, driver):
        fill_valid_form(driver)
        driver.find_element(By.ID, "submitBtn").click()

        # All error spans should be empty
        error_spans = driver.find_elements(By.CLASS_NAME, "error-msg")
        for span in error_spans:
            assert span.text.strip() == "", (
                f"Unexpected error message found: '{span.text}'"
            )


# ─── TC3: Blank Form ─────────────────────────────────────────────────────────

class TestTC3_BlankFormErrors:
    """TC3 – Submit blank form and verify required-field error messages appear."""

    def test_name_error_on_blank_submit(self, driver):
        driver.find_element(By.ID, "submitBtn").click()
        err = wait_for(driver, By.ID, "nameError")
        assert err.text.strip() != "", "Name error message should be displayed."

    def test_email_error_on_blank_submit(self, driver):
        driver.find_element(By.ID, "submitBtn").click()
        err = driver.find_element(By.ID, "emailError")
        assert err.text.strip() != "", "Email error message should be displayed."

    def test_mobile_error_on_blank_submit(self, driver):
        driver.find_element(By.ID, "submitBtn").click()
        err = driver.find_element(By.ID, "mobileError")
        assert err.text.strip() != "", "Mobile error message should be displayed."

    def test_dept_error_on_blank_submit(self, driver):
        driver.find_element(By.ID, "submitBtn").click()
        err = driver.find_element(By.ID, "deptError")
        assert err.text.strip() != "", "Department error message should be displayed."

    def test_gender_error_on_blank_submit(self, driver):
        driver.find_element(By.ID, "submitBtn").click()
        err = driver.find_element(By.ID, "genderError")
        assert err.text.strip() != "", "Gender error message should be displayed."

    def test_comments_error_on_blank_submit(self, driver):
        driver.find_element(By.ID, "submitBtn").click()
        err = driver.find_element(By.ID, "commentsError")
        assert err.text.strip() != "", "Comments error message should be displayed."

    def test_success_banner_not_visible_on_blank_submit(self, driver):
        driver.find_element(By.ID, "submitBtn").click()
        banner = driver.find_element(By.ID, "successBanner")
        assert not banner.is_displayed(), "Success banner must NOT appear on blank form submission."


# ─── TC4: Invalid Email ──────────────────────────────────────────────────────

class TestTC4_InvalidEmail:
    """TC4 – Invalid email formats should show the email error message."""

    INVALID_EMAILS = [
        "notanemail",
        "missing@domain",
        "@nodomain.com",
        "spaces in@email.com",
        "double@@at.com",
    ]

    @pytest.mark.parametrize("bad_email", INVALID_EMAILS)
    def test_invalid_email_shows_error(self, driver, bad_email):
        # Fill name & mobile to isolate email-only error
        driver.find_element(By.ID, "studentName").send_keys("Test User")
        driver.find_element(By.ID, "email").send_keys(bad_email)
        driver.find_element(By.ID, "mobile").send_keys("9876543210")
        Select(driver.find_element(By.ID, "department")).select_by_value("CSE")
        driver.find_element(By.ID, "genderMale").click()
        driver.find_element(By.ID, "comments").send_keys(
            "This is a test feedback comment with enough words here."
        )
        driver.find_element(By.ID, "submitBtn").click()

        err = driver.find_element(By.ID, "emailError")
        assert err.text.strip() != "", (
            f"Expected email error for '{bad_email}' but no error was shown."
        )

    def test_valid_email_clears_error(self, driver):
        fill_valid_form(driver)
        driver.find_element(By.ID, "submitBtn").click()
        err = driver.find_element(By.ID, "emailError")
        assert err.text.strip() == "", "Email error should not appear for a valid email."


# ─── TC5: Invalid Mobile ─────────────────────────────────────────────────────

class TestTC5_InvalidMobile:
    """TC5 – Invalid mobile numbers should show the mobile error message."""

    INVALID_MOBILES = [
        "12345",          # Too short
        "12345678901",    # Too long
        "abcdefghij",     # Letters
        "98765 43210",    # Contains space
        "9876-543210",    # Contains dash
    ]

    @pytest.mark.parametrize("bad_mobile", INVALID_MOBILES)
    def test_invalid_mobile_shows_error(self, driver, bad_mobile):
        driver.find_element(By.ID, "studentName").send_keys("Test User")
        driver.find_element(By.ID, "email").send_keys("test@domain.com")
        driver.find_element(By.ID, "mobile").send_keys(bad_mobile)
        Select(driver.find_element(By.ID, "department")).select_by_value("CSE")
        driver.find_element(By.ID, "genderMale").click()
        driver.find_element(By.ID, "comments").send_keys(
            "This is a test feedback comment with enough words here."
        )
        driver.find_element(By.ID, "submitBtn").click()

        err = driver.find_element(By.ID, "mobileError")
        assert err.text.strip() != "", (
            f"Expected mobile error for '{bad_mobile}' but no error was shown."
        )

    def test_valid_mobile_no_error(self, driver):
        fill_valid_form(driver)
        driver.find_element(By.ID, "submitBtn").click()
        err = driver.find_element(By.ID, "mobileError")
        assert err.text.strip() == "", "Mobile error should not appear for a valid 10-digit number."


# ─── TC6: Dropdown Selection ─────────────────────────────────────────────────

class TestTC6_DropdownSelection:
    """TC6 – Verify department dropdown selects each option correctly."""

    DEPARTMENTS = [
        ("CSE",  "Computer Science Engineering"),
        ("ECE",  "Electronics"),
        ("ME",   "Mechanical"),
        ("CE",   "Civil"),
        ("EEE",  "Electrical"),
        ("IT",   "Information Technology"),
        ("MBA",  "Master of Business"),
    ]

    @pytest.mark.parametrize("value,label_fragment", DEPARTMENTS)
    def test_department_option_selectable(self, driver, value, label_fragment):
        select_el = Select(driver.find_element(By.ID, "department"))
        select_el.select_by_value(value)
        selected = select_el.first_selected_option
        assert selected.get_attribute("value") == value, (
            f"Expected department '{value}' to be selected."
        )
        assert label_fragment in selected.text, (
            f"Option text '{selected.text}' does not contain '{label_fragment}'"
        )

    def test_default_option_is_empty(self, driver):
        """Verify the placeholder option is selected by default."""
        select_el = Select(driver.find_element(By.ID, "department"))
        assert select_el.first_selected_option.get_attribute("value") == "", (
            "Default department selection should have an empty value."
        )

    def test_dropdown_error_without_selection(self, driver):
        """Verify that submitting without dept selection shows an error."""
        driver.find_element(By.ID, "studentName").send_keys("Test User")
        driver.find_element(By.ID, "email").send_keys("test@domain.com")
        driver.find_element(By.ID, "mobile").send_keys("9876543210")
        # Leave department unselected
        driver.find_element(By.ID, "genderMale").click()
        driver.find_element(By.ID, "comments").send_keys(
            "This is a test feedback comment with enough words here."
        )
        driver.find_element(By.ID, "submitBtn").click()

        err = driver.find_element(By.ID, "deptError")
        assert err.text.strip() != "", "Dept error should appear when no department is selected."


# ─── TC7: Submit and Reset Buttons ───────────────────────────────────────────

class TestTC7_Buttons:
    """TC7 – Verify Submit triggers validation and Reset clears form."""

    def test_submit_button_is_clickable(self, driver):
        btn = driver.find_element(By.ID, "submitBtn")
        assert btn.is_enabled() and btn.is_displayed(), "Submit button must be visible and enabled."

    def test_reset_button_is_clickable(self, driver):
        btn = driver.find_element(By.ID, "resetBtn")
        assert btn.is_enabled() and btn.is_displayed(), "Reset button must be visible and enabled."

    def test_reset_clears_text_fields(self, driver):
        driver.find_element(By.ID, "studentName").send_keys("Some Student")
        driver.find_element(By.ID, "email").send_keys("some@email.com")
        driver.find_element(By.ID, "mobile").send_keys("1234567890")
        driver.find_element(By.ID, "comments").send_keys("Some comments here for testing.")

        driver.find_element(By.ID, "resetBtn").click()

        assert driver.find_element(By.ID, "studentName").get_attribute("value") == "", \
            "Student Name should be cleared after Reset."
        assert driver.find_element(By.ID, "email").get_attribute("value") == "", \
            "Email should be cleared after Reset."
        assert driver.find_element(By.ID, "mobile").get_attribute("value") == "", \
            "Mobile should be cleared after Reset."
        assert driver.find_element(By.ID, "comments").get_attribute("value") == "", \
            "Comments should be cleared after Reset."

    def test_reset_clears_dropdown(self, driver):
        Select(driver.find_element(By.ID, "department")).select_by_value("CSE")
        driver.find_element(By.ID, "resetBtn").click()
        select_el = Select(driver.find_element(By.ID, "department"))
        assert select_el.first_selected_option.get_attribute("value") == "", \
            "Department dropdown should reset to the placeholder after Reset."

    def test_reset_clears_gender_selection(self, driver):
        driver.find_element(By.ID, "genderMale").click()
        driver.find_element(By.ID, "resetBtn").click()
        radios = driver.find_elements(By.NAME, "gender")
        for radio in radios:
            assert not radio.is_selected(), "All gender radios should be unchecked after Reset."

    def test_submit_with_valid_data_shows_no_errors(self, driver):
        fill_valid_form(driver)
        driver.find_element(By.ID, "submitBtn").click()
        error_spans = driver.find_elements(By.CLASS_NAME, "error-msg")
        for span in error_spans:
            assert span.text.strip() == "", \
                f"Unexpected error after valid submission: '{span.text}'"
