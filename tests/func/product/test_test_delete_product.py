import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import (
    get_driver,
    LOGIN_URL,
    EMAIL,
    PASSWORD,
    EMAIL_INPUT,
    PASSWORD_INPUT,
    SUBMIT_BUTTON,
    DASHBOARD_URL,
    ADMIN_NAV_CONTAINER,
    PRODUCTS_LINK,
    PRODUCTS_URL,
    PRODUCTS_TABLE,
    PRODUCT_NAME_LINK,
    PRODUCT_CHECKBOX,
    PRODUCT_SELECTED_COUNT,
    PRODUCT_DELETE_BUTTON,
    DELETE_CONFIRM_BUTTON,
    DELETE_CANCEL_BUTTON,
    WAIT_TIME,
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


def test_delete_product(driver):
    """Test deleting a product"""
    # Login first
    login(driver)
    print("\nCurrent URL:", driver.current_url)

    # Verify admin navigation is present
    admin_nav_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ADMIN_NAV_CONTAINER))
    )
    assert admin_nav_container.is_displayed(), "Admin nav container should be visible"
    print("Found admin nav container")

    # Click on Products link (by text)
    products_links = admin_nav_container.find_elements(By.CSS_SELECTOR, PRODUCTS_LINK)
    products_link = None
    for link in products_links:
        if "Products" in link.text:
            products_link = link
            break
    assert products_link is not None, "Products link not found in admin nav"
    products_link.click()
    print("Clicked on Products link")

    # Wait for products page to load
    WebDriverWait(driver, 10).until(EC.url_to_be(PRODUCTS_URL))
    print("Navigated to products page")

    # Find products table
    products_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, PRODUCTS_TABLE))
    )
    assert products_table.is_displayed(), "Products table should be visible"
    print("Found products table")

    # Find and select a product to delete
    product_links = driver.find_elements(By.CSS_SELECTOR, PRODUCT_NAME_LINK)
    target_product = None
    target_checkbox_span = None
    target_product_name = None  # Store the name of the product we're deleting

    for link in product_links:
        if "Test Product" in link.text:
            target_product = link
            target_product_name = link.text  # Store the exact name
            # Find the checkbox span in the same row
            row = link.find_element(By.XPATH, "./ancestor::tr")
            target_checkbox_span = row.find_element(
                By.CSS_SELECTOR, "span.checkbox-unchecked"
            )
            break

    assert target_product is not None, "Test Product not found"
    assert target_checkbox_span is not None, "Product checkbox span not found"
    print(f"Found product to delete: {target_product_name}")

    # Wait for checkbox span to be clickable and click it
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "span.checkbox-unchecked"))
    )
    target_checkbox_span.click()
    print("Clicked product checkbox span")

    # Verify selection count
    selected_count = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, PRODUCT_SELECTED_COUNT))
    )
    assert (
        "1" in selected_count.text
    ), f"Should show 1 product selected, got: {selected_count.text}"
    print("Verified selection count")

    # Click delete button
    delete_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, PRODUCT_DELETE_BUTTON))
    )
    delete_button.click()
    print("Clicked delete button")

    # Verify delete confirmation dialog
    modal_overlay = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal-overlay.fadeIn"))
    )
    assert modal_overlay.is_displayed(), "Modal overlay should be visible"
    print("Found delete confirmation modal")

    # Wait for modal to be fully visible and clickable
    time.sleep(WAIT_TIME * 2)  # Wait for animation to complete

    # Find and click confirm button using JavaScript
    confirm_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.button.critical"))
    )
    driver.execute_script("arguments[0].click();", confirm_button)
    print("Clicked confirm button using JavaScript")

    # Wait for modal to disappear
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "div.modal-overlay.fadeIn")
        )
    )
    print("Modal disappeared")

    # Wait 4 seconds after confirmation
    print("Waiting 4 seconds after confirmation...")
    time.sleep(4)

    # Refresh the page
    print("Refreshing page...")
    driver.refresh()

    # Wait for the table to be present after refresh
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, PRODUCTS_TABLE))
    )
    print("Page refreshed, checking product list...")

    # Check if the specific product is removed
    product_links = driver.find_elements(By.CSS_SELECTOR, PRODUCT_NAME_LINK)
    product_names = [link.text for link in product_links]
    print(f"Current products in list: {product_names}")

    assert (
        target_product_name not in product_names
    ), f"Product '{target_product_name}' should be removed from list"
    print(f"Verified product '{target_product_name}' was removed")
