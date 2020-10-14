import pyodbc
import logging
import time
import gspread
from google.oauth2.service_account import Credentials as gCredentials
import os
import Quick_Python
import json
from enum import IntEnum, auto

log = logging.getLogger(__name__)
pyodbc.native_uuid = True


def get_config_path():
    """
    Returns the path to patreon config file, prioritizing FORGEMASTER_CONFIG_PATH env var.
    :return: patreon config file path
    """
    default_config_path = os.path.join('Credentials', 'config.json')
    environment_path = os.getenv('FORGEMASTER_CONFIG_PATH')
    return default_config_path if environment_path is None else environment_path


'''''''''''''''''''''''''''''''''
############# CONFIG ############
'''''''''''''''''''''''''''''''''


def load_config(path):
    with open(path, "r") as config_file:
        local_config = json.load(config_file)
    return local_config


config = load_config(get_config_path())


'''''''''''''''''''''''''''''''''
############## SQL ##############
'''''''''''''''''''''''''''''''''

db_connect = None

def sql_db_connection() -> pyodbc.Cursor:
    global db_connect
    driver = config["sql-driver"]
    database = config["sql-database"]
    server = config["sql-server"]
    uid = config["sql-uid"]
    pwd = config["sql-pwd"]
    port = config["sql-port"]
    if db_connect is None:
        try:
            db_connect = pyodbc.connect(driver=driver, database=database, server=server, uid=uid, pwd=pwd, port=port,
                                        tds_version='8.0', charset='utf-8')
        except Exception as e:
            log.debug(e)
    return db_connect.cursor()


def sql_log_command(message):
    user = message.message.author.id
    command = message.message.content
    query = "insert into Command_Logs (User_ID,Command,DateTime) values (?,?,?)"\
        
    cursor = Quick_Python.run_query(query, [user, command, time.strftime('%Y-%m-%d %H:%M:%S')])
    cursor.commit()


def sql_log_private_command(user_id: str, command: str):
    query = "insert into Command_Logs (User_ID,Command,DateTime) values (?,?,?)"
    cursor = Quick_Python.run_query(query, [user_id, command, time.strftime('%Y-%m-%d %H:%M:%S')])
    cursor.commit()


def sql_log_error(user_id, user_command, error):
    command = error.replace("Command raised an exception: ", "")
    query = "insert into Error_Messages (Discord_ID,Discord_Command,Error,DateTime) " \
            "values (?,?,?,?)"
    cursor = Quick_Python.run_query(query,
                                    [user_id, user_command[0:50], command[0:200], time.strftime('%Y-%m-%d %H:%M:%S')])
    cursor.commit()


'''''''''''''''''''''''''''''''''
##############Google#############
'''''''''''''''''''''''''''''''''


class RosterColumns(IntEnum):
    BEGIN = 0
    DISCORD_NAME = auto()
    CHARACTER_NAME = auto()
    RACE = auto()
    BACKGROUND = auto()
    CLASS_1 = auto()
    CLASS_2 = auto()
    CLASS_3 = auto()
    EXPERIENCE = auto()
    LEVEL = auto()
    LEVELUP = auto()
    STR = auto()
    DEX = auto()
    CON = auto()
    INT = auto()
    WIS = auto()
    CHA = auto()
    GOLD = auto()
    FEATS = auto()
    SKILLS = auto()
    ITEMS = auto()
    END = auto()


def get_google_api_path():
    """
    Returns the path to patreon config file, prioritizing FORGEMASTER_GOOGLE_API_PATH env var.
    :return: patreon config file path
    """
    default_config_path = os.path.join('Credentials', 'GoogleAPI.json')
    environment_path = os.getenv('FORGEMASTER_GOOGLE_API_PATH')
    return default_config_path if environment_path is None else environment_path


def google_sheet(name: str):
    # connecting to google
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']
    file_path = os.path.join('Credentials', 'GoogleAPI.json')
    credentials = gCredentials.from_service_account_file(file_path, scopes=scope)
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


async def log_to_bot(bot, msg: str):
    log_channel = bot.get_channel(config["log-channel-id"])
    if log_channel is None:
        log.debug(msg)
    else:
        await log_channel.send(msg)


async def log_to_discord(self, msg: str):
    await log_to_bot(self.bot, msg)
