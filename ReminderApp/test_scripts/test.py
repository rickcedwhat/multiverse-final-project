from datetime import timedelta, datetime
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import open_and_get_dialog, post_reminder, put_reminder, get_reminders
import random


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



def test_default_values(driver,wait):
    dialog = open_and_get_dialog(driver,wait,"//button[normalize-space()='Add Reminder']")
    inputs = dialog["inputs"]

    input_message = inputs["message"]
    input_email = inputs["email"]
    input_datetime = inputs["datetime"]
    input_phone = inputs["phone"]

    # Check default values of input elements
    assert input_message.get_attribute("value") == "New Reminder"
    assert input_email.get_attribute("value") == "ccata002@gmail.com"
    assert input_datetime.get_attribute("value") == (datetime.now() + timedelta(hours=1)).strftime("%m/%d/%Y %I:%M %p")
    assert input_phone.get_attribute("value") == "7864400382"


def test_required_fields(driver,wait):
    # dialog = open_add_reminder_dialog(driver,wait)
    # dialog = open_and_get_dialog(driver,wait,"//button[normalize-space()='Add Reminder']")

    reminder = {
        "message": "",
        "email": "",
        "datetime": "",
        "phone": ""
    }
    dialog = post_reminder(driver,wait,reminder)

    inputs = dialog["inputs"]
    input_message = inputs["message"]
    input_email = inputs["email"]
    input_datetime = inputs["datetime"]
    input_phone = inputs["phone"]

    # input_message.clear()
    # input_email.clear()
    # input_datetime.send_keys(Keys.CONTROL + "a")
    # input_datetime.send_keys(Keys.DELETE)
    # input_phone.clear()



    assert input_message.get_attribute("value") == ""
    assert input_email.get_attribute("value") == ""
    assert input_datetime.get_attribute("value") == ""
    assert input_phone.get_attribute("value") == ""

    submit_button = dialog["buttons"]["SUBMIT"]
    submit_button.click()

    for input_name in inputs:
        helper_text = dialog["get_helper_text"](input_name)
        assert helper_text.text == f"{input_name.capitalize()} is required"

def test_field_validation(driver,wait):
    dialog = open_and_get_dialog(driver,wait,"//button[normalize-space()='Add Reminder']")

    inputs = dialog["inputs"]
    input_email = inputs["email"]
    input_phone = inputs["phone"]

    # Fill in email and phone fields with invalid values
    input_email.send_keys("invalidemail")
    input_phone.send_keys("123")

    # Find submit button in dialog
    submit_button = dialog["buttons"]["SUBMIT"]
    submit_button.click()

def test_add_reminder(driver,wait):
    reminder = {
        "message": "New Reminder from pytest",
        "email": "fake@test.com",
        "datetime": "05/12/2024 11:59 PM",
        "phone": "1234567890"
    }

    dialog = post_reminder(driver,wait,reminder)

    assert wait.until(EC.staleness_of(dialog["self"])) == True

    reminders = get_reminders()
    lastReminder = reminders[-1]
    print(lastReminder,reminder)
    print(lastReminder["datetime"].strftime("%m/%d/%Y %I:%M %p"))

    assert lastReminder["message"] == reminder["message"]
    assert lastReminder["email"] == reminder["email"]
    assert lastReminder["datetime"].strftime("%m/%d/%Y %I:%M %p") == reminder["datetime"]
    assert lastReminder["phone"] == reminder["phone"]

def test_edit_reminder(driver,wait):
    reminder = {
        "message": "Updated Reminder from pytest",
        "email": "ccata003@gmail.com",
        "datetime": "01/01/2025 12:00 AM",
        "phone": "7864400383"
    }

    reminders = get_reminders()
    # get random index
    index = random.randint(0,len(reminders)-1)

    dialog = put_reminder(driver,wait,reminder,index)

    assert wait.until(EC.staleness_of(dialog["self"])) == True

    reminders = get_reminders()
    updatedReminder = reminders[index]
    print(updatedReminder,reminder)

    assert updatedReminder["message"] == reminder["message"]
    assert updatedReminder["email"] == reminder["email"]
    assert updatedReminder["datetime"].strftime("%m/%d/%Y %I:%M %p") == reminder["datetime"]
    assert updatedReminder["phone"] == reminder["phone"]
    
# test delete and deleteAll opens confirmation dialog
# test delete deletes reminder
# test deleteAll deletes all reminders