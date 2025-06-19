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
    CATEGORY_SELECT_BUTTON,
    CATEGORY_TREE,
    CATEGORY_TREE_ITEMS,
    CATEGORY_TEMPLATES,
    CATEGORY_URL_KEY,
    CATEGORY_META_TITLE,
    CATEGORY_META_KEYWORDS,
    CATEGORY_META_DESCRIPTION,
    CATEGORY_ADD_IMAGE,
    CATEGORY_STATUS_ENABLED,
    CATEGORY_INCLUDE_IN_NAV_RADIO,
    CATEGORY_SHOW_PRODUCTS,
    CATEGORY_CANCEL_BUTTON,
    CATEGORY_SAVE_BUTTON,
    CATEGORIES_URL,
    NEW_CATEGORY_URL,
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
    WebDriverWait(driver, 10).until(EC.url_to_be(DASHBOARD_URL))


def test_add_category_form(driver):
    """Test filling and submitting the category form"""
    # Login first
    login(driver)
    print("\nCurrent URL:", driver.current_url)

    # Navigate to new category page
    admin_nav = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ADMIN_NAVIGATION))
    )
    categories_link = admin_nav.find_element(By.CSS_SELECTOR, CATEGORIES_LINK)
    categories_link.click()

    WebDriverWait(driver, 10).until(EC.url_to_be(CATEGORIES_URL))

    new_category_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, NEW_CATEGORY_BUTTON))
    )
    new_category_btn.click()

    WebDriverWait(driver, 10).until(EC.url_to_be(NEW_CATEGORY_URL))

    print("\nFilling category form...")

    # Fill name
    print("Filling name")
    name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CATEGORY_NAME_INPUT))
    )
    name_input.clear()
    time.sleep(WAIT_TIME)
    name_input.send_keys("gadgets")

    # Select parent category
    print("Selecting parent category")
    select_btn = driver.find_element(By.CSS_SELECTOR, CATEGORY_SELECT_BUTTON)
    select_btn.click()
    time.sleep(WAIT_TIME)

    # Wait for tree and select first category
    category_tree = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CATEGORY_TREE))
    )
    first_category = category_tree.find_element(
        By.CSS_SELECTOR, "li a:nth-child(2)"
    )  # Select the category name link
    first_category.click()
    time.sleep(WAIT_TIME)

    # Fill URL Key
    print("Filling URL key")
    url_key = driver.find_element(By.CSS_SELECTOR, CATEGORY_URL_KEY)
    url_key.clear()
    time.sleep(WAIT_TIME)
    unique_url = f"test-category-{int(time.time())}"
    url_key.send_keys(unique_url)

    # Fill Meta Title
    print("Filling meta title")
    meta_title = driver.find_element(By.CSS_SELECTOR, CATEGORY_META_TITLE)
    meta_title.clear()
    time.sleep(WAIT_TIME)
    meta_title.send_keys("Test Category Meta Title")

    # Fill Meta Keywords
    print("Filling meta keywords")
    meta_keywords = driver.find_element(By.CSS_SELECTOR, CATEGORY_META_KEYWORDS)
    meta_keywords.clear()
    time.sleep(WAIT_TIME)
    meta_keywords.send_keys("test, category, keywords")

    # Fill Meta Description
    print("Filling meta description")
    meta_description = driver.find_element(By.CSS_SELECTOR, CATEGORY_META_DESCRIPTION)
    meta_description.clear()
    time.sleep(WAIT_TIME)
    meta_description.send_keys(
        "This is a test category description for testing purposes."
    )

    # Add Image
    print("Adding image")
    file_input = driver.find_element(
        By.CSS_SELECTOR, "input[type='file']#categoryImageUpload"
    )
    image_path = os.path.abspath("config/test_image.jpg")
    file_input.send_keys(image_path)
    time.sleep(WAIT_TIME * 2)  # Wait longer for image upload

    # Verify radio buttons are selected
    print("Verifying radio buttons")
    status = driver.find_element(By.CSS_SELECTOR, CATEGORY_STATUS_ENABLED)
    assert status.is_selected(), "Status should be enabled"

    include_nav = driver.find_element(By.CSS_SELECTOR, CATEGORY_INCLUDE_IN_NAV_RADIO)
    assert include_nav.is_selected(), "Include in nav should be yes"

    show_products = driver.find_element(By.CSS_SELECTOR, CATEGORY_SHOW_PRODUCTS)
    assert show_products.is_selected(), "Show products should be yes"

    # Save the category
    print("Saving category")
    save_btn = driver.find_element(By.CSS_SELECTOR, CATEGORY_SAVE_BUTTON)
    save_btn.click()

    # Wait for success toast with the exact structure
    time.sleep(WAIT_TIME * 2)
    try:
        # Attendre d'abord que le toast soit présent
        toast = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.Toastify__toast.Toastify__toast--success")
            )
        )
        # Puis attendre que le message soit visible
        toast_body = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.Toastify__toast-body[role='alert']")
            )
        )
        print(f"Toast found with text: '{toast_body.text}'")
        assert (
            "Category saved successfully!" in toast_body.text
        ), f"Toast should contain 'Category saved successfully!', got: '{toast_body.text}'"

        # Vérifier que nous sommes sur la page d'édition avec le bon titre
        edit_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title"))
        )
        print(f"Redirected to edit page with title: '{edit_title.text}'")

        # Vérifier que nous sommes sur la page d'édition avec le bon titre
        assert (
            "Editing gadgets" in edit_title.text
        ), f"Expected 'Editing gadgets' in title, got '{edit_title.text}'"

        # Vérifier tous les champs du formulaire
        print("\nVerifying form fields after save:")

        # Vérifier le nom
        name_input = driver.find_element(By.CSS_SELECTOR, CATEGORY_NAME_INPUT)
        actual_name = name_input.get_attribute("value")
        print(f"Name - Expected: 'gadgets', Actual: '{actual_name}'")
        assert actual_name == "gadgets", f"Expected name 'gadgets', got '{actual_name}'"

        # Vérifier l'URL key
        url_key = driver.find_element(By.CSS_SELECTOR, CATEGORY_URL_KEY)
        actual_url = url_key.get_attribute("value")
        print(
            f"URL key - Expected to contain: 'test-category-', Actual: '{actual_url}'"
        )
        assert (
            "test-category-" in actual_url
        ), f"URL key should contain 'test-category-', got '{actual_url}'"

        # Vérifier le meta title
        meta_title = driver.find_element(By.CSS_SELECTOR, CATEGORY_META_TITLE)
        actual_meta_title = meta_title.get_attribute("value")
        print(
            f"Meta title - Expected: 'Test Category Meta Title', Actual: '{actual_meta_title}'"
        )
        assert (
            actual_meta_title == "Test Category Meta Title"
        ), f"Expected meta title 'Test Category Meta Title', got '{actual_meta_title}'"

        # Vérifier les meta keywords
        meta_keywords = driver.find_element(By.CSS_SELECTOR, CATEGORY_META_KEYWORDS)
        actual_meta_keywords = meta_keywords.get_attribute("value")
        print(
            f"Meta keywords - Expected: 'test, category, keywords', Actual: '{actual_meta_keywords}'"
        )
        assert (
            actual_meta_keywords == "test, category, keywords"
        ), f"Expected meta keywords 'test, category, keywords', got '{actual_meta_keywords}'"

        # Vérifier la meta description
        meta_description = driver.find_element(
            By.CSS_SELECTOR, CATEGORY_META_DESCRIPTION
        )
        actual_meta_description = meta_description.get_attribute("value")
        print(
            f"Meta description - Expected: 'This is a test category description for testing purposes.', Actual: '{actual_meta_description}'"
        )
        assert (
            actual_meta_description
            == "This is a test category description for testing purposes."
        ), f"Expected meta description 'This is a test category description for testing purposes.', got '{actual_meta_description}'"

        # Vérifier que les boutons radio sont toujours sélectionnés
        status = driver.find_element(By.CSS_SELECTOR, CATEGORY_STATUS_ENABLED)
        assert status.is_selected(), "Status should still be enabled"
        print("Status is still enabled")

        include_nav = driver.find_element(
            By.CSS_SELECTOR, CATEGORY_INCLUDE_IN_NAV_RADIO
        )
        assert include_nav.is_selected(), "Include in nav should still be yes"
        print("Include in nav is still yes")

        show_products = driver.find_element(By.CSS_SELECTOR, CATEGORY_SHOW_PRODUCTS)
        assert show_products.is_selected(), "Show products should still be yes"
        print("Show products is still yes")

        print("\nAll form fields verified successfully after save")

    except Exception as e:
        print(f"Toast not found or error: {str(e)}")
        # Vérifier si nous sommes redirigés vers la page d'édition
        try:
            edit_title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h1.page-heading-title")
                )
            )
            print(f"Redirected to edit page with title: '{edit_title.text}'")

            # Vérifier que nous sommes sur la page d'édition avec le bon titre
            assert (
                "Editing gadgets" in edit_title.text
            ), f"Expected 'Editing gadgets' in title, got '{edit_title.text}'"

            # Vérifier tous les champs du formulaire
            print("\nVerifying form fields after save:")

            # Vérifier le nom
            name_input = driver.find_element(By.CSS_SELECTOR, CATEGORY_NAME_INPUT)
            actual_name = name_input.get_attribute("value")
            print(f"Name - Expected: 'gadgets', Actual: '{actual_name}'")
            assert (
                actual_name == "gadgets"
            ), f"Expected name 'gadgets', got '{actual_name}'"

            # Vérifier l'URL key
            url_key = driver.find_element(By.CSS_SELECTOR, CATEGORY_URL_KEY)
            actual_url = url_key.get_attribute("value")
            print(
                f"URL key - Expected to contain: 'test-category-', Actual: '{actual_url}'"
            )
            assert (
                "test-category-" in actual_url
            ), f"URL key should contain 'test-category-', got '{actual_url}'"

            # Vérifier le meta title
            meta_title = driver.find_element(By.CSS_SELECTOR, CATEGORY_META_TITLE)
            actual_meta_title = meta_title.get_attribute("value")
            print(
                f"Meta title - Expected: 'Test Category Meta Title', Actual: '{actual_meta_title}'"
            )
            assert (
                actual_meta_title == "Test Category Meta Title"
            ), f"Expected meta title 'Test Category Meta Title', got '{actual_meta_title}'"

            # Vérifier les meta keywords
            meta_keywords = driver.find_element(By.CSS_SELECTOR, CATEGORY_META_KEYWORDS)
            actual_meta_keywords = meta_keywords.get_attribute("value")
            print(
                f"Meta keywords - Expected: 'test, category, keywords', Actual: '{actual_meta_keywords}'"
            )
            assert (
                actual_meta_keywords == "test, category, keywords"
            ), f"Expected meta keywords 'test, category, keywords', got '{actual_meta_keywords}'"

            # Vérifier la meta description
            meta_description = driver.find_element(
                By.CSS_SELECTOR, CATEGORY_META_DESCRIPTION
            )
            actual_meta_description = meta_description.get_attribute("value")
            print(
                f"Meta description - Expected: 'This is a test category description for testing purposes.', Actual: '{actual_meta_description}'"
            )
            assert (
                actual_meta_description
                == "This is a test category description for testing purposes."
            ), f"Expected meta description 'This is a test category description for testing purposes.', got '{actual_meta_description}'"

            # Vérifier que les boutons radio sont toujours sélectionnés
            status = driver.find_element(By.CSS_SELECTOR, CATEGORY_STATUS_ENABLED)
            assert status.is_selected(), "Status should still be enabled"
            print("Status is still enabled")

            include_nav = driver.find_element(
                By.CSS_SELECTOR, CATEGORY_INCLUDE_IN_NAV_RADIO
            )
            assert include_nav.is_selected(), "Include in nav should still be yes"
            print("Include in nav is still yes")

            show_products = driver.find_element(By.CSS_SELECTOR, CATEGORY_SHOW_PRODUCTS)
            assert show_products.is_selected(), "Show products should still be yes"
            print("Show products is still yes")

            print("\nAll form fields verified successfully after save")

        except Exception as e2:
            print(f"Not redirected to edit page: {str(e2)}")
            raise
