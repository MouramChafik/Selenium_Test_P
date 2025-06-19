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
DASHBOARD_URL = f"{BASE_URL}/admin"
LOGIN_URL = f"{BASE_URL}/admin/login"
PRODUCTS_URL = f"{BASE_URL}/admin/products"
NEW_PRODUCT_URL = f"{BASE_URL}/admin/products/new"
CATEGORIES_URL = f"{BASE_URL}/admin/categories"
COLLECTIONS_URL = f"{BASE_URL}/admin/collections"
ATTRIBUTES_URL = f"{BASE_URL}/admin/attributes"
ORDERS_URL = f"{BASE_URL}/admin/orders"
CUSTOMERS_URL = f"{BASE_URL}/admin/customers"
COUPONS_URL = f"{BASE_URL}/admin/coupons"
NEW_COUPON_URL = f"{BASE_URL}/admin/coupon/new"
PAGES_URL = f"{BASE_URL}/admin/pages"
WIDGETS_URL = f"{BASE_URL}/admin/widgets"
SETTINGS_URL = f"{BASE_URL}/admin/setting/store"

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

# Description Editor Selectors
DESCRIPTION_EDITOR = "div.editor.form-field-container"
DESCRIPTION_ROWS = "div#rows"
DESCRIPTION_TEMPLATES = "div.row-templates"
DESCRIPTION_TEMPLATE_LINKS = "div.row-templates a"
DESCRIPTION_INPUT = "input#description"

# Wait times
WAIT_TIME = 2  # seconds to wait between actions

# Navbar Selectors
NAVBAR = "div.admin-navigation"
NAV_ITEMS = "li.nav-item a"
ROOT_NAV_ITEMS = "li.root-nav-item"
ROOT_LABELS = "div.root-label span"

# Page Title Selectors
PAGE_TITLE = "h1.page-heading-title"

# Dashboard Statistics Selectors
SALES_STATS_CARD = "div.card.shadow"
SALES_STATS_TITLE = "h2.card-title"
SALES_STATS_PERIODS = "div.card-action a.text-interactive"
SALES_STATS_CHART = "div.recharts-responsive-container"
SALES_STATS_CHART_SVG = "svg.recharts-surface"
SALES_STATS_CHART_AREA = "path.recharts-curve.recharts-area-area"
SALES_STATS_CHART_LINE = "path.recharts-curve.recharts-area-curve"
SALES_STATS_CHART_TOOLTIP = "div.recharts-tooltip-wrapper"
SALES_STATS_CHART_PIE = "g.recharts-layer.recharts-pie"
SALES_STATS_CHART_SECTORS = "path.recharts-sector"
SALES_STATS_CHART_LABELS = "text.recharts-text.recharts-pie-label-text"

# Admin Navigation
ADMIN_NAVIGATION = "div.admin-navigation"
CATEGORIES_LINK = "a[href*='categories']"
NEW_CATEGORY_BUTTON = "a[href*='/admin/categories/new']"

# Category Form Elements
CATEGORY_NAME_INPUT = "input[name='name']"
CATEGORY_SKU_INPUT = "input[name='sku']"
CATEGORY_SELECT_BUTTON = "a.text-interactive"
CATEGORY_TREE = "ul.category-tree"
CATEGORY_TREE_ITEMS = "ul.category-tree li"
CATEGORY_TEMPLATES = "div.row-templates"
CATEGORY_URL_KEY = "input[name='url_key']"
CATEGORY_META_TITLE = "input[name='meta_title']"
CATEGORY_META_KEYWORDS = "input[name='meta_keywords']"
CATEGORY_META_DESCRIPTION = "textarea[name='meta_description']"
CATEGORY_ADD_IMAGE = "button.button.default"
CATEGORY_STATUS_ENABLED = "input[name='status'][value='1']"
CATEGORY_INCLUDE_IN_NAV_RADIO = "input[name='include_in_nav'][value='1']"
CATEGORY_SHOW_PRODUCTS = "input[name='show_products'][value='1']"
CATEGORY_CANCEL_BUTTON = "button.button.critical.outline"
CATEGORY_SAVE_BUTTON = "button.button.primary"

# URLs
NEW_CATEGORY_URL = f"{BASE_URL}/admin/categories/new"

# Orders Navigation
ORDERS_LINK = "a[href*='/admin/orders']"
ORDERS_TITLE = "h1.page-heading-title"

# Orders Table and Status
ORDERS_TABLE = "table.listing.sticky"
ORDER_DELIVERED = "span.success.badge span.self-center.title"
ORDER_PAID = "span.success.badge span.self-center.title"
ORDER_NUMBER_LINK = "a.hover\\:underline.font-semibold"
ORDER_EDIT_TITLE = "h1.page-heading-title"
ORDER_COMPLETED_BADGE = "span.success.badge span.self-center.title"
ORDER_BACK_BUTTON = "a.breadcrum-icon"

# Shopping selectors
FEATURED_PRODUCTS_TITLE = "h3.mt-12.mb-12.text-center.uppercase.h5.tracking-widest"
PRODUCTS_GRID = "div.grid.grid-cols-2.md\\:grid-cols-4.gap-8"
PRODUCT_LINK = "div.product-name.product-list-name.mt-4.mb-1 a"
ADD_TO_CART_BUTTON = "button.button.primary.outline"
MINI_CART_TOAST = "div.toast-mini-cart"
MINI_CART_TITLE = "div.top-head.grid.grid-cols-2 div.self-center"
MINI_CART_ITEM_NAME = "div.item-info div.name span.font-bold"
MINI_CART_ITEM_QTY = "div.item-info div:nth-child(2)"
VIEW_CART_BUTTON = "a.add-cart-popup-button"
CONTINUE_SHOPPING_LINK = "a.add-cart-popup-continue"

# URLs
HOME_URL = "http://localhost:3000/"
CART_URL = "http://localhost:3000/cart"

# Category Edit selectors
CATEGORIES_TABLE = "table.listing.sticky"
CATEGORY_ROW = "tbody > tr"
CATEGORY_NAME_LINK = "td > div > a.hover\\:underline.font-semibold"
CATEGORY_EDIT_TITLE = "h1.page-heading-title"

# Category form selectors
CATEGORY_NAME_INPUT = "input[name='name']"
CATEGORY_SKU_INPUT = "input[name='sku']"
CATEGORY_URL_KEY_INPUT = "input[name='url_key']"
CATEGORY_META_TITLE_INPUT = "input[name='meta_title']"
CATEGORY_META_KEYWORDS_INPUT = "input[name='meta_keywords']"
CATEGORY_META_DESCRIPTION_INPUT = "textarea[name='meta_description']"
CATEGORY_STATUS_RADIO = "input[name='status'][value='1']"
CATEGORY_INCLUDE_IN_NAV_RADIO = "input[name='include_in_nav'][value='1']"
CATEGORY_SHOW_PRODUCTS_RADIO = "input[name='show_products'][value='1']"
CATEGORY_SAVE_BUTTON = "button.button.primary"

# Product navigation selectors
ADMIN_NAV_CONTAINER = ".admin-nav-container"
PRODUCTS_LINK = ".admin-nav-container li.nav-item a"
PRODUCTS_TABLE = "table.listing.sticky"
PRODUCT_NAME_LINK = "td > div > a.hover\\:underline.font-semibold"
PRODUCT_EDIT_TITLE = "h1.page-heading-title"

# Product form selectors
PRODUCT_NAME_INPUT = "input[name='name']"
PRODUCT_SKU_INPUT = "input[name='sku']"
PRODUCT_PRICE_INPUT = "input[name='price']"
PRODUCT_STOCK_INPUT = "input[name='stock']"
PRODUCT_DESCRIPTION_INPUT = "textarea[name='description']"
PRODUCT_STATUS_RADIO = "input[name='status'][value='1']"
PRODUCT_SAVE_BUTTON = "button.button.primary"

# Product deletion selectors
PRODUCT_CHECKBOX = "input[type='checkbox']"
PRODUCT_SELECTED_COUNT = "a.font-semibold:first-child"
PRODUCT_DELETE_BUTTON = "a.font-semibold:nth-child(4)"
DELETE_CONFIRM_BUTTON = "button.button.critical"
DELETE_CANCEL_BUTTON = "button.button.primary"

# Category Delete Selectors
CATEGORY_TABLE = "table.listing.sticky"
CATEGORY_ROW = "tbody > tr"
CATEGORY_CHECKBOX_CONTAINER = "td:first-child"
CATEGORY_CHECKBOX = "input[type='checkbox']"
CATEGORY_SELECTED_COUNT = "a.font-semibold:first-child"
CATEGORY_DELETE_BUTTON = "a.font-semibold:nth-child(2)"
DELETE_MODAL = "div.modal-overlay.fadeIn"
DELETE_MODAL_TITLE = "h2.card-title"
DELETE_CONFIRM_BUTTON = "button.button.critical"
DELETE_CANCEL_BUTTON = "button.button.primary"
CATEGORY_NAME_LINK = "a.hover\\:underline.font-semibold"


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
