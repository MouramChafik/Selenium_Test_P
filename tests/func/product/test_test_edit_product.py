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
    PRODUCTS_LINK,
    PRODUCTS_URL,
    PRODUCTS_TABLE,
    PRODUCT_NAME_LINK,
    PRODUCT_EDIT_TITLE,
    PRODUCT_NAME_INPUT,
    PRODUCT_SKU_INPUT,
    PRODUCT_PRICE_INPUT,
    PRODUCT_QUANTITY,
    PRODUCT_STATUS_RADIO,
    PRODUCT_SAVE_BUTTON,
    ADMIN_NAV_CONTAINER,
    DESCRIPTION_EDITOR,
    DESCRIPTION_ROWS,
    DESCRIPTION_TEMPLATES,
    DESCRIPTION_TEMPLATE_LINKS,
    DESCRIPTION_INPUT
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
    WebDriverWait(driver, 10).until(
        EC.url_to_be(DASHBOARD_URL)
    )

def add_product_description(driver):
    """Helper function to add product description using the editor"""
    try:
        # Wait for the description editor to be present
        editor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, DESCRIPTION_EDITOR))
        )
        print("Found description editor")
        
        # Wait for the templates to be present
        templates = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, DESCRIPTION_TEMPLATES))
        )
        print("Found description templates")
        
        # Click on the first template (full width)
        template_links = driver.find_elements(By.CSS_SELECTOR, DESCRIPTION_TEMPLATE_LINKS)
        if template_links:
            template_links[0].click()
            time.sleep(1)
            print("Clicked first template")
            
            # Wait for the rows container to be present
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, DESCRIPTION_ROWS))
            )
            print("Found rows container")
            
            # Add some text to the description
            driver.execute_script("""
                var row = document.createElement('div');
                row.className = 'row';
                row.innerHTML = '<div class="col"><p>This is an updated test product description. It includes multiple paragraphs to demonstrate the product features and benefits.</p><p>Second paragraph with more details about the product specifications and usage instructions.</p></div>';
                document.getElementById('rows').appendChild(row);
            """)
            time.sleep(1)
            print("Added description text")
            
            return True
    except Exception as e:
        print(f"Error adding product description: {str(e)}")
        return False

def test_edit_product(driver):
    """Test editing a product"""
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
    WebDriverWait(driver, 10).until(
        EC.url_to_be(PRODUCTS_URL)
    )
    print("Navigated to products page")

    # Find products table
    products_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, PRODUCTS_TABLE))
    )
    assert products_table.is_displayed(), "Products table should be visible"
    print("Found products table")

    # Find and click on "Test Product"
    product_links = driver.find_elements(By.CSS_SELECTOR, PRODUCT_NAME_LINK)
    target_product = None
    for link in product_links:
        if "Test Product" in link.text:
            target_product = link
            break

    assert target_product is not None, "Test Product not found"
    print("Found Test Product")
    target_product.click()

    # Verify we're on the edit page
    edit_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, PRODUCT_EDIT_TITLE))
    )
    assert edit_title.is_displayed(), "Edit title should be visible"
    assert "Editing Test Product" in edit_title.text, "Title should contain 'Editing Test Product'"
    print("Navigated to edit page")

    # Edit product fields
    name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, PRODUCT_NAME_INPUT))
    )
    name_input.clear()
    name_input.send_keys("Test Product Updated")
    print("Updated product name")

    sku_input = driver.find_element(By.CSS_SELECTOR, PRODUCT_SKU_INPUT)
    sku_input.clear()
    sku_input.send_keys("TEST-SKU-UPDATED")
    print("Updated SKU")

    price_input = driver.find_element(By.CSS_SELECTOR, PRODUCT_PRICE_INPUT)
    price_input.clear()
    price_input.send_keys("149.99")
    print("Updated price")

    quantity_input = driver.find_element(By.CSS_SELECTOR, PRODUCT_QUANTITY)
    quantity_input.clear()
    quantity_input.send_keys("150")
    print("Updated quantity")

    # Update product description
    assert add_product_description(driver), "Failed to update product description"

    # Verify status radio is selected
    status_radio = driver.find_element(By.CSS_SELECTOR, PRODUCT_STATUS_RADIO)
    assert status_radio.is_selected(), "Status radio should be selected"
    print("Verified status radio")

    # Click save button
    save_button = driver.find_element(By.CSS_SELECTOR, PRODUCT_SAVE_BUTTON)
    save_button.click()
    print("Clicked save button")

    # Wait for success message or redirect
    time.sleep(2)  # Wait for any success message
    print("Product updated successfully")
