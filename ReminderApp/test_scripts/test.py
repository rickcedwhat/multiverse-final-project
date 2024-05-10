from datetime import timedelta, datetime
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import open_and_get_dialog, post_reminder, put_reminder, get_random_reminder, get_reminder_by_id, get_date_from_now, format_datetime, parse_datetime, parse_reminders, parse_reminder, backup_and_drop, seed_reminders
from datetime import datetime

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

seed = [
    {"message": "Reminder 1", "email": "ccata002@gmail.com", "datetime": "2025-01-01T12:00:00", "phone": "1234567890"},
    {"message": "Reminder 2", "email": "ccata002@gmail.com", "datetime": "2025-01-02T12:00:00", "phone": "0987654321"}
]

# before every test, drop all reminders
@pytest.fixture(autouse=True)
def drop_reminders():
    table = backup_and_drop()
    seed_reminders(seed)
    yield
    seed_reminders(table)


def test_default_values(wait):
    dialog = open_and_get_dialog(wait,"//button[normalize-space()='Add Reminder']")
    inputs = dialog["inputs"]

    input_message = inputs["message"]
    input_email = inputs["email"]
    input_datetime = inputs["datetime"]
    input_phone = inputs["phone"]

    # Check default values of input elements
    assert input_message.get_attribute("value") == "New Reminder"
    assert input_email.get_attribute("value") == "ccata002@gmail.com"
    # assert input_datetime.get_attribute("value") == (datetime.now() + timedelta(hours=1)).strftime("%m/%d/%Y %I:%M %p")
    assert input_datetime.get_attribute("value") == format_datetime(get_date_from_now(1/24),False)
    assert input_phone.get_attribute("value") == "7864400382"


def test_required_fields(wait):

    reminder = {
        "message": "",
        "email": "",
        "datetime": "",
        "phone": ""
    }
    dialog = post_reminder(wait,reminder)

    inputs = dialog["inputs"]
    input_message = inputs["message"]
    input_email = inputs["email"]
    input_datetime = inputs["datetime"]
    input_phone = inputs["phone"]

    assert input_message.get_attribute("value") == ""
    assert input_email.get_attribute("value") == ""
    assert input_datetime.get_attribute("value") == ""
    assert input_phone.get_attribute("value") == ""

    submit_button = dialog["buttons"]["SUBMIT"]
    submit_button.click()

    for input_name in inputs:
        helper_text = dialog["get_helper_text"](input_name)
        assert helper_text.text == f"{input_name.capitalize()} is required"

def test_field_validation(wait):
    dialog = open_and_get_dialog(wait,"//button[normalize-space()='Add Reminder']")

    inputs = dialog["inputs"]
    input_email = inputs["email"]
    input_phone = inputs["phone"]

    # Fill in email and phone fields with invalid values
    input_email.send_keys("invalidemail")
    input_phone.send_keys("123")

    # Find submit button in dialog
    submit_button = dialog["buttons"]["SUBMIT"]
    submit_button.click()

def test_add_reminder(wait):
    three_days_from_now = format_datetime(get_date_from_now(3),False)
    reminder = {
        "message": "New Reminder from pytest",
        "email": "fake@test.com",
        "datetime": three_days_from_now,
        "phone": "1234567890"
    }

    dialog = post_reminder(wait,reminder)

    assert wait.until(EC.staleness_of(dialog["self"])) == True

    reminders = parse_reminders(wait)
    lastReminder = reminders[-1]
    print(lastReminder,reminder)

    assert lastReminder["message"] == reminder["message"]
    assert lastReminder["email"] == reminder["email"]
    assert parse_datetime(lastReminder["datetime"]) == parse_datetime(reminder["datetime"],False)
    assert lastReminder["phone"] == reminder["phone"]

def test_edit_reminder(wait):
    four_days_from_now = format_datetime(get_date_from_now(4),False)
    reminder = {
        "message": "Updated Reminder from pytest",
        "email": "ccata003@gmail.com",
        "datetime": four_days_from_now,
        "phone": "7864400383"
    }

    id = get_random_reminder(wait)["id"]

    dialog = put_reminder(wait,reminder,id)

    assert wait.until(EC.staleness_of(dialog["self"])) == True

    updatedReminder = parse_reminder(wait,id)
    print(updatedReminder,reminder)

    assert updatedReminder["message"] == reminder["message"]
    assert updatedReminder["email"] == reminder["email"]
    # assert updatedReminder["datetime"].strftime("%m/%d/%Y %I:%M %p") == reminder["datetime"]
    assert parse_datetime(updatedReminder["datetime"]) == parse_datetime(reminder["datetime"],False)
    assert updatedReminder["phone"] == reminder["phone"]

def test_cancellable_dialog(wait):
    dialog = open_and_get_dialog(wait,"//button[normalize-space()='Delete All']")
    
    if dialog == None:
        pytest.skip("No reminders available to delete")

    assert dialog["self"].find_element(By.XPATH,"//h2[normalize-space()='Confirmation']")
    assert dialog["self"].find_element(By.XPATH,"//p[normalize-space()='Are you sure you want to delete all reminders?']")

    # print all the keys in the dialog button dictionary
    print(dialog["buttons"].keys()) 

    dialog["buttons"]["CANCEL"].click()

    # dialog should no longer be visible
    assert wait.until(EC.staleness_of(dialog["self"])) == True

    dialog = open_and_get_dialog(wait,"//button[normalize-space()='Delete']")

    assert dialog["self"].find_element(By.XPATH,"//h2[normalize-space()='Confirmation']")
    assert dialog["self"].find_element(By.XPATH,"//p[normalize-space()='Are you sure you want to delete this reminder?']")

    dialog["buttons"]["CANCEL"].click()

    # dialog should no longer be visible
    assert wait.until(EC.staleness_of(dialog["self"])) == True

def test_delete_reminder(wait):
    # delete button should open confirmation dialog
    id = get_random_reminder(wait)["id"]

    if id == None:
        pytest.skip("No reminders available to delete")

    dialog = open_and_get_dialog(wait,f"//div[@data-id='reminder-{id}']//button[normalize-space()='Delete']")

    assert dialog["text"]["title"] == "Confirmation"
    assert "Are you sure you want to delete this reminder?" in dialog["text"]["content"]

    dialog["buttons"]["CONFIRM DELETION"].click()

    deleted_reminder = get_reminder_by_id(wait,id)

    assert deleted_reminder == None

def test_delete_all(wait):
    dialog = open_and_get_dialog(wait,"//button[normalize-space()='Delete All']")

    if dialog == None:
        pytest.skip("No reminders available to delete")

    assert dialog["text"]["title"] == "Confirmation"
    assert "Are you sure you want to delete all reminders?" in dialog["text"]["content"]

    dialog["buttons"]["CONFIRM DELETION"].click()

    # wait for reminders to be deleted
    reminders = parse_reminders(wait,True)

    assert len(reminders) == 0
