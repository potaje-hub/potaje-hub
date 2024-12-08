# Generated by Selenium IDE
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from core.selenium.common import initialize_driver


class TestFilterbynumberoffeatures():
    def setup_method(self, method):
        self.driver = initialize_driver()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_filterbynumberoffeatures(self):
        self.driver.get("http://127.0.0.1:5000/")
        time.sleep(1)
        self.driver.set_window_size(1854, 1048)
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Explore").click()
        self.driver.find_element(By.ID, "number_of_features").click()
        self.driver.find_element(By.ID, "number_of_features").send_keys("50")
        self.driver.find_element(By.ID, "number_of_features").send_keys(Keys.DOWN)
        self.driver.find_element(By.ID, "number_of_features").send_keys("49")
        self.driver.find_element(By.ID, "number_of_features").send_keys(Keys.UP)
        self.driver.find_element(By.ID, "number_of_features").send_keys("50")
        self.driver.find_element(By.ID, "number_of_features").send_keys(Keys.UP)
        self.driver.find_element(By.ID, "number_of_features").send_keys("51")