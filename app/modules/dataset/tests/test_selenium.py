import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver
from selenium import webdriver


def wait_for_page_to_load(driver, timeout=4):
    WebDriverWait(driver, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )


def count_datasets(driver, host):
    driver.get(f"{host}/dataset/list")
    wait_for_page_to_load(driver)

    try:
        amount_datasets = len(driver.find_elements(By.XPATH, "//table//tbody//tr"))
    except Exception:
        amount_datasets = 0
    return amount_datasets


def test_upload_dataset():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")

        # Send the form
        password_field.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        # Count initial datasets
        initial_datasets = count_datasets(driver, host)

        # Open the upload dataset
        driver.get(f"{host}/dataset/upload")
        wait_for_page_to_load(driver)

        # Find basic info and UVL model and fill values
        title_field = driver.find_element(By.NAME, "title")
        title_field.send_keys("Title")
        desc_field = driver.find_element(By.NAME, "desc")
        desc_field.send_keys("Description")
        tags_field = driver.find_element(By.NAME, "tags")
        tags_field.send_keys("tag1,tag2")

        # Add two authors and fill
        add_author_button = driver.find_element(By.ID, "add_author")
        add_author_button.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)
        add_author_button.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        name_field0 = driver.find_element(By.NAME, "authors-0-name")
        name_field0.send_keys("Author0")
        affiliation_field0 = driver.find_element(By.NAME, "authors-0-affiliation")
        affiliation_field0.send_keys("Club0")
        orcid_field0 = driver.find_element(By.NAME, "authors-0-orcid")
        orcid_field0.send_keys("0000-0000-0000-0000")

        name_field1 = driver.find_element(By.NAME, "authors-1-name")
        name_field1.send_keys("Author1")
        affiliation_field1 = driver.find_element(By.NAME, "authors-1-affiliation")
        affiliation_field1.send_keys("Club1")

        # Obtén las rutas absolutas de los archivos
        file1_path = os.path.abspath("app/modules/dataset/uvl_examples/file1.uvl")
        file2_path = os.path.abspath("app/modules/dataset/uvl_examples/file2.uvl")

        # Subir el primer archivo
        dropzone = driver.find_element(By.CLASS_NAME, "dz-hidden-input")
        dropzone.send_keys(file1_path)
        wait_for_page_to_load(driver)

        # Subir el segundo archivo
        dropzone = driver.find_element(By.CLASS_NAME, "dz-hidden-input")
        dropzone.send_keys(file2_path)
        wait_for_page_to_load(driver)

        # Add authors in UVL models
        show_button = driver.find_element(By.ID, "0_button")
        show_button.send_keys(Keys.RETURN)
        add_author_uvl_button = driver.find_element(By.ID, "0_form_authors_button")
        add_author_uvl_button.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        name_field = driver.find_element(By.NAME, "feature_models-0-authors-2-name")
        name_field.send_keys("Author3")
        affiliation_field = driver.find_element(By.NAME, "feature_models-0-authors-2-affiliation")
        affiliation_field.send_keys("Club3")

        # Check I agree and send form
        check = driver.find_element(By.ID, "agreeCheckbox")
        check.send_keys(Keys.SPACE)
        wait_for_page_to_load(driver)
        time.sleep(2)  # Force wait time

        upload_btn = driver.find_element(By.ID, "upload_button")
        upload_btn.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)
        time.sleep(7)

        assert driver.current_url == f"{host}/dataset/list", "Test failed!"

        # Count final datasets
        final_datasets = count_datasets(driver, host)
        assert final_datasets == initial_datasets + 1, "Test failed!"

        print("Test passed!")

    finally:

        # Close the browser
        close_driver(driver)


def test_download_dataset_glencoe():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")

        # Send the form
        password_field.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        # Open the dataset list page
        driver.get(f"{host}/dataset/list")
        wait_for_page_to_load(driver)

        # Click on the first dataset in the list
        first_dataset = driver.find_element(By.XPATH, "//table//tbody//tr[1]//td[1]//a")
        first_dataset.click()
        wait_for_page_to_load(driver)

        # Click the dropdown to reveal the download all button

        dropdown = driver.find_element(By.ID, "btnGroupDonwloadAll")
        driver.execute_script("arguments[0].click();", dropdown)

        wait_for_page_to_load(driver)

        download_all_button = driver.find_element(By.ID, "download-glencoe")
        driver.execute_script("arguments[0].click();", download_all_button)
        wait_for_page_to_load(driver)
        time.sleep(2)  # Force wait time

        print("Download one dataset in Glencoe test passed!")

    finally:
        # Close the browser
        close_driver(driver)


def test_download_dataset_DIMACS():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")

        # Send the form
        password_field.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        # Open the dataset list page
        driver.get(f"{host}/dataset/list")
        wait_for_page_to_load(driver)

        # Click on the first dataset in the list
        first_dataset = driver.find_element(By.XPATH, "//table//tbody//tr[1]//td[1]//a")
        first_dataset.click()
        wait_for_page_to_load(driver)

        # Click the dropdown to reveal the download all button

        dropdown = driver.find_element(By.ID, "btnGroupDonwloadAll")
        driver.execute_script("arguments[0].click();", dropdown)

        wait_for_page_to_load(driver)

        download_all_button = driver.find_element(By.ID, "download-DIMACS")
        driver.execute_script("arguments[0].click();", download_all_button)
        wait_for_page_to_load(driver)
        time.sleep(2)  # Force wait time
        print("Download one dataset in DIMACS test passed!")

    finally:
        # Close the browser
        close_driver(driver)


def test_download_dataset_splot():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")

        # Send the form
        password_field.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        # Open the dataset list page
        driver.get(f"{host}/dataset/list")
        wait_for_page_to_load(driver)

        # Click on the first dataset in the list
        first_dataset = driver.find_element(By.XPATH, "//table//tbody//tr[1]//td[1]//a")
        first_dataset.click()
        wait_for_page_to_load(driver)

        # Click the dropdown to reveal the download all button

        dropdown = driver.find_element(By.ID, "btnGroupDonwloadAll")
        driver.execute_script("arguments[0].click();", dropdown)

        wait_for_page_to_load(driver)

        download_all_button = driver.find_element(By.ID, "download-splot")
        driver.execute_script("arguments[0].click();", download_all_button)
        wait_for_page_to_load(driver)
        time.sleep(2)  # Force wait time

        print("Download one dataset in Splot test passed!")

    finally:
        # Close the browser
        close_driver(driver)


def test_export_file_glencoe():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")

        # Send the form
        password_field.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        # Open the dataset list page
        driver.get(f"{host}/dataset/list")
        wait_for_page_to_load(driver)

        # Click on the first dataset in the list
        first_dataset = driver.find_element(By.XPATH, "//table//tbody//tr[1]//td[1]//a")
        first_dataset.click()
        wait_for_page_to_load(driver)

        # Click the dropdown to reveal the export button for the first file
        dropdown = driver.find_element(By.XPATH,
                                       "//div[@class='list-group-item']//button[contains(@id, 'btnGroupDropExport')]")
        driver.execute_script("arguments[0].click();", dropdown)
        wait_for_page_to_load(driver)

        # Click the export button for DIMACS for the first file
        export_button = driver.find_element(By.XPATH, "//div[@class='list-group-item']//a[@id='export-Glencoe']")
        driver.execute_script("arguments[0].click();", export_button)
        wait_for_page_to_load(driver)

        print("Export file to Glencoe test passed!")

    finally:
        # Close the browser
        close_driver(driver)


def test_export_file_splot():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")

        # Send the form
        password_field.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        # Open the dataset list page
        driver.get(f"{host}/dataset/list")
        wait_for_page_to_load(driver)

        # Click on the first dataset in the list
        first_dataset = driver.find_element(By.XPATH, "//table//tbody//tr[1]//td[1]//a")
        first_dataset.click()
        wait_for_page_to_load(driver)

        # Click the dropdown to reveal the export button for the first file
        dropdown = driver.find_element(By.XPATH,
                                       "//div[@class='list-group-item']//button[contains(@id, 'btnGroupDropExport')]")
        driver.execute_script("arguments[0].click();", dropdown)
        wait_for_page_to_load(driver)

        # Click the export button for DIMACS for the first file
        export_button = driver.find_element(By.XPATH,
                                            "//div[@class='list-group-item']//a[@id='export-SPLOT']")
        driver.execute_script("arguments[0].click();", export_button)
        wait_for_page_to_load(driver)

        print("Export file to Splot test passed!")

    finally:
        # Close the browser
        close_driver(driver)


def test_export_file_DIMACS():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")

        # Send the form
        password_field.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        # Open the dataset list page
        driver.get(f"{host}/dataset/list")
        wait_for_page_to_load(driver)

        # Click on the first dataset in the list
        first_dataset = driver.find_element(By.XPATH, "//table//tbody//tr[1]//td[1]//a")
        first_dataset.click()
        wait_for_page_to_load(driver)

        # Click the dropdown to reveal the export button for the first file
        dropdown = driver.find_element(By.XPATH,
                                       "//div[@class='list-group-item']//button[contains(@id, 'btnGroupDropExport')]")
        driver.execute_script("arguments[0].click();", dropdown)
        wait_for_page_to_load(driver)

        # Click the export button for DIMACS for the first file
        export_button = driver.find_element(By.XPATH, "//div[@class='list-group-item']//a[@id='export-DIMACS']")
        driver.execute_script("arguments[0].click();", export_button)
        wait_for_page_to_load(driver)

        print("Export file to DIMACS test passed!")

    finally:
        # Close the browser
        close_driver(driver)


def test_download_all_datasets():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")

        # Send the form
        password_field.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        button = driver.find_element(By.ID, "downloadAll")
        driver.execute_script("arguments[0].click();", button)

        wait_for_page_to_load(driver)
        time.sleep(2)  # Force wait time

        print("Download all datasets test passed!")

    finally:
        # Close the browser
        close_driver(driver)


def test_download_all_datasets_no_logged():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000/")  # Open the website
    time.sleep(2)  # Force wait time

    try:
        download_button = driver.find_element(By.ID, "downloadAll")
        download_button.click()
    except Exception as e:
        print("Error al encontrar el botón:", e)
        driver.quit()
        return

    time.sleep(2)  # Force wait time

    # Check if the user is redirected to the login page
    current_url = driver.current_url
    assert "login" in current_url, f"Se esperaba redirigir a login, pero la URL es {current_url}"

    print("Download all datasets no logged test passed!")

    # Close the browser
    driver.quit()


# Call the test function

test_upload_dataset()
test_download_all_datasets()
test_download_all_datasets_no_logged()
test_download_dataset_glencoe()
test_download_dataset_DIMACS()
test_download_dataset_splot()
test_export_file_DIMACS()
test_export_file_glencoe()
test_export_file_splot()
