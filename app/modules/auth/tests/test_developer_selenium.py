# Generated by Selenium IDE
from selenium.webdriver.common.by import By
from core.selenium.common import initialize_driver


class TestTestdeveloperselenium():
    def setup_method(self, method):
        self.driver = initialize_driver()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_testdeveloperselenium(self):
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1850, 1011)
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
        self.driver.find_element(By.ID, "name").click()
        self.driver.find_element(By.ID, "name").send_keys("Test")
        self.driver.find_element(By.ID, "surname").click()
        self.driver.find_element(By.ID, "surname").send_keys("Developer")
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("testdeveloper@gmail.com")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("testdeveloper")
        self.driver.find_element(By.ID, "developer_checkbox").click()
        self.driver.find_element(By.ID, "github_user").click()
        self.driver.find_element(By.ID, "github_user").send_keys("developergithub")
        self.driver.find_element(By.ID, "submit").click()
        self.driver.close()
