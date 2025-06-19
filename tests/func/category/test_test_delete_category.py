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
    CATEGORIES_URL,
    CATEGORY_TABLE,
    CATEGORY_ROW,
    CATEGORY_CHECKBOX,
    CATEGORY_CHECKBOX_CONTAINER,
    CATEGORY_SELECTED_COUNT,
    CATEGORY_DELETE_BUTTON,
    DELETE_MODAL,
    DELETE_MODAL_TITLE,
    DELETE_CONFIRM_BUTTON,
    CATEGORY_NAME_LINK,
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
    WebDriverWait(driver, 10).until(EC.url_to_be(DASHBOARD_URL))


def test_delete_category(driver):
    """Test deleting a category"""
    # Login first
    login(driver)
    print("\nCurrent URL:", driver.current_url)

    # Navigate to categories page
    admin_nav = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ADMIN_NAVIGATION))
    )
    categories_link = admin_nav.find_element(By.CSS_SELECTOR, CATEGORIES_LINK)
    categories_link.click()

    # Wait for categories page to load
    WebDriverWait(driver, 10).until(EC.url_to_be(CATEGORIES_URL))

    # Wait for the table to be present and visible
    table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, CATEGORY_TABLE))
    )

    # Wait for at least one row to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CATEGORY_ROW))
    )

    # Find the first visible category name
    category_links = driver.find_elements(By.CSS_SELECTOR, CATEGORY_NAME_LINK)
    first_category = None
    category_name = None

    for link in category_links:
        if link.is_displayed():
            first_category = link
            category_name = link.text
            break

    assert first_category is not None, "No category found in the table"
    print(f"\nCategory to delete: {category_name}")

    # Trouver la ligne (tr) correspondant à la catégorie
    first_row = first_category.find_element(By.XPATH, "./ancestor::tr")
    # Chercher le span de la checkbox dans cette ligne
    checkbox_span = first_row.find_element(By.CSS_SELECTOR, "span.checkbox-unchecked")
    # Cliquer sur la checkbox
    driver.execute_script("arguments[0].click();", checkbox_span)
    time.sleep(WAIT_TIME)

    # Verify the selection count appears
    selected_count = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CATEGORY_SELECTED_COUNT))
    )
    assert (
        "1 selected" in selected_count.text
    ), "Selection count should show '1 selected'"

    # Click the delete button
    delete_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, CATEGORY_DELETE_BUTTON))
    )
    delete_button.click()
    time.sleep(WAIT_TIME)

    # Wait for and verify the delete modal
    modal = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, DELETE_MODAL))
    )
    modal_title = modal.find_element(By.CSS_SELECTOR, DELETE_MODAL_TITLE)
    assert (
        "Delete 1 categories" in modal_title.text
    ), "Modal title should indicate deletion of 1 category"

    # Click the confirm delete button
    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, DELETE_CONFIRM_BUTTON))
    )
    confirm_button.click()
    time.sleep(WAIT_TIME * 2)  # Wait longer for deletion to complete

    # Refresh the page
    driver.refresh()
    time.sleep(WAIT_TIME)

    # Wait for the table to be present again after refresh
    table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, CATEGORY_TABLE))
    )

    # Get all category names
    category_links = table.find_elements(By.CSS_SELECTOR, CATEGORY_NAME_LINK)
    category_names = [link.text for link in category_links if link.is_displayed()]

    # Verify the deleted category is not in the list
    assert (
        category_name not in category_names
    ), f"Category '{category_name}' should not be in the list after deletion"
    print(f"\nCategory '{category_name}' successfully deleted")
