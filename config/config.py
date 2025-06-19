from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Login credentials
EMAIL = "chafikdev23@gmail.com"
PASSWORD = "Chafikdev23"

# URLs
BASE_URL = "http://localhost:3000"
ADMIN_URL = f"{BASE_URL}/admin"
LOGIN_URL = f"{BASE_URL}/admin/login"
PRODUCTS_URL = f"{BASE_URL}/admin/products"
NEW_PRODUCT_URL = f"{BASE_URL}/admin/products/new"

# Test Data
TEST_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "test_image.jpg")

# Login Selectors
EMAIL_INPUT = "input[name='email']"
PASSWORD_INPUT = "input[name='password']"
SUBMIT_BUTTON = "button.button.primary"
ERROR_MESSAGE = "div.text-critical"
DASHBOARD_TITLE = "h1.page-heading-title"

# Navigation Selectors
NEW_PRODUCT_LINK = "a[href*='/admin/products/new']"

# Product Form Selectors
PRODUCT_NAME = "input[name='name']"
PRODUCT_SKU = "input[name='sku']"
PRODUCT_PRICE = "input[name='price']"
PRODUCT_WEIGHT = "input[name='weight']"
CATEGORY_SELECT = "a.text-interactive"
CATEGORY_SEARCH = "input[placeholder='Search categories']"
CATEGORY_ITEM = "div.grid.grid-cols-8 button.button.secondary"
CATEGORY_CLOSE = "button.button.secondary"
PRODUCT_TAX_CLASS = "select[name='tax_class']"
PRODUCT_DESCRIPTION = "#description"
PRODUCT_URL_KEY = "input[name='url_key']"
PRODUCT_META_TITLE = "input[name='meta_title']"
PRODUCT_META_KEYWORDS = "input[name='meta_keywords']"
PRODUCT_META_DESCRIPTION = "textarea[name='meta_description']"
PRODUCT_STATUS_ENABLED = "input[name='status'][value='1']"
PRODUCT_VISIBILITY_VISIBLE = "input[name='visibility'][value='1']"
PRODUCT_MANAGE_STOCK = "input[name='manage_stock'][value='1']"
PRODUCT_STOCK_AVAILABILITY = "input[name='stock_availability'][value='1']"
PRODUCT_QUANTITY = "input[name='qty']"
PRODUCT_ATTRIBUTE_GROUP = "select[name='group_id']"
PRODUCT_COLOR = "select[name='attributes[0][value]']"
PRODUCT_SIZE = "select[name='attributes[1][value]']"
SAVE_PRODUCT_BUTTON = "button.button.primary"
CANCEL_BUTTON = "button.button.critical.outline"

# Image Upload Selectors
IMAGE_UPLOAD_INPUT = "input[type='file']"
IMAGE_UPLOAD_ICON = "div.uploader-icon"
IMAGE_LIST = "div.image-list"
IMAGE_PREVIEW = "div.image-list div.img img"
IMAGE_UPLOADER = "div.uploader"

# Wait times
WAIT_TIME = 1  # seconds to wait between actions

def get_driver():
    """Initialize and return a Chrome WebDriver instance"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    # Remove headless mode to make browser visible
    # chrome_options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
