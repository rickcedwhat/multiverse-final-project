import pyodbc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime, timedelta
import random
import requests



conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=USLMACEATALAN2\MSSQLSERVER01;'
    r'DATABASE=Reminders2024;'
    r'Trusted_Connection=yes;'
)

# def seed_reminders(reminders):
#     conn = pyodbc.connect(conn_str)
#     cursor = conn.cursor()
#     for reminder in reminders:
#         cursor.execute("INSERT INTO Reminders (message,email,datetime,phone) VALUES (?,?,?,?)",reminder["message"],reminder["email"],reminder["datetime"],reminder["phone"])
#     conn.commit()
#     cursor.close()
#     conn.close()

# def seed_reminders():
#     reminders = [
#         {"message": "New Reminder", "email": "ccata002@gmail.com
#     ]

#     # call fastapi endpoint to seed reminders
#     for reminder in reminders:
#         response = requests.post("http://localhost:8000/seed",json=reminder)
#         print(response.json())

def backup_and_drop():
    # call backup endpoint
    response = requests.get("http://localhost:8000/backup_and_drop")
    print(response.json())
    return response.json()
    


def open_and_get_dialog(wait,button_xpath):
    button = None
    try:
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
    except:
        print("Could not find element with xpath: "+button_xpath)
        return None

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

    # wait for button elements to have text
    button_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH,"//div[@role='dialog']//button"))
    )

    for button_element in button_elements:
        buttons[button_element.text] = button_element

    title = dialog.find_element(By.XPATH,".//*[contains(@class,'MuiDialogTitle-root')]").text

    content = dialog.find_element(By.XPATH,".//div[contains(@class,'MuiDialogContent-root')]")
    content_text = [el.text for el in content.find_elements(By.XPATH,".//*[contains(@class,'MuiTypography-root')]")]

    def get_helper_text(input_name):
        return dialog.find_element(By.XPATH, f".//input[@name='{input_name}']/ancestor::div[2]/p")
    
    # def get_button(button_name):
    #     return dialog.find_element(By.XPATH, f".//button[normalize-space()='{button_name}']")

    return {
        "self": dialog,
        "inputs": inputs,
        "buttons": buttons,
        "text":{"title":title,"content":content_text},
        "get_helper_text": get_helper_text,
        # "get_button": get_button
    }

def datetime_to_keys(datetime_str):
    if(datetime_str == ""):
        return datetime_str
    date_obj = datetime.strptime(datetime_str,"%m/%d/%Y %I:%M %p")
    return date_obj.strftime("%m%d%Y%I%M%p")

def post_reminder(wait,reminder={"message": "New Reminder", "email": "ccata002@gmail.com", "datetime": "12/31/2024 11:59 PM", "phone": "7864400382"}):
    dialog = open_and_get_dialog(wait,"//button[normalize-space()='Add Reminder']")

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

def put_reminder(wait,reminder,id):
    dialog = open_and_get_dialog(wait,f"//div[@data-id='reminder-{id}']//button[normalize-space()='Edit']")

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

def get_reminders(random=False):
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

def get_random_reminder(wait):
    # reminders = get_reminders()
    reminders = parse_reminders(wait)
    if len(reminders) == 0:
        return None
    elif len(reminders) == 1:
        return reminders[0]
    index = random.randint(0,len(reminders)-1)
    print(index,reminders[index])
    return reminders[index]

def get_reminder_by_id(wait,id):
    reminders = parse_reminders(wait)
    for reminder in reminders:
        if reminder["id"] == id:
            return reminder

    return None

# def get_reminder_by_id(id):
#     conn = pyodbc.connect(conn_str)
#     cursor = conn.cursor()
#     cursor.execute(f"SELECT * FROM Reminders WHERE id={id}")
#     result = cursor.fetchone()
#     cursor.close()
#     conn.close()

#     if result == None:
#         return None 

#     return {
#         "id": result[0],
#         "message": result[1],
#         "email": result[2],
#         "datetime": result[3],
#         "phone": result[4]
#     }

def format_datetime(datetime,for_front_end=True):
    if(for_front_end):
        return datetime.strftime("%a %b %dth %Y %I:%M %p")
    return datetime.strftime("%m/%d/%Y %I:%M %p")
    
def parse_datetime(datetime_str,for_front_end=True):
    if(for_front_end):
        return datetime.strptime(datetime_str,"%a %b %dth %Y %I:%M %p")
    return datetime.strptime(datetime_str,"%m/%d/%Y %I:%M %p")


def get_date_from_now(days=3):
    return datetime.now() + timedelta(days)

def parse_reminders(wait,stale=False):

    if stale and wait.until(EC.staleness_of((By.XPATH,"//div[@data-id]"))):
        return []
    
    # get all reminders on the page
    reminders = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@data-id]")))
    parsed_reminders = []
    for reminder in reminders:
        id = reminder.get_attribute("data-id").split("-")[1]
        message = reminder.find_element(By.XPATH,".//*[@data-id='message']").text
        email = reminder.find_element(By.XPATH,".//*[@data-id='email']").text
        datetime = reminder.find_element(By.XPATH,".//*[@data-id='datetime']").text
        phone = reminder.find_element(By.XPATH,".//*[@data-id='phone']").text
        parsed_reminders.append({
            "id": id,
            "message": message,
            "email": email,
            "datetime": datetime,
            "phone": phone
        })

    return parsed_reminders

def parse_reminder(wait,id):
    # reminder = driver.find_element(By.XPATH,f"//div[@data-id='reminder-{id}']")
    reminder = wait.until(EC.presence_of_element_located((By.XPATH,f"//div[@data-id='reminder-{id}']")))
    message = reminder.find_element(By.XPATH,".//*[@data-id='message']").text
    email = reminder.find_element(By.XPATH,".//*[@data-id='email']").text
    datetime = reminder.find_element(By.XPATH,".//*[@data-id='datetime']").text
    phone = reminder.find_element(By.XPATH,".//*[@data-id='phone']").text

    return {
        "id": id,
        "message": message,
        "email": email,
        "datetime": datetime,
        "phone": phone
    }
    

__all__ = ["open_and_get_dialog","post_reminder","put_reminder","get_reminders", "get_random_reminder","get_reminder_by_id","drop_reminders","get_date_from_now", "format_datetime","parse_datetime","parse_reminders","parse_reminder","backup_and_drop"]