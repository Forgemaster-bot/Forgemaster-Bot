import pyodbc
import time


def db_connection():
    db_credential = 'Driver={SQL Server};''Server={DESKTOP-I8HAFTK\DB};''Database=LostWorld;''Trusted_Connection=yes;'
    db_connect = pyodbc.connect(db_credential)
    return db_connect.cursor()


def log_command(message: str):
    user = message.message.author.id
    command = message.message.content
    cursor = db_connection()
    insert = "insert into Command_Logs (User_ID,Command,DateTime) values ('{}','{}','{}')"\
        .format(user, command, time.strftime('%Y-%m-%d %H:%M:%S'))
    cursor.execute(insert)
    cursor.commit()
