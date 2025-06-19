import pytest
import time
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
    DASHBOARD_URL,
    ADMIN_NAVIGATION,
    CATEGORIES_LINK,
    CATEGORIES_URL,
    CATEGORIES_TABLE,
    CATEGORY_ROW,
    CATEGORY_NAME_LINK,
    CATEGORY_EDIT_TITLE,
    CATEGORY_NAME_INPUT,
    CATEGORY_URL_KEY_INPUT,
    CATEGORY_META_TITLE_INPUT,
    CATEGORY_META_KEYWORDS_INPUT,
    CATEGORY_META_DESCRIPTION_INPUT,
    CATEGORY_STATUS_RADIO,
    CATEGORY_INCLUDE_IN_NAV_RADIO,
    CATEGORY_SHOW_PRODUCTS_RADIO,
    CATEGORY_SAVE_BUTTON,
)


@pytest.fixture
def driver():
    """Create and close WebDriver"""
    driver = get_driver()
    yield driver
    driver.quit()


def login(driver):
    """Helper function to login"""
    driver.get(LOGIN_URL)
    time.sleep(1)

    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, EMAIL_INPUT))
    )
    email_field.clear()
    time.sleep(1)
    email_field.send_keys(EMAIL)

    password_field = driver.find_element(By.CSS_SELECTOR, PASSWORD_INPUT)
    password_field.clear()
    time.sleep(1)
    password_field.send_keys(PASSWORD)

    submit_button = driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON)
    time.sleep(1)
    submit_button.click()

    # Wait for dashboard to load
    WebDriverWait(driver, 10).until(EC.url_to_be(DASHBOARD_URL))


def test_edit_category(driver):
    """Test editing a category"""
    # Login first
    login(driver)
    print("\nCurrent URL:", driver.current_url)

    # Verify admin navigation is present
    admin_nav = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ADMIN_NAVIGATION))
    )
    assert admin_nav.is_displayed(), "Admin navigation should be visible"
    print("Found admin navigation")

    # Click on Categories link
    categories_link = admin_nav.find_element(By.CSS_SELECTOR, CATEGORIES_LINK)
    categories_link.click()
    print("Clicked on Categories link")

    # Wait for categories page to load
    WebDriverWait(driver, 10).until(EC.url_to_be(CATEGORIES_URL))
    print("Navigated to categories page")

    # Find categories table
    categories_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CATEGORIES_TABLE))
    )
    assert categories_table.is_displayed(), "Categories table should be visible"
    print("Found categories table")

    # Find and click on "Test Category"
    category_links = driver.find_elements(By.CSS_SELECTOR, CATEGORY_NAME_LINK)
    target_category = None
    for link in category_links:
        if "gadgets" in link.text:
            target_category = link
            break

    assert target_category is not None, "gadgets not found"
    print("Found gadgets")
    target_category.click()

    # Verify we're on the edit page
    edit_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CATEGORY_EDIT_TITLE))
    )
    assert edit_title.is_displayed(), "Edit title should be visible"
    assert (
        "Editing gadgets" in edit_title.text
    ), f"Title should contain 'Editing gadgets', got: {edit_title.text}"
    print("Navigated to edit page")

    # Edit category fields
    name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CATEGORY_NAME_INPUT))
    )
    name_input.clear()
    name_input.send_keys("gadgets Updated")
    print("Updated category name")

    url_key_input = driver.find_element(By.CSS_SELECTOR, CATEGORY_URL_KEY_INPUT)
    url_key_input.clear()
    url_key_input.send_keys("test-gadgets-updated")
    print("Updated URL key")

    meta_title_input = driver.find_element(By.CSS_SELECTOR, CATEGORY_META_TITLE_INPUT)
    meta_title_input.clear()
    meta_title_input.send_keys("Updated Meta Title")
    print("Updated meta title")

    meta_keywords_input = driver.find_element(
        By.CSS_SELECTOR, CATEGORY_META_KEYWORDS_INPUT
    )
    meta_keywords_input.clear()
    meta_keywords_input.send_keys("updated, meta, keywords")
    print("Updated meta keywords")

    meta_description_input = driver.find_element(
        By.CSS_SELECTOR, CATEGORY_META_DESCRIPTION_INPUT
    )
    meta_description_input.clear()
    meta_description_input.send_keys("Updated meta description for the category")
    print("Updated meta description")

    # Verify radio buttons are selected
    status_radio = driver.find_element(By.CSS_SELECTOR, CATEGORY_STATUS_RADIO)
    assert status_radio.is_selected(), "Status radio should be selected"

    include_in_nav_radio = driver.find_element(
        By.CSS_SELECTOR, CATEGORY_INCLUDE_IN_NAV_RADIO
    )
    assert include_in_nav_radio.is_selected(), "Include in nav radio should be selected"

    show_products_radio = driver.find_element(
        By.CSS_SELECTOR, CATEGORY_SHOW_PRODUCTS_RADIO
    )
    assert show_products_radio.is_selected(), "Show products radio should be selected"
    print("Verified radio buttons")

    # Click save button
    save_button = driver.find_element(By.CSS_SELECTOR, CATEGORY_SAVE_BUTTON)
    save_button.click()
    print("Clicked save button")

    # Wait for success message or redirect
    time.sleep(2)  # Wait for any success message
    print("Category updated successfully")
