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
    CATEGORIES_LINK,
    NEW_CATEGORY_BUTTON,
    CATEGORY_NAME_INPUT,
    CATEGORIES_URL,
    NEW_CATEGORY_URL
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

def test_add_category(driver):
    """Test adding a new category"""
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
    
    # Find and click Categories link
    print("\nLooking for Categories link")
    categories_link = admin_nav.find_element(By.CSS_SELECTOR, CATEGORIES_LINK)
    assert categories_link.is_displayed(), "Categories link should be visible"
    print("Categories link found")
    categories_link.click()
    
    # Wait for categories page to load
    WebDriverWait(driver, 10).until(
        EC.url_to_be(CATEGORIES_URL)
    )
    print("Navigated to categories page")
    
    # Find and click New Category button
    print("\nLooking for New Category button")
    new_category_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, NEW_CATEGORY_BUTTON))
    )
    assert new_category_btn.is_displayed(), "New Category button should be visible"
    print("New Category button found")
    new_category_btn.click()
    
    # Wait for new category page to load
    WebDriverWait(driver, 10).until(
        EC.url_to_be(NEW_CATEGORY_URL)
    )
    print("Navigated to new category page")
    
    # Find the name input field
    print("\nLooking for name input field")
    name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CATEGORY_NAME_INPUT))
    )
    assert name_input.is_displayed(), "Name input field should be visible"
    print("Name input field found")
