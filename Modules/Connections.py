import pyodbc
import time
import gspread
from google.oauth2.service_account import Credentials as gCredentials
from oauth2client.service_account import ServiceAccountCredentials
import os
from Quick_Python import run_query
import json


def load_config(path):
    config = dict()
    with open(path, "r") as config_file:
        config = json.load(config_file)
    return config

config = load_config(os.path.join('Credentials','config.json'))

'''''''''''''''''''''''''''''''''
################SQL#############
'''''''''''''''''''''''''''''''''


def sql_db_connection():
    driver      = config["sql-driver"]
    database    = config["sql-database"]
    server      = config["sql-server"]
    uid         = config["sql-uid"]
    pwd         = config["sql-pwd"]
    port        = config["sql-port"]
    try:
        db_connect = pyodbc.connect(driver=driver, database=database, server=server, uid=uid, pwd=pwd, port=port)
    except Exception as e:
        print(e)
    return db_connect.cursor()


def sql_log_command(message):
    user = message.message.author.id
    command = message.message.content.replace("'", "''")
    query = "insert into Command_Logs (User_ID,Command,DateTime) values (?,?,?)"\
        
    cursor = run_query(query, [user, command, time.strftime('%Y-%m-%d %H:%M:%S')])
    cursor.commit()


def sql_log_private_command(user_id: str, command: str):
    query = "insert into Command_Logs (User_ID,Command,DateTime) values (?,?,?)"
    cursor = run_query(query, [user_id, command, time.strftime('%Y-%m-%d %H:%M:%S')])
    cursor.commit()


def sql_log_error(user_id, user_command, error):
    command = error.replace("'", "''").replace("Command raised an exception: ", "")
    query = "insert into Error_Messages (Discord_ID,Discord_Command,Error,DateTime) " \
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
    worksheet = client.open_by_key(config["spreadsheet-id"]).worksheet(name)
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
async def log_to_bot(bot, log: str):
    log_channel = bot.get_channel(config["log-channel-id"])
    await log_channel.send(log)


async def log_to_discord(self, log: str):
    await log_to_bot(self.bot, log)
