import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from config import (
    get_driver,
    LOGIN_URL,
    NEW_PRODUCT_URL,
    EMAIL,
    PASSWORD,
    EMAIL_INPUT,
    PASSWORD_INPUT,
    SUBMIT_BUTTON,
    NEW_PRODUCT_LINK,
    PRODUCT_NAME,
    PRODUCT_SKU,
    PRODUCT_PRICE,
    PRODUCT_WEIGHT,
    CATEGORY_SELECT,
    CATEGORY_SEARCH,
    CATEGORY_ITEM,
    CATEGORY_CLOSE,
    PRODUCT_TAX_CLASS,
    PRODUCT_URL_KEY,
    PRODUCT_META_TITLE,
    PRODUCT_META_KEYWORDS,
    PRODUCT_META_DESCRIPTION,
    PRODUCT_STATUS_ENABLED,
    PRODUCT_VISIBILITY_VISIBLE,
    PRODUCT_MANAGE_STOCK,
    PRODUCT_STOCK_AVAILABILITY,
    PRODUCT_QUANTITY,
    PRODUCT_ATTRIBUTE_GROUP,
    PRODUCT_COLOR,
    PRODUCT_SIZE,
    SAVE_PRODUCT_BUTTON,
    WAIT_TIME,
    TEST_IMAGE_PATH,
    IMAGE_UPLOAD_INPUT,
    IMAGE_UPLOAD_ICON,
    IMAGE_PREVIEW,
    IMAGE_UPLOADER,
    IMAGE_LIST,
    DESCRIPTION_EDITOR,
    DESCRIPTION_ROWS,
    DESCRIPTION_TEMPLATES,
    DESCRIPTION_TEMPLATE_LINKS,
    DESCRIPTION_INPUT,
)
import time
import os


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
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title"))
    )


def click_radio_button(driver, selector):
    """Helper function to click radio buttons using JavaScript"""
    try:
        radio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", radio)
        time.sleep(WAIT_TIME)
        driver.execute_script("arguments[0].click();", radio)
        time.sleep(WAIT_TIME)
    except Exception as e:
        print(f"Error clicking radio button {selector}: {str(e)}")
        raise


def select_category(driver):
    """Helper function to select a category"""
    # Click on category select button
    category_select = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, CATEGORY_SELECT))
    )
    category_select.click()
    time.sleep(WAIT_TIME)

    # Search for a category
    search_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CATEGORY_SEARCH))
    )
    search_field.clear()
    time.sleep(WAIT_TIME)
    search_field.send_keys("Lifestyle")
    time.sleep(WAIT_TIME)

    # Select the first category
    category_items = driver.find_elements(By.CSS_SELECTOR, CATEGORY_ITEM)
    if category_items:
        category_items[0].click()
        time.sleep(WAIT_TIME)

    # Close the category modal
    close_buttons = driver.find_elements(By.CSS_SELECTOR, CATEGORY_CLOSE)
    for button in close_buttons:
        if "Close" in button.text:
            button.click()
            time.sleep(WAIT_TIME)
            break


def upload_image(driver):
    """Helper function to upload an image"""
    try:
        # Wait for the uploader to be present
        uploader = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, IMAGE_UPLOADER))
        )
        print("Found uploader element")

        # Find the file input element
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, IMAGE_UPLOAD_INPUT))
        )
        print("Found file input element")

        # Get the absolute path of the test image
        image_path = os.path.abspath(TEST_IMAGE_PATH)
        print(f"Uploading image from: {image_path}")

        # Make sure the file exists
        if not os.path.exists(image_path):
            print(f"Error: Image file not found at {image_path}")
            return False

        # Send the file path to the input element
        file_input.send_keys(image_path)
        print("File path sent to input element")
        time.sleep(WAIT_TIME * 3)  # Wait longer for image upload

        # Try to find the image preview
        try:
            # Wait for the image list to contain an image
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, IMAGE_LIST))
            )
            print("Image list found")

            # Wait for the image preview to appear
            preview = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, IMAGE_PREVIEW))
            )
            print("Image preview found")

            # Verify the image is actually loaded
            if preview.get_attribute("src"):
                print("Image source is set")
                return True
            else:
                print("Image source is not set")
                return False

        except Exception as e:
            print(f"Error finding image preview: {str(e)}")
            return False

    except Exception as e:
        print(f"Error during image upload: {str(e)}")
        return False


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
        template_links = driver.find_elements(
            By.CSS_SELECTOR, DESCRIPTION_TEMPLATE_LINKS
        )
        if template_links:
            template_links[0].click()
            time.sleep(WAIT_TIME)
            print("Clicked first template")

            # Wait for the rows container to be present
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, DESCRIPTION_ROWS))
            )
            print("Found rows container")

            # Add some text to the description
            driver.execute_script(
                """
                var row = document.createElement('div');
                row.className = 'row';
                row.innerHTML = '<div class="col"><p>This is a test product description. It includes multiple paragraphs to demonstrate the product features and benefits.</p><p>Second paragraph with more details about the product specifications and usage instructions.</p></div>';
                document.getElementById('rows').appendChild(row);
            """
            )
            time.sleep(WAIT_TIME)
            print("Added description text")

            return True
    except Exception as e:
        print(f"Error adding product description: {str(e)}")
        return False


def test_add_product(driver):
    """Test adding a new product"""
    # First login
    login(driver)

    # Navigate to new product page
    driver.get(NEW_PRODUCT_URL)
    time.sleep(WAIT_TIME)

    # Fill in product details
    # Basic Information
    name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, PRODUCT_NAME))
    )
    name_field.clear()
    time.sleep(WAIT_TIME)
    name_field.send_keys("Test Product")

    sku_field = driver.find_element(By.CSS_SELECTOR, PRODUCT_SKU)
    sku_field.clear()
    time.sleep(WAIT_TIME)
    unique_sku = f"TEST-SKU-{int(time.time()* 1000)}"
    sku_field.send_keys(unique_sku)

    price_field = driver.find_element(By.CSS_SELECTOR, PRODUCT_PRICE)
    price_field.clear()
    time.sleep(WAIT_TIME)
    price_field.send_keys("99.99")

    weight_field = driver.find_element(By.CSS_SELECTOR, PRODUCT_WEIGHT)
    weight_field.clear()
    time.sleep(WAIT_TIME)
    weight_field.send_keys("1.5")

    # Upload product image
    assert upload_image(driver), "Failed to upload product image"

    # Add product description
    assert add_product_description(driver), "Failed to add product description"

    # Select category
    select_category(driver)

    # Select tax class
    tax_class = Select(driver.find_element(By.CSS_SELECTOR, PRODUCT_TAX_CLASS))
    time.sleep(WAIT_TIME)
    tax_class.select_by_value("1")  # Taxable Goods

    # description of product display

    # SEO Information
    url_key = driver.find_element(By.CSS_SELECTOR, PRODUCT_URL_KEY)
    url_key.clear()
    time.sleep(WAIT_TIME)
    unique_url = f"test-product-{int(time.time())}"
    url_key.send_keys(unique_url)

    meta_title = driver.find_element(By.CSS_SELECTOR, PRODUCT_META_TITLE)
    meta_title.clear()
    time.sleep(WAIT_TIME)
    meta_title.send_keys("Test Product Meta Title")

    meta_keywords = driver.find_element(By.CSS_SELECTOR, PRODUCT_META_KEYWORDS)
    meta_keywords.clear()
    time.sleep(WAIT_TIME)
    meta_keywords.send_keys("test, product, keywords")

    meta_description = driver.find_element(By.CSS_SELECTOR, PRODUCT_META_DESCRIPTION)
    meta_description.clear()
    time.sleep(WAIT_TIME)
    meta_description.send_keys("This is a test product description for SEO purposes.")

    # Product Status
    click_radio_button(driver, PRODUCT_STATUS_ENABLED)
    click_radio_button(driver, PRODUCT_VISIBILITY_VISIBLE)

    # Inventory
    click_radio_button(driver, PRODUCT_MANAGE_STOCK)
    click_radio_button(driver, PRODUCT_STOCK_AVAILABILITY)

    quantity = driver.find_element(By.CSS_SELECTOR, PRODUCT_QUANTITY)
    quantity.clear()
    time.sleep(WAIT_TIME)
    quantity.send_keys("100")

    # Attributes
    attribute_group = Select(
        driver.find_element(By.CSS_SELECTOR, PRODUCT_ATTRIBUTE_GROUP)
    )
    time.sleep(WAIT_TIME)
    attribute_group.select_by_value("1")  # Default

    color = Select(driver.find_element(By.CSS_SELECTOR, PRODUCT_COLOR))
    time.sleep(WAIT_TIME)
    color.select_by_value("1")  # White

    size = Select(driver.find_element(By.CSS_SELECTOR, PRODUCT_SIZE))
    time.sleep(WAIT_TIME)
    size.select_by_value("4")  # XXL

    # Save the product
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, SAVE_PRODUCT_BUTTON))
    )
    time.sleep(WAIT_TIME)
    save_button.click()

    # Wait for success message or redirect
    time.sleep(WAIT_TIME * 2)  # Wait longer for save operation

    # Verify we're redirected to products page
    assert "products" in driver.current_url

    # Verify meta description was saved
    meta_description_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#meta_description"))
    )
    meta_description_text = meta_description_field.get_attribute("value")
    print(f"Meta description content: {meta_description_text}")
    assert (
        "this is a test product description for seo purposes"
        in meta_description_text.lower()
    ), "Meta description not saved correctly"
    print("Meta description verified")
