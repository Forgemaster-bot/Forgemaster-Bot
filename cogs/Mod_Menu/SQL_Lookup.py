import Connections


def player_id_by_name(name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where Name = '{}'".format(name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.ID


def player_name_by_id(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where ID = '{}'".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def player_stat_roll(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Discord_Roll " \
            "where Discord_ID = '{}'".format(discord_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result


def character_owner(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID='{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Discord_ID


def character_ability_score(character_id: str, ability: str):
    cursor = Connections.sql_db_connection()
    sql_command = "select * from Main_Characters where ID = '{}'".format(character_id)
    cursor.execute(sql_command)
    result = cursor.fetchone()
    value = 0
    if ability == "STR":
        value = result.Strength
    if ability == "DEX":
        value = result.Dexterity
    if ability == "CON":
        value = result.Constitution
    if ability == "INT":
        value = result.Intelligence
    if ability == "WIS":
        value = result.Wisdom
    if ability == "CHA":
        value = result.Charisma
    return value


def character_item_quantity(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Link_Character_Items where Character_ID = '{}' AND Item = '{}'".format(character_id,
                                                                                                  item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item.Quantity


def character_id_by_character_name(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.ID


def character_name_by_character_id(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Character_Name
