import Connections
from Player_Menu import SQL_Lookup


def character_has_profession_tools(character_name:str, profession: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character = '{}' AND Item = '{}'".format(character_name, profession)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_on_crafting_table(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Crafting " \
            "where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_crafted_this_week(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Crafting " \
            "where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Crafting_Value != 50:
        return False
    return True


def character_has_gold(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_can_level_up(character_name: str):
    character_level = SQL_Lookup.character_sum_class_levels(character_name)
    character_xp = SQL_Lookup.character_xp(character_name)
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_XP " \
            "where Level='{}'".format(character_level)
    cursor.execute(query)
    xp_sheet = cursor.fetchone()
    if character_xp >= xp_sheet.XP:
        return True
    return False


def character_has_items_to_sell_to_town(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Link_Character_Items " \
            "Where Character = '{}' " \
            "AND Item in (select Name from Info_Item)".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_items_to_trade(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Link_Character_Items " \
            "Where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_items_on_sale(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Trade " \
            "where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_item(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character = '{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_item_quantity(character_name: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character = '{}' AND Item = '{}' AND Quantity >= '{}'".format(character_name, item_name, quantity)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_exists(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select Character_Name " \
            "From Main_Characters " \
            "Where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_class(character_name: str, class_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Class " \
            "where Character = '{}' AND Class = '{}'".format(character_name, class_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_professions(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Skills " \
            "where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def player_exists(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_Discord where ID='{}'".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def player_stat_roll(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Discord_Roll " \
            "where Discord_ID = '{}' ".format(discord_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_enough_gold_to_buy_trade(gold: float):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Trade " \
            "where Price <='{}'".format(gold)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True
