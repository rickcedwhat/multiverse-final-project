# Reminder App

This project is a reminder app that allows users to create, edit, update, and delete reminders in a local SQL Server database. The app is built using React, TypeScript, and the FastAPI framework.

## Core Ideas

1. **Local SQL Server Database**: The app stores reminders in a local SQL Server database. The app uses pyodbc to connect to the database and perform CRUD operations.

2. **Server Agent**: The app uses the SQL Server Agent to check the Reminders table every minute for reminders to be sent. The app includes a code snippet to set up the job.

3. **DB Mail**: The app uses DB Mail to send reminders. The app includes a place to configure the SMTP server, sender email, and sender password.

4. **Client-Side Validation**: The app uses client-side validation to ensure that the user creates a valid reminder. The app includes code to validate the reminder message, datetime, email, and phone number.

5. **Testing**: The app includes several tests in pytest to ensure that the front end functions the way it should. The app includes a place to include all the test names.

## Getting Started

1. **Database Setup**: Set up a local SQL Server database with a Reminders table. The app uses the Reminder model to create the table.

2. **Environment Variables**: Set up the necessary environment variables for the app to connect to the database and send reminders. The app uses the dotenv package to load the environment variables.

3. **Server Agent Setup**: Set up the SQL Server Agent to run the job that checks the Reminders table for reminders to be sent. The app includes a code snippet to set up the job.

4. **DB Mail Setup**: Set up the SMTP server, sender email, and sender password for the app to send reminders. The app uses the DBMail package to send the reminders.

## Code Snippets

### Server Agent Job Setup

```
DECLARE @current_datetime DATETIME = GETDATE();

DECLARE @recipients TABLE (email NVARCHAR(MAX), message NVARCHAR(MAX));

INSERT INTO @recipients
SELECT email, message
FROM Reminders
WHERE datetime <= @current_datetime;

DECLARE @recipient NVARCHAR(MAX);
DECLARE @message NVARCHAR(MAX);

WHILE EXISTS (SELECT TOP 1 1 FROM @recipients)
BEGIN
SELECT TOP 1 @recipient = email, @message = message FROM @recipients;

DECLARE @formatted_message NVARCHAR(MAX);
SET @formatted_message = 'Hello, This is the reminder you requested for ' + FORMAT(@current_datetime, 'MM/dd/yyyy HH:mm:ss') + '. ' + @message;

EXEC msdb.dbo.sp_send_dbmail
@profile_name = 'DB Notification',
@recipients = @recipient,
@subject = 'Reminder Notification',
@body = @formatted_message;

 DELETE FROM @recipients WHERE email = @recipient;
END;

DELETE FROM Reminders WHERE datetime <= @current_datetime;
```
