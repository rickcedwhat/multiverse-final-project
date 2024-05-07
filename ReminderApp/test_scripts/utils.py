import pyodbc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime


conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=USLMACEATALAN2\MSSQLSERVER01;'
    r'DATABASE=Reminders2024;'
    r'Trusted_Connection=yes;'
)

def open_and_get_dialog(driver,wait,button_xpath):
    print("button_xpath",button_xpath)
    button = wait.until(
        EC.presence_of_element_located((By.XPATH, button_xpath))
    )

    button.click()

    dialog = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
    )   

    input_elements = dialog.find_elements(By.XPATH,".//input")
    inputs = {}
    buttons = {}
    for input_element in input_elements:
        input_name = input_element.get_attribute("name")
        inputs[input_name] = input_element

    button_elements = dialog.find_elements(By.XPATH,".//button")
    for button_element in button_elements:
        buttons[button_element.text] = button_element

    def get_helper_text(input_name):
        return dialog.find_element(By.XPATH, f".//input[@name='{input_name}']/ancestor::div[2]/p")

    return {
        "self": dialog,
        "inputs": inputs,
        "buttons": buttons,
        "get_helper_text": get_helper_text
    }

def datetime_to_keys(datetime_str):
    if(datetime_str == ""):
        return datetime_str
    date_obj = datetime.strptime(datetime_str,"%m/%d/%Y %I:%M %p")
    return date_obj.strftime("%m%d%Y%I%M%p")

def post_reminder(driver,wait,reminder={"message": "New Reminder", "email": "ccata002@gmail.com", "datetime": "12/31/2024 11:59 PM", "phone": "7864400382"}):
    dialog = open_and_get_dialog(driver,wait,"//button[normalize-space()='Add Reminder']")

    inputs = dialog["inputs"]
    input_message = inputs["message"]
    input_email = inputs["email"]
    input_datetime = inputs["datetime"]
    input_phone = inputs["phone"]

    input_message.clear()
    input_email.clear()
    input_datetime.send_keys(Keys.CONTROL + "a")
    input_datetime.send_keys(Keys.DELETE)
    input_phone.clear()    

    input_message.send_keys(reminder["message"])
    input_email.send_keys(reminder["email"])
    input_datetime.send_keys(Keys.CONTROL + "a")
    input_datetime.send_keys(datetime_to_keys(reminder["datetime"]))
    input_phone.send_keys(reminder["phone"])

    submit_button = dialog["buttons"]["SUBMIT"]
    submit_button.click()

    return dialog

def put_reminder(driver,wait,reminder,index):
    dialog = open_and_get_dialog(driver,wait,f"//button[normalize-space()='Edit'][{index+1}]")

    inputs = dialog["inputs"]
    input_message = inputs["message"]
    input_email = inputs["email"]
    input_datetime = inputs["datetime"]
    input_phone = inputs["phone"]

    input_message.clear()
    input_email.clear()
    input_phone.clear()

    input_message.send_keys(reminder["message"])
    input_email.send_keys(reminder["email"])
    input_datetime.send_keys(Keys.CONTROL + "a")
    input_datetime.send_keys(datetime_to_keys(reminder["datetime"]))
    input_phone.send_keys(reminder["phone"])

    submit_button = dialog["buttons"]["SUBMIT"]
    submit_button.click()

    return dialog

def get_reminders():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reminders")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    reminders = []
    for reminder in result:
        reminders.append({
            "id": reminder[0],
            "message": reminder[1],
            "email": reminder[2],
            "datetime": reminder[3],
            "phone": reminder[4]
        })
        
    return reminders

__all__ = ["open_and_get_dialog","post_reminder","put_reminder","get_reminders"]