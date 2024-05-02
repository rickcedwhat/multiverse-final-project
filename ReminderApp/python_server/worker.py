import pyodbc
from datetime import datetime
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=USLMACEATALAN2\MSSQLSERVER01;'
    r'DATABASE=Reminders2024;'
    r'Trusted_Connection=yes;'
)



def get_rows():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("SELECT * FROM Reminders WHERE datetime <= ? ORDER BY datetime", current_datetime)
    rows = cursor.fetchall()
    
    conn.close()
    
    return rows if rows else None

def job():
    rows = get_rows()
    if rows:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        for row in rows:
            id = row[0]
            message = row[1]
            email = row[2]
            datetime = row[3]
            print(f"Sending reminder: {message} to {email} at {datetime}")
            cursor.execute("DELETE FROM Reminders WHERE id = ?", id)
        conn.commit()
        conn.close()
    else:
        print("No reminders to send")

def send_email(sender_email, sender_password, recipient_email, subject, body):
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create a MIME message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Add the body to the message
    msg.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


if __name__ == "__main__":
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(5)