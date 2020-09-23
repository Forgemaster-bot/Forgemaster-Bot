import random
import logging
import Connections
import pyodbc
from textwrap import dedent
import struct


log = logging.getLogger(__name__)


def labelled_str(label, data):
    """
    Return string with bold label followed by data
    :param label: object containing string rep of label
    :param data: object containing string rep of items
    :return: string with bold key in format "key: value"
    """
    return "**{}:** {}".format(str(label), str(data))


def labelled_list(label, data: list):
    """
    Returns label joined with string representation of objects in data separated by commas.
    :param label: object containing string rep of bold label in front of data
    :param data: list of object containing string rep of items to separate by comma
    :return: string with bold key in format "key: value"
    """
    csv = ", ".join(str(item) for item in data) if data else "None"
    return labelled_str(label, csv)


def flatten(container):
    """
    Flattens iterarable container passed into a single list
    :param container: iterable container (i.e. list)
    :return: single level list
    """
    if not container:
        return container
    if isinstance(container, str):
        container = [container]
    if isinstance(container[0], list):
        return flatten(container[0]) + flatten(container[1:])
    return container[:1] + flatten(container[1:])


def transform_dict_keys(values_dict: dict, keys_dict: dict) -> dict:
    """
    Transform values_dict to contain new keys of matching value in keys_dict
    :param values_dict: dictionary containing key:value pairs where value contains final values
    :param keys_dict: dictionary containing key:value where key matches key in values_dict and value is the new key
    :return: dict containing new keys relating to Character attributes
    """
    return dict((keys_dict[k], v) for k, v in values_dict.items() if k in keys_dict)


def to_single_line(query: str) -> str:
    # Strip common leading whitespace and remove new lines to make a single line
    return dedent(query).replace('\n', '')


def log_transaction(query: str, args: list = None):
    log.debug(f"run_query: query[{to_single_line(query)}]; args[{str(args)}];")


def run_query(query: str, args: list = None) -> pyodbc.Cursor:
    # log the query
    log_transaction(query, args)
    # Connect to db, execute the query, and return cursor
    cursor = Connections.sql_db_connection()
    if args is None:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor


def run_query_commit(query: str, args: list = None):
    run_query(query, args).commit()


def get_column_names_and_types(table: str):
    cursor = Connections.sql_db_connection()
    return get_column_names_and_types_with_cursor(table, cursor)


def get_column_names_and_types_with_cursor(table: str, cursor):
    return {c.column_name: c.data_type for c in cursor.columns(table=table)}


def list_to_string(given_list: list):
    return ", ".join(str(element) for element in given_list) if given_list else ""


def list_to_table(given_list: list):
    return_string = ""
    for element in given_list:
        if return_string == "":
            return_string = element
        else:
            return_string = "{}\n{}".format(return_string, element)
    return return_string


def find_character_row(character_list: list, character_name: str):
    for row in range(len(character_list)):
        target = character_list[row].lower()
        if target == character_name.lower():
            return row + 1
    return 0


def ability_name_check(stat: str):
    stat_list = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
    for name in stat_list:
        if name == stat:
            return True
    return False


def ability_name_convert(ability: str):
    if ability == 'STR':
        return 'Strength'
    elif ability == 'DEX':
        return 'Dexterity'
    elif ability == 'CON':
        return 'Constitution'
    elif ability == 'INT':
        return 'Intelligence'
    elif ability == 'WIS':
        return 'Wisdom'
    elif ability == 'CHA':
        return 'Charisma'
    return None


def dice_roll(low: int, high: int):
    response = random.randint(low, high)
    return response


def question_list(give_list: list):
    return_string = ""
    list_length = len(give_list)
    for entry in range(list_length):
        if return_string == "":
            return_string = "{} : {}".format(entry + 1, give_list[entry])
        else:
            return_string = "{}\n{} : {}".format(return_string, entry + 1, give_list[entry])
    return return_string


def find_trade_row(seller_name: str, seller_list: list, item_name: str, item_list: list):
    for row in range(len(seller_list)):
        if seller_list[row].lower() == seller_name.lower():
            character_index = row
            list_item_name = item_list[character_index]
            if list_item_name.lower() == item_name.lower():
                trade_row = character_index + 1
                return trade_row


def check_player_exists(user_id: str):
    query = "select * " \
            "from Info_Discord where ID= ? "
    cursor = run_query(query, [user_id])
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def sync_player(discord_id: str, discord_name: str):
    try:
        log.debug("discord_id: " + discord_id + "; discord_name: " + discord_name)
        if not check_player_exists(discord_id):
            insert_players(discord_id, discord_name)
            return True, "New"
        elif discord_name != lookup_player_name_by_id(discord_id):
            update_player_name(discord_name, discord_id)
            return True, "Update"
    except Exception as e:
        log.debug(e)
        return False, "Something went wrong adding {} to the list".format(discord_name)
    return False, "No change"


def insert_players(user_id: str, name: str):
    query = "insert into Info_Discord (ID,Name,Character_Number) values (?,?,1)"
    cursor = run_query(query, [user_id, name])
    cursor.commit()


def lookup_player_name_by_id(user_id: str):
    query = "select * from Info_Discord where ID= ?"
    cursor = run_query(query, [user_id])
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def update_player_name(discord_name: str, discord_id: str):
    query = "UPDATE Info_Discord " \
            "SET Name = ? " \
            "WHERE ID = ?"
    cursor = run_query(query, [discord_name, discord_id])
    cursor.commit()

def guid_to_lowercase(value):
    first_three_values = struct.unpack('<I2H', value[:8])
    fourth_value = struct.unpack('>H', value[8:10])[0]
    fifth_value = struct.unpack('>Q', b'\x00\x00' + value[10:16])[0]
    guid_string_parts = (
        '{:08x}'.format(first_three_values[0]),
        '{:04x}'.format(first_three_values[1]),
        '{:04x}'.format(first_three_values[2]),
        '{:04x}'.format(fourth_value),
        '{:012x}'.format(fifth_value),
    )
    return '-'.join(guid_string_parts)
