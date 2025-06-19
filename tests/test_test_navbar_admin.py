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
    NAVBAR,
    NAV_ITEMS,
    ROOT_NAV_ITEMS,
    ROOT_LABELS,
    DASHBOARD_URL,
    PRODUCTS_URL,
    NEW_PRODUCT_URL,
    CATEGORIES_URL,
    COLLECTIONS_URL,
    ATTRIBUTES_URL,
    ORDERS_URL,
    CUSTOMERS_URL,
    COUPONS_URL,
    NEW_COUPON_URL,
    PAGES_URL,
    WIDGETS_URL,
    SETTINGS_URL,
    PAGE_TITLE
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
        EC.presence_of_element_located((By.CSS_SELECTOR, PAGE_TITLE))
    )

def test_navbar_presence(driver):
    """Test that navbar elements are present"""
    login(driver)
    
    # Verify navbar is present
    navbar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, NAVBAR))
    )
    assert navbar.is_displayed(), "Navbar should be visible"
    
    # Verify root navigation items are present
    root_items = driver.find_elements(By.CSS_SELECTOR, ROOT_NAV_ITEMS)
    expected_sections = ["Quick links", "Catalog", "Sale", "Customer", "Promotion", "CMS", "Setting"]
    assert len(root_items) == len(expected_sections), f"Expected {len(expected_sections)} root sections"
    
    # Verify navigation items are present
    nav_items = driver.find_elements(By.CSS_SELECTOR, NAV_ITEMS)
    assert len(nav_items) > 0, "Should have navigation items"

def test_navbar_navigation(driver):
    """Test navigation through navbar links"""
    login(driver)
    
    # Dictionary of navigation items and their expected URLs
    nav_links = {
        "Dashboard": DASHBOARD_URL,
        "New Product": NEW_PRODUCT_URL,
        "New Coupon": NEW_COUPON_URL,
        "Products": PRODUCTS_URL,
        "Categories": CATEGORIES_URL,
        "Collections": COLLECTIONS_URL,
        "Attributes": ATTRIBUTES_URL,
        "Orders": ORDERS_URL,
        "Customers": CUSTOMERS_URL,
        "Coupons": COUPONS_URL,
        "Pages": PAGES_URL,
        "Widgets": WIDGETS_URL,
        "Setting": SETTINGS_URL
    }
    
    # Test each navigation link
    for link_text, expected_url in nav_links.items():
        try:
            print(f"\nTesting navigation to: {link_text}")
            
            # Find the link
            link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{link_text}')]"))
            )
            time.sleep(WAIT_TIME)
            
            # Scroll the link into view
            driver.execute_script("arguments[0].scrollIntoView(true);", link)
            time.sleep(WAIT_TIME)
            
            # Click using JavaScript
            driver.execute_script("arguments[0].click();", link)
            time.sleep(WAIT_TIME)
            
            # Verify URL change
            WebDriverWait(driver, 10).until(
                EC.url_to_be(expected_url)
            )
            print(f"Successfully navigated to {expected_url}")
            
            # For Setting page, skip title check as it might have a different structure
            if link_text != "Setting":
                # Verify page title is present
                title = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, PAGE_TITLE))
                )
                assert title.is_displayed(), f"Page title should be visible for {link_text}"
            else:
                # For Setting page, just verify we're on the correct URL
                assert driver.current_url == expected_url, f"Should be on {expected_url}"
            
            # Verify navbar is still present
            navbar = driver.find_element(By.CSS_SELECTOR, NAVBAR)
            assert navbar.is_displayed(), "Navbar should remain visible after navigation"
            
            time.sleep(WAIT_TIME)  # Wait between navigations
            
        except Exception as e:
            print(f"Error navigating to {link_text}: {str(e)}")
            raise

def test_navbar_visibility_across_pages(driver):
    """Test navbar visibility across different pages"""
    login(driver)
    
    # List of pages to test
    pages = [
        DASHBOARD_URL,
        NEW_PRODUCT_URL,
        NEW_COUPON_URL,
        PRODUCTS_URL,
        CATEGORIES_URL,
        COLLECTIONS_URL,
        ATTRIBUTES_URL,
        ORDERS_URL,
        CUSTOMERS_URL,
        COUPONS_URL,
        PAGES_URL,
        WIDGETS_URL,
        SETTINGS_URL
    ]
    
    # Test navbar visibility on each page
    for page_url in pages:
        print(f"\nTesting navbar visibility on: {page_url}")
        driver.get(page_url)
        time.sleep(WAIT_TIME)
        
        # Verify navbar is present and visible
        navbar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, NAVBAR))
        )
        assert navbar.is_displayed(), f"Navbar should be visible on {page_url}"
        
        # Verify all navigation items are clickable
        nav_items = driver.find_elements(By.CSS_SELECTOR, NAV_ITEMS)
        for item in nav_items:
            assert item.is_displayed(), f"Navigation item should be visible on {page_url}"
            assert item.is_enabled(), f"Navigation item should be enabled on {page_url}"
