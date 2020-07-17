import pyodbc
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


'''''''''''''''''''''''''''''''''
################SQL#############
'''''''''''''''''''''''''''''''''


def sql_db_connection():
    # db_credential = 'Driver={SQL Server};''Server={DESKTOP-I8HAFTK\DB};''Database=LostWorld;''Trusted_Connection=yes;'
    driver = 'FreeTDS'
    database = 'LostWorld'
    server = '172.17.0.2'
    db_connect = pyodbc.connect(driver=driver, database=database, server=server)
    return db_connect.cursor()


def sql_log_command(message):
    user = message.message.author.id
    command = message.message.content.replace("'", "''")
    cursor = sql_db_connection()
    insert = "insert into Command_Logs (User_ID,Command,DateTime) values ('{}','{}','{}')"\
        .format(user, command, time.strftime('%Y-%m-%d %H:%M:%S'))
    cursor.execute(insert)
    cursor.commit()


def sql_log_private_command(user_id: str, command: str):
    cursor = sql_db_connection()
    insert = "insert into Command_Logs (User_ID,Command,DateTime) values ('{}','{}','{}')"\
        .format(user_id, command, time.strftime('%Y-%m-%d %H:%M:%S'))
    cursor.execute(insert)
    cursor.commit()


def sql_log_error(user_id, user_command, error):
    command = error.replace("'", "''").replace("Command raised an exception: ", "")
    cursor = sql_db_connection()
    insert = "insert into Error_Messages (Discord_ID,Discord_Command,Error,DateTime) " \
             "values ('{}','{}','{}','{}')"\
        .format(user_id, user_command[0:50], command[0:200], time.strftime('%Y-%m-%d %H:%M:%S'))
    cursor.execute(insert)
    cursor.commit()


'''''''''''''''''''''''''''''''''
##############Google#############
'''''''''''''''''''''''''''''''''


def google_sheet(name: str):
    # connecting to google
    scope = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join('Credentials', 'GoogleAPI.json'), scope)
    client = gspread.authorize(credentials)
    worksheet = client.open_by_key("1LzFoY8OT6ZbYL4lF10Ngz93lqYr97pP3iv8B3crdNyI").worksheet(name)
    return worksheet


def google_find_trade_seller(name: str, item: str):
    worksheet = google_sheet("Trade")
    row_count = len(worksheet.col_values(1))+1
    for row in range(row_count):
        if row in [0, 1]:
            continue
        # check name on row vs list
        if worksheet.cell(row, 1).value == name.lstrip() and worksheet.cell(row, 2).value == item.lstrip():
            return row
    return 0


'''''''''''''''''''''''''''''''''
#############Discord#############
'''''''''''''''''''''''''''''''''
test_server_channel = 733788956101181600


async def log_to_discord(self, log: str):
    log_channel = self.bot.get_channel(test_server_channel)
    await log_channel.send(log)
