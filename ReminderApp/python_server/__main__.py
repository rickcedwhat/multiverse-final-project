import pyodbc
import time
from pydantic import BaseModel, field_validator
import re
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

class Reminder(BaseModel):
    message: str
    email: str
    datetime: str
    phone:str

    @field_validator('phone')
    def phone_must_match_pattern(cls, v):
        phone_regex = r"^\d{10}$"
        if not re.match(phone_regex, v):
            raise ValueError("Invalid phone number. Please enter a 10-digit number.")
        return v

    @field_validator('email')
    def email_must_match_pattern(cls, v):
        email_regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if not re.match(email_regex, v):
            raise ValueError("Invalid email address format. Please enter a valid email address.")
        return v

table_columns = [("id", "INT PRIMARY KEY IDENTITY"), ("message", "VARCHAR(255)"), ("email", "VARCHAR(255)"), ("datetime", "DATETIME"), ("phone", "VARCHAR(255)")]

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connection string
conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=USLMACEATALAN2\MSSQLSERVER01;'
    r'DATABASE=Reminders2024;'
    r'Trusted_Connection=yes;'
)

@app.get("/")
def read_root():
    return "Read docs at localhost:8000/docs or localhost:8000/redoc"


@app.get("/reminders")
def read_reminders():

    print("Getting reminders")

    # Establish a connection to the SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # check connection
    cursor.execute("SELECT * FROM Reminders")
    rows = cursor.fetchall()
    reminders = []
    for row in rows:
        reminders.append({
            "id": row[0],
            "message": row[1],
            "email": row[2],
            "datetime": row[3],
            "phone": row[4]            
        })

    # Close the connection
    conn.close()

    return reminders

@app.post("/reminders")
def create_reminder(reminder:Reminder):
    print("Creating reminder",reminder)

    datetime_obj = datetime.strptime(reminder.datetime, "%a %b %d %Y %H:%M:%S GMT%z (%Z)")

    # Establish a connection to the SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Execute the INSERT statement
    cursor.execute("INSERT INTO Reminders (message, email, datetime,phone) VALUES (?, ?, ?, ?)",
                reminder.message, reminder.email, datetime_obj, reminder.phone)

    # Commit the transaction
    conn.commit()

    # Retrieve the generated ID
    cursor.execute("SELECT SCOPE_IDENTITY()")
    row = cursor.fetchone()
    id = row[0]

    # Close the connection
    conn.close()

    return {
        "id": id,
        "message": reminder.message,
        "email": reminder.email,
        "datetime": reminder.datetime,
        "phone": reminder.phone
    }

@app.put("/reminders/{id}")
def update_reminder(id:int, reminder:Reminder):
    print("Updating reminder",reminder,id)

    datetime_obj = datetime.strptime(reminder.datetime, "%a %b %d %Y %H:%M:%S GMT%z (%Z)")

    # Establish a connection to the SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Execute the UPDATE statement
    cursor.execute("UPDATE Reminders SET message = ?, email = ?, datetime = ?, phone = ? WHERE id = ?",
                   reminder.message, reminder.email, datetime_obj, reminder.phone, id)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

    return {
        "id": id,
        "message": reminder.message,
        "email": reminder.email,
        "datetime": reminder.datetime,
        "phone": reminder.phone
    }

@app.delete("/reminders/{id}")
def delete_reminder(id:int):
    print("Deleting reminder", id)

    # Establish a connection to the SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Execute the DELETE statement
    cursor.execute("DELETE FROM Reminders WHERE id = ?", id)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

    return {
        "status": "success"
    }

@app.delete("/reminders")
def delete_all_reminders():
    print("Deleting all reminders")

    # Establish a connection to the SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Execute the DELETE statement
    cursor.execute("DELETE FROM Reminders")

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

    return {
        "status": "success"
    }

@app.get("/reformat")
def reformat_reminders():
    print("Reformatting reminders")
    # drop reminders table and create a new reminder table based on the Reminder model

    # Establish a connection to the SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    create_reminder_table(cursor)

    # # Execute the DROP statement
    # cursor.execute("DROP TABLE Reminders")
    
    # # Execute the CREATE statement
    # print("CREATE TABLE Reminders ({})".format(" ".join([f"{column[0]} {column[1]}" for column in table_columns])))
    # cursor.execute("CREATE TABLE Reminders ({})".format(", ".join([f"{column[0]} {column[1]}" for column in table_columns])))
    
    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

    return {
        "status": "success"
    }

def create_reminder_table(cursor):
    print("Creating reminder table")
    # drop table if it exists and create a new reminder table based on the Reminder model
    cursor.execute("DROP TABLE IF EXISTS Reminders")
    
    # Execute the CREATE statement
    cursor.execute("CREATE TABLE Reminders ({})".format(", ".join([f"{column[0]} {column[1]}" for column in table_columns])))

@app.get("/backup_and_drop")
def backup_and_drop():
    print("Backing up and dropping reminders")
    # drop reminders table and create a new reminder table based on the Reminder model

    # Establish a connection to the SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Execute the SELECT statement
    cursor.execute("SELECT * FROM Reminders")
    rows = cursor.fetchall()
    reminders = []
    for row in rows:
        reminders.append({
            "message": row[1],
            "email": row[2],
            "datetime": row[3],
            "phone": row[4]            
        })

    create_reminder_table(cursor)
    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

    return reminders

@app.post("/seed")
def seed_reminders(seed:List[Reminder]):
    print("Seeding reminders")
    
    # Establish a connection to the SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    create_reminder_table(cursor)

    for reminder in seed:
        datetime_obj = datetime.fromisoformat(reminder.datetime)
        # Execute the INSERT statement
        cursor.execute("INSERT INTO Reminders (message, email, datetime,phone) VALUES (?, ?, ?, ?)",
                    reminder.message, reminder.email, datetime_obj, reminder.phone)
    
    # Commit the transaction
    conn.commit()
    conn.close()
    return {
        "status": "success"
    }



