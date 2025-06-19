import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from config import get_driver, HOME_URL


@pytest.fixture
def driver():
    """Create and close WebDriver"""
    driver = get_driver()
    yield driver
    driver.quit()


@pytest.fixture
def panier_pret(driver):
    """Ajoute un produit au panier et arrive sur la page de checkout"""
    driver.get(HOME_URL)
    print("\nNavigated to home page")
    # Trouver et cliquer sur le premier produit
    product_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-name a"))
    )
    assert len(product_links) > 0, "No products found in the grid"
    first_product = product_links[0]
    product_name = first_product.text.strip()
    print(f"Found product: {product_name}")
    first_product.click()
    print(f"Clicked on product: {product_name}")
    # Ajouter au panier
    add_to_cart_buttons = driver.find_elements(
        By.CSS_SELECTOR, "button.button.primary.outline"
    )
    add_to_cart = None
    for btn in add_to_cart_buttons:
        if "ADD TO CART" in btn.text.upper():
            add_to_cart = btn
            break
    assert add_to_cart is not None, "Bouton 'ADD TO CART' introuvable"
    driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart)
    time.sleep(1)
    add_to_cart.click()
    print("Clicked 'ADD TO CART' button")
    # Attendre que le mini-cart (toast) s'ouvre après l'ajout au panier
    time.sleep(2)
    view_cart = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.add-cart-popup-button"))
    )
    view_cart.click()
    print("Clicked 'VIEW CART (1)' dans le mini-cart")
    # Cliquer sur le bouton Checkout
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button.primary"))
    )
    checkout_button.click()
    print("Clicked Checkout button")
    # On est maintenant sur la page de checkout
    WebDriverWait(driver, 10).until(EC.url_contains("/checkout"))
    print("Arrived on checkout page")
    return driver


def test_checkout_process(panier_pret):
    driver = panier_pret
    # Step 1: Email and Note
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']"))
    )
    email_input.send_keys("test@example.com")
    print("Email entered")
    note_textarea = driver.find_element(By.CSS_SELECTOR, "textarea#note")
    note_textarea.send_keys("Test order note")
    print("Note entered")
    save_button = driver.find_element(By.CSS_SELECTOR, "button.button.primary span")
    save_button.click()
    print("Clicked Save button")
    continue_shipping = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'] span"))
    )
    continue_shipping.click()
    print("Clicked Continue to shipping")
    # Step 2: Shipping Address
    shipping_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "checkoutShippingAddressForm"))
    )
    assert shipping_form.is_displayed(), "Shipping form should be visible"
    print("Shipping form is visible")
    full_name = driver.find_element(By.CSS_SELECTOR, "input[name='address[full_name]']")
    full_name.send_keys("ff")
    print("Full name entered")
    telephone = driver.find_element(By.CSS_SELECTOR, "input[name='address[telephone]']")
    telephone.send_keys("45454656")
    print("Telephone entered")
    address = driver.find_element(By.CSS_SELECTOR, "input[name='address[address_1]']")
    address.send_keys("45 rue delandine")
    print("Address entered")
    city = driver.find_element(By.CSS_SELECTOR, "input[name='address[city]']")
    city.send_keys("lyon")
    print("City entered")
    country_select = Select(driver.find_element(By.ID, "address[country]"))
    country_select.select_by_value("FR")
    print("Country selected: France")
    province_select = Select(driver.find_element(By.ID, "address[province]"))
    province_select.select_by_value("FR-ARA")
    print("Province selected: Auvergne-Rhone-Alpes")
    postcode = driver.find_element(By.CSS_SELECTOR, "input[name='address[postcode]']")
    postcode.send_keys("69002")
    print("Postcode entered")
    # Step 3: Shipping Method
    shipping_methods = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.field-wrapper.radio-field")
        )
    )
    assert shipping_methods.is_displayed(), "Shipping methods should be visible"
    print("Shipping methods are visible")
    # Cliquer sur le label associé à 'collissimo'
    labels = driver.find_elements(
        By.CSS_SELECTOR, "div.field-wrapper.radio-field label"
    )
    collissimo_label = None
    for label in labels:
        if "collissimo" in label.text.lower():
            collissimo_label = label
            break
    assert collissimo_label is not None, "Label 'collissimo' introuvable"
    driver.execute_script("arguments[0].scrollIntoView(true);", collissimo_label)
    time.sleep(0.5)
    collissimo_label.click()
    print("Selected Collissimo shipping method via label")

    # Cliquer sur Continue to payment
    continue_payment_buttons = driver.find_elements(
        By.CSS_SELECTOR, "button[type='submit'].button.primary"
    )
    continue_payment = None
    for btn in continue_payment_buttons:
        spans = btn.find_elements(By.TAG_NAME, "span")
        for span in spans:
            if span.text.strip().lower() == "continue to payment":
                continue_payment = btn
                break
        if continue_payment:
            break
    assert continue_payment is not None, "Bouton 'Continue to payment' introuvable"
    driver.execute_script("arguments[0].scrollIntoView(true);", continue_payment)
    continue_payment.click()
    print("Clicked 'Continue to payment'")

    # Vérifier que nous sommes toujours sur la même page
    current_url = driver.current_url
    print(f"Current URL after clicking Continue to payment: {current_url}")

    # Attendre que le bloc de paiement apparaisse sur la page
    try:
        # Attendre que le bloc de paiement soit visible
        payment_block = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div.divide-y.border.rounded.border-divider.px-8.mb-8",
                )
            )
        )
        assert payment_block.is_displayed(), "Le bloc de paiement doit être visible"
        print("Le bloc de paiement est visible")

        # Cliquer sur le lien Stripe (le deuxième lien dans le bloc payment-method-list)
        stripe_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.payment-method-list:nth-child(2) a[href='#']")
            )
        )
        stripe_link.click()
        print("Cliqué sur le lien Stripe")
        # Attendre et cliquer sur le bouton "Test success"
        test_success_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.button.interactive.outline")
            )
        )
        assert "Test success" in test_success_btn.text
        print("Bouton 'Test success' trouvé")
        test_success_btn.click()
        print("Cliqué sur le bouton 'Test success'")

        # Attendre que l'iframe Stripe soit disponible
        stripe_iframe = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "iframe[name^='__privateStripeFrame']")
            )
        )
        driver.switch_to.frame(stripe_iframe)
        print("Entré dans l'iframe Stripe")

        # Remplir les champs de carte avec WebDriverWait
        card_number_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='number']"))
        )
        card_number_input.send_keys("4242 4242 4242 4242")
        print("Numéro de carte entré")

        expiry_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='expiry']"))
        )
        expiry_input.send_keys("04/26")
        print("Date d'expiration entrée")

        cvc_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='cvc']"))
        )
        cvc_input.send_keys("242")
        print("CVC entré")

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Field-linkEmailInput"))
        )
        email_input.clear()
        email_input.send_keys("test@example.com")

        # 2. Remplir le téléphone
        phone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Field-linkMobilePhoneInput"))
        )
        phone_input.clear()
        phone_input.send_keys("0612345678")

        # 3. Remplir le nom/prénom
        name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Field-linkLegalNameInput"))
        )
        name_input.clear()
        name_input.send_keys("Jean Dupont")
        
        driver.switch_to.default_content()

        form_submit_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.form-submit-button"))
        )
        
        place_order_btn = WebDriverWait(form_submit_div, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-submit-button > .button"))
        )
        place_order_btn.click()
        print("Cliqué sur 'Place Order'")

        # Attendre que le message de confirmation apparaisse
        confirmation_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h3.thank-you"))
        )
        assert "Thank you" in confirmation_element.text
        print("Message de confirmation trouvé :", confirmation_element.text)

    except Exception as e:
        print(f"Erreur lors de la vérification du bloc de paiement: {str(e)}")
        # Afficher le HTML de la page pour debug
        print("Page HTML:")
        print(driver.page_source)
        raise
