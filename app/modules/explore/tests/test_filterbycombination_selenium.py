# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from core.selenium.common import initialize_driver

class TestFilterbycombination():
  def setup_method(self, method):
    self.driver = initialize_driver()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_filterbycombination(self):
    self.driver.get("http://127.0.0.1:5000/")
    time.sleep(1)
    self.driver.set_window_size(1854, 1048)
    time.sleep(1)
    self.driver.find_element(By.LINK_TEXT, "Explore").click()
    self.driver.find_element(By.ID, "number_of_models").click()
    self.driver.find_element(By.ID, "number_of_models").send_keys("5")
    self.driver.find_element(By.ID, "number_of_features").send_keys("50")
    self.driver.find_element(By.ID, "number_of_features").send_keys(Keys.DOWN)
    self.driver.find_element(By.ID, "number_of_features").send_keys("49")
    self.driver.find_element(By.ID, "number_of_features").send_keys(Keys.UP)
    self.driver.find_element(By.ID, "number_of_features").send_keys("50")
    self.driver.find_element(By.ID, "number_of_features").send_keys(Keys.UP)
    self.driver.find_element(By.ID, "number_of_features").send_keys("51")
    self.driver.find_element(By.ID, "number_of_features").send_keys(Keys.DOWN)
    self.driver.find_element(By.ID, "number_of_features").send_keys("50")
    self.driver.find_element(By.ID, "number_of_models").click()
    self.driver.find_element(By.ID, "number_of_models").send_keys(Keys.DOWN)
    self.driver.find_element(By.ID, "number_of_models").send_keys("4")
    self.driver.find_element(By.ID, "number_of_models").send_keys(Keys.UP)
    self.driver.find_element(By.ID, "number_of_models").send_keys("5")
    self.driver.find_element(By.ID, "number_of_models").send_keys(Keys.UP)
    self.driver.find_element(By.ID, "number_of_models").send_keys("6")
    self.driver.find_element(By.ID, "number_of_features").click()
    self.driver.find_element(By.ID, "number_of_features").send_keys(Keys.DOWN)
    self.driver.find_element(By.ID, "number_of_features").send_keys("49")
    self.driver.find_element(By.ID, "number_of_features").send_keys(Keys.UP)
    self.driver.find_element(By.ID, "number_of_features").send_keys("50")
    self.driver.find_element(By.ID, "number_of_features").send_keys(Keys.UP)
    self.driver.find_element(By.ID, "number_of_features").send_keys("51")
  