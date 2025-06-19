import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import (
    get_driver,
    LOGIN_URL,
    EMAIL,
    PASSWORD,
    EMAIL_INPUT,
    PASSWORD_INPUT,
    SUBMIT_BUTTON,
    ERROR_MESSAGE,
    DASHBOARD_TITLE,
    WAIT_TIME
)
import time

@pytest.fixture
def driver():
    """Fixture to create and close the WebDriver"""
    driver = get_driver()
    yield driver
    time.sleep(WAIT_TIME)  # Wait before closing
    driver.quit()

def test_login_success(driver):
    """Test successful login with valid credentials"""
    # Navigate to login page
    driver.get(LOGIN_URL)
    time.sleep(WAIT_TIME)  # Wait for page load
    
    # Wait for and fill in email
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, EMAIL_INPUT))
    )
    email_field.clear()
    time.sleep(WAIT_TIME)  # Wait before typing
    email_field.send_keys(EMAIL)
    time.sleep(WAIT_TIME)  # Wait after typing
    
    # Fill in password
    password_field = driver.find_element(By.CSS_SELECTOR, PASSWORD_INPUT)
    password_field.clear()
    time.sleep(WAIT_TIME)  # Wait before typing
    password_field.send_keys(PASSWORD)
    time.sleep(WAIT_TIME)  # Wait after typing
    
    # Click submit button
    submit_button = driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON)
    time.sleep(WAIT_TIME)  # Wait before clicking
    submit_button.click()
    
    # Wait for and verify dashboard title
    dashboard_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, DASHBOARD_TITLE))
    )
    time.sleep(WAIT_TIME)  # Wait to see the dashboard
    assert dashboard_title.text == "Dashboard"

def test_login_error(driver):
    """Test login with invalid credentials"""
    # Navigate to login page
    driver.get(LOGIN_URL)
    time.sleep(WAIT_TIME)  # Wait for page load
    
    # Wait for and fill in email with invalid email
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, EMAIL_INPUT))
    )
    email_field.clear()
    time.sleep(WAIT_TIME)  # Wait before typing
    email_field.send_keys("invalid@email.com")
    time.sleep(WAIT_TIME)  # Wait after typing
    
    # Fill in password with invalid password
    password_field = driver.find_element(By.CSS_SELECTOR, PASSWORD_INPUT)
    password_field.clear()
    time.sleep(WAIT_TIME)  # Wait before typing
    password_field.send_keys("wrongpassword")
    time.sleep(WAIT_TIME)  # Wait after typing
    
    # Click submit button
    submit_button = driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON)
    time.sleep(WAIT_TIME)  # Wait before clicking
    submit_button.click()
    
    # Wait for and verify error message
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ERROR_MESSAGE))
    )
    time.sleep(WAIT_TIME)  # Wait to see the error message
    assert error_message.text == "Invalid email or password"
