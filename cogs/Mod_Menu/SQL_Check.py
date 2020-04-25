import Connections


def character_exists_by_name(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Characters " \
            "where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_exists_by_id(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Characters " \
            "where ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def race_exists(name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_Races " \
            "where Name = '{}'".format(name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def class_exists(name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_Classes " \
            "where Class = '{}'".format(name)
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


def character_has_feat(character_id: str, feat_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Feats " \
            "where Character_ID = '{}' AND Feat = '{}'".format(character_id, feat_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def skill_exists(name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_Skills " \
            "where Name = '{}'".format(name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_skill(character_id: str, skill_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Skills " \
            "where Character_ID = '{}' AND Skill = '{}'".format(character_id, skill_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_stat_max(character_id: str, stat: str, change: int):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Characters " \
            "where ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    value = 0
    if stat == "STR":
        value = result.Strength
    elif stat == "DEX":
        value = result.Dexterity
    elif stat == "CON":
        value = result.Constitution
    elif stat == "INT":
        value = result.Intelligence
    elif stat == "WIS":
        value = result.Wisdom
    elif stat == "CHA":
        value = result.Charisma

    if value + change > 20:
        return False
    return True


def character_has_item(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character_ID = '{}' AND Item = '{}'".format(character_id, item_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True

