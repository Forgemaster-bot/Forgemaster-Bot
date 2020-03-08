import pyodbc
import time


def db_connection():
    db_credential = 'Driver={SQL Server};''Server={DESKTOP-I8HAFTK\DB};''Database=LostWorld;''Trusted_Connection=yes;'
    db_connect = pyodbc.connect(db_credential)
    return db_connect.cursor()


def log_command(message):
    user = message.message.author.id
    command = message.message.content
    cursor = db_connection()
    insert = "insert into Command_Logs (User_ID,Command,DateTime) values ('{}','{}','{}')"\
        .format(user, command, time.strftime('%Y-%m-%d %H:%M:%S'))
    cursor.execute(insert)
    cursor.commit()


def log_craft_command(character_name: str, item_name: str, quantity: int, value: int, user_id: str):
    command = "{} made {} {} for {}g".format(character_name,quantity, item_name, value)
    cursor = db_connection()
    insert = "insert into Command_Logs (User_ID,Command,DateTime) values ('{}','{}','{}')"\
        .format(user_id, command, time.strftime('%Y-%m-%d %H:%M:%S'))
    cursor.execute(insert)
    cursor.commit()
