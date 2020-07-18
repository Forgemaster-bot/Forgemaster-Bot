import pyodbc
import time
import gspread
from google.oauth2.service_account import Credentials as gCredentials
from oauth2client.service_account import ServiceAccountCredentials
import os
from Quick_Python import run_query

spreadsheet_id = "1jcL82F3cCBrcOHkQtW-cepiwkcPYRcej5ZMFNQ8CirI"

'''''''''''''''''''''''''''''''''
################SQL#############
'''''''''''''''''''''''''''''''''


def sql_db_connection():
    # db_credential = 'Driver={SQL Server};''Server={DESKTOP-I8HAFTK\DB};''Database=LostWorld;''Trusted_Connection=yes;'
    driver = 'FreeTDS'
    database = 'LostWorld'
    server = '172.17.0.2'
    try:
        db_connect = pyodbc.connect(driver=driver, database=database, server=server, uid='SA', pwd='{W$lfBaj&q;wmD64TzbXtd$Jtj|jO}', port='1433')
    except Exception as e:
        print(e)
    return db_connect.cursor()


def sql_log_command(message):
    user = message.message.author.id
    command = message.message.content.replace("'", "''")
    insert = "insert into Command_Logs (User_ID,Command,DateTime) values (?,?,?)"\
        
    cursor = run_query(query, [user, command, time.strftime('%Y-%m-%d %H:%M:%S')])
    cursor.commit()


def sql_log_private_command(user_id: str, command: str):
    insert = "insert into Command_Logs (User_ID,Command,DateTime) values (?,?,?)"
    cursor = run_query(query, [user_id, command, time.strftime('%Y-%m-%d %H:%M:%S')])
    cursor.commit()


def sql_log_error(user_id, user_command, error):
    command = error.replace("'", "''").replace("Command raised an exception: ", "")
    insert = "insert into Error_Messages (Discord_ID,Discord_Command,Error,DateTime) " \
             "values (?,?,?,?)"
    cursor = run_query(query, [user_id, user_command[0:50], command[0:200], time.strftime('%Y-%m-%d %H:%M:%S')])
    cursor.commit()


'''''''''''''''''''''''''''''''''
##############Google#############
'''''''''''''''''''''''''''''''''


def google_sheet(name: str):
    # connecting to google
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']
    file_path = os.path.join('Credentials', 'GoogleAPI.json')
    credentials = gCredentials.from_service_account_file(file_path, scopes=scope)
    # credentials = ServiceAccountCredentials.from_json_keyfile_name(file_path, scopes=scope)

    client = gspread.authorize(credentials)
    worksheet = client.open_by_key(spreadsheet_id).worksheet(name)
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
