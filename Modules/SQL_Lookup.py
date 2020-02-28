import Quick_SQL


def player_name_by_id(user_id: str):
    cursor = Quick_SQL.db_connection()
    query = 'select * from Info_Discord where ID={}'.format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def player_id_by_name(name:str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Info_Discord where Name = '{}'".format(name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.ID


def player_stat_roll(discord_id: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "From Discord_Roll " \
            "where Discord_ID = '{}'".format(discord_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result


def character_sheet(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    return cursor.fetchone()


def character_owner(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Discord_ID


def character_class_by_order(character_name: str, order: int):
    cursor = Quick_SQL.db_connection()
    query = "select * from Link_Character_Class where Character='{}' and Number = '{}'".format(character_name,order)
    cursor.execute(query)
    class_lookup = cursor.fetchone()
    return class_lookup.Class, class_lookup.Level


def character_class_level_by_class(character_name: str, character_class: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Link_Character_Class where Character='{}' and Class = '{}'".format(character_name,character_class)
    cursor.execute(query)
    class_lookup = cursor.fetchone()
    return class_lookup.Level


def character_count_classes(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select Count(*) Total from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def character_sum_class_levels(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select SUM(Level) Total from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def character_feats(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Link_Character_Feats where Character='{}'".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    feats = []
    for row in rows:
        feats.append(row.Feat)
    return feats


def character_item_quantity(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Link_Character_Items where Character='{}' AND Item = '{}'".format(character_name,item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item.Quantity


def character_inventory(character_name:str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Link_Character_Items where Character='{}'".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


def character_xp(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.XP


def character_gold(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.Gold


def character_ability_score(character_name: str, ability: str):
    cursor = Quick_SQL.db_connection()
    sql_command = "select * from Main_Characters where Character_Name = '{}'".format(character_name)
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


def character_skills(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Link_Character_Skills where Character='{}'".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    skills = []
    for row in rows:
        if row.Proficiency == 1:
            skills.append(row.Skill)
        else:
            skills.append(row.Skill + " (D)")
    return skills


def trade_item_quantity(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Trade where Character='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item.Quantity


def trade_item_price(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Trade where Character='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item.Price


def trade_item(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Trade where Character='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def info_skills():
    cursor = Quick_SQL.db_connection()
    query = "select Name from Info_Skills Where Job = 'True' ORDER BY Name"
    cursor.execute(query)
    rows = cursor.fetchall()
    skills = []
    for row in rows:
        skills.append(row.Name)
    return skills


def info_classes():
    cursor = Quick_SQL.db_connection()
    query = "select Name from Info_Classes ORDER BY Name"
    cursor.execute(query)
    rows = cursor.fetchall()
    classes = []
    for row in rows:
        classes.append(row.Name)
    return classes

