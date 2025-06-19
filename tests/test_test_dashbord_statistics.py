import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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
    SALES_STATS_CARD,
    SALES_STATS_TITLE,
    SALES_STATS_PERIODS,
    SALES_STATS_CHART,
    SALES_STATS_CHART_SVG,
    SALES_STATS_CHART_AREA,
    SALES_STATS_CHART_LINE,
    SALES_STATS_CHART_LABELS
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

def test_sales_statistics_presence(driver):
    """Test that sales statistics card and its elements are present"""
    login(driver)
    print("\nCurrent URL:", driver.current_url)
    
    # Verify sales statistics card is present
    print("\nLooking for stats card with selector:", SALES_STATS_CARD)
    stats_card = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, SALES_STATS_CARD))
    )
    assert stats_card.is_displayed(), "Sales statistics card should be visible"
    print("Stats card found and visible")
    
    # Print the HTML of the stats card for debugging
    print("\nStats card HTML:", stats_card.get_attribute('outerHTML'))
    
    # Verify title
    print("\nLooking for title with selector:", SALES_STATS_TITLE)
    title = stats_card.find_element(By.CSS_SELECTOR, SALES_STATS_TITLE)
    assert title.text == "Sale Statistics", "Title should be 'Sale Statistics'"
    print("Title found:", title.text)
    
    # Verify period options
    print("\nLooking for periods with selector:", SALES_STATS_PERIODS)
    periods = stats_card.find_elements(By.CSS_SELECTOR, SALES_STATS_PERIODS)
    expected_periods = ["Daily", "Weekly", "Monthly"]
    assert len(periods) == len(expected_periods), f"Should have {len(expected_periods)} period options"
    for period in periods:
        assert period.text in expected_periods, f"Period {period.text} should be in {expected_periods}"
    print("Periods found:", [p.text for p in periods])
    
    # Verify chart is present
    print("\nLooking for chart with selector:", SALES_STATS_CHART)
    chart = stats_card.find_element(By.CSS_SELECTOR, SALES_STATS_CHART)
    assert chart.is_displayed(), "Chart should be visible"
    print("Chart found and visible")
    
    # Print the HTML of the chart for debugging
    print("\nChart HTML:", chart.get_attribute('outerHTML'))
    
    # Verify SVG and chart elements
    print("\nLooking for SVG with selector:", SALES_STATS_CHART_SVG)
    svg = chart.find_element(By.CSS_SELECTOR, SALES_STATS_CHART_SVG)
    assert svg.is_displayed(), "Chart SVG should be visible"
    print("SVG found and visible")
    
    # Print the HTML of the SVG for debugging
    print("\nSVG HTML:", svg.get_attribute('outerHTML'))
    
    # Verify area chart elements
    print("\nLooking for area chart with selector:", SALES_STATS_CHART_AREA)
    areas = svg.find_elements(By.CSS_SELECTOR, SALES_STATS_CHART_AREA)
    assert len(areas) > 0, "Should have areas in the chart"
    print("Found", len(areas), "areas")
    
    # Verify chart lines
    print("\nLooking for chart lines with selector:", SALES_STATS_CHART_LINE)
    lines = svg.find_elements(By.CSS_SELECTOR, SALES_STATS_CHART_LINE)
    assert len(lines) > 0, "Should have lines in the chart"
    print("Found", len(lines), "lines")

def test_sales_statistics_interaction(driver):
    """Test interaction with sales statistics chart"""
    login(driver)
    print("\nCurrent URL:", driver.current_url)
    
    # Find the chart
    print("\nLooking for stats card with selector:", SALES_STATS_CARD)
    stats_card = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, SALES_STATS_CARD))
    )
    print("Stats card found")
    
    # Test period switching
    print("\nLooking for periods with selector:", SALES_STATS_PERIODS)
    periods = driver.find_elements(By.CSS_SELECTOR, SALES_STATS_PERIODS)
    expected_periods = ["Daily", "Weekly", "Monthly"]
    print("Found", len(periods), "periods")
    
    chart = None
    for period in periods:
        if period.text not in expected_periods:
            continue
            
        print("\nClicking period:", period.text)
        period.click()
        time.sleep(WAIT_TIME * 2)  # Wait longer for chart to update
        
        # Wait for chart to be present and visible
        print("Looking for chart with selector:", SALES_STATS_CHART)
        chart = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SALES_STATS_CHART))
        )
        assert chart.is_displayed(), "Chart should be visible after period change"
        print("Chart found and visible")
        
        # Wait for SVG to be present and visible
        print("Looking for SVG with selector:", SALES_STATS_CHART_SVG)
        svg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SALES_STATS_CHART_SVG))
        )
        assert svg.is_displayed(), "Chart SVG should be visible after period change"
        print("SVG found and visible")
        
        # Verify area chart elements
        print("Looking for area chart with selector:", SALES_STATS_CHART_AREA)
        areas = svg.find_elements(By.CSS_SELECTOR, SALES_STATS_CHART_AREA)
        assert len(areas) > 0, "Should have areas in the chart after period change"
        print("Found", len(areas), "areas")
        
        # Verify chart lines
        print("Looking for chart lines with selector:", SALES_STATS_CHART_LINE)
        lines = svg.find_elements(By.CSS_SELECTOR, SALES_STATS_CHART_LINE)
        assert len(lines) > 0, "Should have lines in the chart after period change"
        print("Found", len(lines), "lines")
    
    if chart:
        # Test chart hover interaction
        print("\nTesting hover interaction")
        action = ActionChains(driver)
        action.move_to_element(chart).perform()
        time.sleep(WAIT_TIME)
        print("Hover completed")
