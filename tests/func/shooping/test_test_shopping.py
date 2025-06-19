import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import (
    get_driver,
    HOME_URL,
    CART_URL,
    FEATURED_PRODUCTS_TITLE,
    PRODUCTS_GRID,
    PRODUCT_LINK,
    ADD_TO_CART_BUTTON,
    MINI_CART_TOAST,
    MINI_CART_TITLE,
    MINI_CART_ITEM_NAME,
    MINI_CART_ITEM_QTY,
    VIEW_CART_BUTTON,
    CONTINUE_SHOPPING_LINK,
)


@pytest.fixture
def driver():
    """Create and close WebDriver"""
    driver = get_driver()
    yield driver
    driver.quit()


def test_shopping_journey(driver):
    """Test the shopping journey from home page to cart"""
    # Navigate to home page
    driver.get(HOME_URL)
    print("\nNavigated to home page")

    # Verify Featured Products section
    featured_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, FEATURED_PRODUCTS_TITLE))
    )
    assert featured_title.is_displayed(), "Featured Products title should be visible"
    assert (
        featured_title.text.upper() == "FEATURED PRODUCTS"
    ), "Title should be 'FEATURED PRODUCTS'"
    print("Found Featured Products section")

    # Find products grid
    products_grid = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, PRODUCTS_GRID))
    )
    assert products_grid.is_displayed(), "Products grid should be visible"
    print("Found products grid")

    # Find and click on the first product in the list
    product_links = driver.find_elements(By.CSS_SELECTOR, "div.product-name a")
    assert len(product_links) > 0, "No products found in the grid"
    first_product = product_links[0]  # Get the first product link
    product_name = first_product.text.strip()
    print(f"Found product: {product_name}")
    first_product.click()
    print(f"Clicked on product: {product_name}")

    # Verify product title on the product page
    product_title = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-single-name"))
    )
    assert product_title.is_displayed(), "Product title should be visible"
    print(f"Product title on page: {product_title.text}")

    # Vérifier la présence du titre produit et du bouton 'ADD TO CART'
    add_to_cart = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ADD_TO_CART_BUTTON))
    )
    assert add_to_cart.is_displayed(), "Add to Cart button should be visible"
    print("Found Add to Cart button")

    # Scroll to button and click
    driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart)
    time.sleep(1)  # Wait for scroll to complete
    add_to_cart.click()
    print("Clicked Add to Cart button")

    # Wait and check for mini cart
    time.sleep(2)  # Wait for mini cart to appear
    mini_carts = driver.find_elements(By.CSS_SELECTOR, MINI_CART_TOAST)
    print(f"Found {len(mini_carts)} mini cart elements")

    # Verify mini cart toast appears
    mini_cart = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, MINI_CART_TOAST))
    )
    assert mini_cart.is_displayed(), "Mini cart toast should be visible"

    # Verify mini cart contents
    cart_title = mini_cart.find_element(By.CSS_SELECTOR, MINI_CART_TITLE)
    assert cart_title.text == "JUST ADDED TO YOUR CART", "Cart title should be correct"

    item_name = mini_cart.find_element(By.CSS_SELECTOR, MINI_CART_ITEM_NAME)
    assert item_name.text == product_name, "Product name should be correct"

    item_qty = mini_cart.find_element(By.CSS_SELECTOR, MINI_CART_ITEM_QTY)
    assert item_qty.text == "QTY: 1", "Quantity should be 1"
    print("Verified mini cart contents")

    # Click View Cart button
    view_cart = mini_cart.find_element(By.CSS_SELECTOR, VIEW_CART_BUTTON)
    assert view_cart.is_displayed(), "View Cart button should be visible"
    print("Found View Cart button")
    view_cart.click()

    # Vérifier que l'URL est bien celle du panier
    WebDriverWait(driver, 10).until(EC.url_to_be(CART_URL))
    assert driver.current_url == CART_URL, f"URL inattendue : {driver.current_url}"
    print("Navigated to cart page")

    # Vérifier la présence du bloc checkout complet
    checkout_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "div.shopping-cart-checkout-btn.flex.justify-between.mt-8",
            )
        )
    )
    assert checkout_div.is_displayed(), "Le bloc checkout n'est pas visible"
    print("Bloc checkout visible")

    # Vérifier le lien CHECKOUT
    checkout_link = checkout_div.find_element(By.CSS_SELECTOR, "a.button.primary")
    assert checkout_link.is_displayed(), "Le lien CHECKOUT n'est pas visible"
    assert checkout_link.get_attribute("href").endswith(
        "/checkout"
    ), f"Lien inattendu : {checkout_link.get_attribute('href')}"
    assert (
        "CHECKOUT" in checkout_link.text.upper()
    ), "Le texte CHECKOUT n'est pas trouvé"
    print("Lien CHECKOUT correct et visible")

    # Cliquer sur le lien CHECKOUT
    checkout_link.click()
    print("Clic sur le lien CHECKOUT effectué")

    # Vérifier la redirection vers la page de checkout
    WebDriverWait(driver, 10).until(EC.url_to_be("http://localhost:3000/checkout"))
    assert (
        driver.current_url == "http://localhost:3000/checkout"
    ), f"URL inattendue après clic sur CHECKOUT : {driver.current_url}"
    print("Navigué vers la page de checkout")
