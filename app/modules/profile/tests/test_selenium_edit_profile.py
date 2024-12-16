# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class TestTestseleniumeditprofile():

    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_testseleniumeditprofile(self):
        self.driver.get("http://localhost:5000/")
        self.driver.set_window_size(1920, 1102)
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(1)").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        self.driver.find_element(By.CSS_SELECTOR, ".sidebar-item:nth-child(9) .align-middle:nth-child(2)").click()
        self.driver.find_element(By.ID, "surname").click()
        self.driver.find_element(By.ID, "surname").click()
        element = self.driver.find_element(By.ID, "surname")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.ID, "developer_checkbox").click()
        self.driver.find_element(By.ID, "github_user").click()
        self.driver.find_element(By.ID, "github_user").send_keys("JohnDoe")
        self.driver.find_element(By.ID, "submit").click()
        self.driver.find_element(By.LINK_TEXT, "Edit profile").click()
        self.driver.find_element(By.ID, "developer_checkbox").click()
        self.driver.find_element(By.ID, "submit").click()