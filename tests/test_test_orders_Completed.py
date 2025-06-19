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
    ORDERS_URL,
    ORDERS_TABLE,
    ORDER_DELIVERED,
    ORDER_PAID,
    ORDER_NUMBER_LINK,
    ORDER_EDIT_TITLE,
    ORDER_COMPLETED_BADGE,
    ORDER_BACK_BUTTON
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

def test_navigate_to_completed_order(driver):
    """Test navigation to a completed order (Delivered + Paid)"""
    login(driver)
    print("\nCurrent URL:", driver.current_url)

    # Navigation vers la page commandes
    admin_nav = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ADMIN_NAVIGATION))
    )
    orders_link = admin_nav.find_element(By.CSS_SELECTOR, ORDERS_LINK)
    orders_link.click()
    WebDriverWait(driver, 10).until(
        EC.url_to_be(ORDERS_URL)
    )
    print("Navigated to orders page")

    # Trouver le tableau des commandes
    orders_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ORDERS_TABLE))
    )
    assert orders_table.is_displayed(), "Orders table should be visible"
    print("Orders table found")

    # Parcourir les lignes du tableau
    rows = orders_table.find_elements(By.CSS_SELECTOR, "tbody > tr")
    print(f"Found {len(rows)} order rows")
    completed_order_link = None
    for row in rows:
        tds = row.find_elements(By.TAG_NAME, "td")
        if len(tds) < 6:
            continue
        # Statut livraison (5e td), paiement (6e td)
        shipment_status = tds[4].find_element(By.CSS_SELECTOR, ".self-center.title").text.strip()
        payment_status = tds[5].find_element(By.CSS_SELECTOR, ".self-center.title").text.strip()
        print(f"Order status - Delivered: {shipment_status}, Paid: {payment_status}")
        if shipment_status == "Delivered" and payment_status == "Paid":
            # Lien du numéro de commande (2e td)
            completed_order_link = tds[1].find_element(By.TAG_NAME, "a")
            print("Found completed order!")
            break

    assert completed_order_link is not None, "No completed order found"
    print("Clicking on completed order")
    completed_order_link.click()

    # Vérifier la page d'édition de la commande
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ORDER_EDIT_TITLE))
    )
    print("Order edit page loaded")

    completed_badge = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ORDER_COMPLETED_BADGE))
    )
    assert completed_badge.is_displayed(), "Completed badge should be visible"
    print("Completed badge found")

    back_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ORDER_BACK_BUTTON))
    )
    assert back_button.is_displayed(), "Back button should be visible"
    print("Back button found")
