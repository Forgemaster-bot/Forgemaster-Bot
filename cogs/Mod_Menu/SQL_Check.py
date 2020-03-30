import Quick_SQL


def character_exists(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Main_Characters " \
            "where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def race_exists(name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Info_Races " \
            "where Name = '{}'".format(name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def class_exists(name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Info_Classes " \
            "where Name = '{}'".format(name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def player_exists(user_id: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Info_Discord where ID='{}'".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_feat(character_name: str, feat_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Link_Character_Feats " \
            "where Character = '{}' AND Feat = '{}'".format(character_name, feat_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def skill_exists(name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Info_Skills " \
            "where Name = '{}'".format(name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_skill(character_name: str, skill_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Link_Character_Skills " \
            "where Character = '{}' AND Skill = '{}'".format(character_name, skill_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_stat_max(character_name: str, stat: str, change: int):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Main_Characters " \
            "where Character_Name = '{}'".format(character_name)
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
