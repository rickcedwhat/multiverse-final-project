import pyodbc
from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

class Reminder(BaseModel):
    message: str
    email: str
    datetime: str
    # is_active: bool

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
    return "Read docs at /docs or /redoc"


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
            "datetime": row[3]
        })

    # Close the connection
    conn.close()

    return reminders

@app.post("/reminders")
def create_reminder(reminder:Reminder):
    print("Creating reminder")
    
    datetime_obj = datetime.fromisoformat(reminder.datetime)

    # Establish a connection to the SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Execute the INSERT statement
    cursor.execute("INSERT INTO Reminders (message, email, datetime) VALUES (?, ?, ?)",
                   reminder.message, reminder.email, datetime_obj)

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
        "datetime": reminder.datetime
    }

@app.put("/reminders/{id}")
def update_reminder(id:int, reminder:Reminder):
    print("Updating reminder")

    print(reminder)

    datetime_obj = datetime.fromisoformat(reminder.datetime)

    # Establish a connection to the SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Execute the UPDATE statement
    cursor.execute("UPDATE Reminders SET message = ?, email = ?, datetime = ? WHERE id = ?",
                   reminder.message, reminder.email, datetime_obj, id)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

    return {
        "id": id,
        "message": reminder.message,
        "email": reminder.email,
        "datetime": reminder.datetime
    }

@app.delete("/reminders/{id}")
def delete_reminder(id:int):
    print("Deleting reminder")

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

# // added more endpoints in the backend and added ways to connect with them on the frontend

# - added a form to create a new reminder or edit an existing one

# - added a way to delete a reminder

# - need to make sure the sql server automations I set up the other day are working

# saved my project to its own repo - need to add michael as a collaborator