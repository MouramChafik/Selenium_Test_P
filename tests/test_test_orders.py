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
    WAIT_TIME,
    DASHBOARD_URL,
    ADMIN_NAVIGATION,
    ORDERS_LINK,
    ORDERS_TITLE,
    ORDERS_URL
)
import time

@pytest.fixture
def driver():
    """Fixture to create and close the WebDriver"""
    driver = get_driver()
    yield driver
    time.sleep(WAIT_TIME)  # Wait before closing
    driver.quit()

def login(driver):
    """Helper function to login"""
    driver.get(LOGIN_URL)
    time.sleep(WAIT_TIME)
    
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, EMAIL_INPUT))
    )
    email_field.clear()
    time.sleep(WAIT_TIME)
    email_field.send_keys(EMAIL)
    
    password_field = driver.find_element(By.CSS_SELECTOR, PASSWORD_INPUT)
    password_field.clear()
    time.sleep(WAIT_TIME)
    password_field.send_keys(PASSWORD)
    
    submit_button = driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON)
    time.sleep(WAIT_TIME)
    submit_button.click()
    
    # Wait for dashboard to load
    WebDriverWait(driver, 10).until(
        EC.url_to_be(DASHBOARD_URL)
    )

def test_navigate_to_orders(driver):
    """Test navigation to orders page"""
    # Login first
    login(driver)
    print("\nCurrent URL:", driver.current_url)
    
    # Verify admin navigation is present
    print("\nLooking for admin navigation")
    admin_nav = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ADMIN_NAVIGATION))
    )
    assert admin_nav.is_displayed(), "Admin navigation should be visible"
    print("Admin navigation found")
    
    # Find and click Orders link
    print("\nLooking for Orders link")
    orders_link = admin_nav.find_element(By.CSS_SELECTOR, ORDERS_LINK)
    assert orders_link.is_displayed(), "Orders link should be visible"
    print("Orders link found")
    orders_link.click()
    
    # Wait for orders page to load
    WebDriverWait(driver, 10).until(
        EC.url_to_be(ORDERS_URL)
    )
    print("Navigated to orders page")
    
    # Verify orders page title
    print("\nVerifying orders page title")
    orders_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ORDERS_TITLE))
    )
    assert orders_title.is_displayed(), "Orders title should be visible"
    assert orders_title.text == "Orders", "Page title should be 'Orders'"
    print("Orders title verified")
