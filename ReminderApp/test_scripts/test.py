from datetime import timedelta, datetime
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get('http://localhost:5173')
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)

def open_add_reminder_dialog(driver,wait):

    # Find element that has text Add Reminder
    add_reminder = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Add Reminder']"))
    )

    # Click on the Add Reminder button
    add_reminder.click()

    # Find dialog element
    dialog = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
    )

    return dialog


def test_default_values(driver,wait):
    dialog = open_add_reminder_dialog(driver,wait)

    # Find input elements in dialog
    input_message = driver.find_element(By.XPATH,"//input[@name='message']")
    input_email = driver.find_element(By.XPATH,"//input[@name='email']")
    input_datetime = driver.find_element(By.XPATH,"//input[@name='datetime']")
    input_phone = driver.find_element(By.XPATH,"//input[@name='phone']")

    # Check default values of input elements
    assert input_message.get_attribute("value") == "New Reminder"
    assert input_email.get_attribute("value") == ""
    assert input_datetime.get_attribute("value") == (datetime.now() + timedelta(hours=1)).strftime("%m/%d/%Y %I:%M %p")
    assert input_phone.get_attribute("value") == ""


def test_required_fields(driver,wait):
    dialog = open_add_reminder_dialog(driver,wait)

    # Find submit button in dialog
    submit_button = driver.find_element(By.XPATH,"//button[text()='Submit']")

    # Click on submit button without filling in any fields
    submit_button.click()

    # Find input elements in dialog
    input_message = driver.find_element(By.XPATH,"//input[@name='message']")
    input_datetime = driver.find_element(By.XPATH,"//input[@name='datetime']")

    input_message.clear()
    input_datetime.clear()

    print("input_message.get_attribute('value')",input_message.get_attribute("value"))

    assert input_message.get_attribute("value") == ""
    # assert input_datetime.get_attribute("value") == ""
