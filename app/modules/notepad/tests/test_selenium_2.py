# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from core.selenium.common import initialize_driver


class TestPruebas():
  def setup_method(self, method):

    self.driver = initialize_driver()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
    
  def test_list(self):
    self.driver.get("http://127.0.0.1:5000/login")
    self.driver.set_window_size(927, 1011)
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
    self.driver.find_element(By.ID, "password").send_keys("1234")
    self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
    self.driver.get("http://127.0.0.1:5000/notepad")
    
  def test_create(self):
    self.driver.get("http://127.0.0.1:5000/login")
    self.driver.set_window_size(927, 1011)
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
    self.driver.find_element(By.ID, "password").send_keys("1234")
    self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
    self.driver.get("http://127.0.0.1:5000/notepad/create")
    self.driver.find_element(By.ID, "title").click()
    self.driver.find_element(By.ID, "title").send_keys("prueba")
    self.driver.find_element(By.ID, "body").send_keys("pruebita")
    self.driver.find_element(By.ID, "submit").click()
  
  def test_update(self):
    self.driver.get("http://127.0.0.1:5000/login")
    self.driver.set_window_size(927, 1011)
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
    self.driver.find_element(By.ID, "password").send_keys("1234")
    self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
    self.driver.get("http://127.0.0.1:5000/notepad")
    self.driver.find_element(By.LINK_TEXT, "Edit").click()
    self.driver.find_element(By.ID, "body").click()
    self.driver.find_element(By.ID, "body").send_keys("pruebitaa")
    self.driver.find_element(By.ID, "submit").click()

    def test_delete(self):
        self.driver.get("http://127.0.0.1:5000/login")
        self.driver.set_window_size(927, 1011)
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
        self.driver.get("http://127.0.0.1:5000/notepad")
        self.driver.find_element(By.CSS_SELECTOR, "button").click()
