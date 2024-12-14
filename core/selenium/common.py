from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def initialize_driver():
    # Initializes the browser options
    options = webdriver.ChromeOptions()

    # Initialise the browser using WebDriver Manager
    service = Service('core/selenium/chromedriver-linux64 (1)/chromedriver-linux64/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def close_driver(driver):
    driver.quit()
