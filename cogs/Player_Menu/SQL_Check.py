import Quick_SQL
from Player_Menu import SQL_Lookup


def character_can_craft(character_name: str, gold_limit: float):
    cursor = Quick_SQL.db_connection()
    item_value = gold_limit * 2
    query = "Select A.Skill, D.Total " \
            "From Link_Character_Skills A " \
            "Left Join Info_Skills B " \
            "On A.Skill = B.Name " \
            "left join Link_Character_Items C " \
            "on B.Tools = C.Item " \
            "left join (select Crafting, count(*) as Total from Info_Item where value <= '{}' group by Crafting) D " \
            "on A.Skill = D.Crafting " \
            "where A.Character = '{}' and C.Character = '{}' and B.Job = 1 " \
            "order by A.Skill".format(item_value, character_name, character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        if row.Total is not None:
            return True
    return False


def character_on_crafting_table(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Main_Crafting " \
            "where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_crafting_point(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Main_Crafting " \
            "where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Crafting_Point != 1:
        return False
    return True


def character_has_gold(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_can_level_up(character_name: str):
    character_level = SQL_Lookup.character_sum_class_levels(character_name)
    character_xp = SQL_Lookup.character_xp(character_name)
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Info_XP " \
            "where Level='{}'".format(character_level)
    cursor.execute(query)
    xp_sheet = cursor.fetchone()
    if character_xp > xp_sheet.XP:
        return True
    return False


def character_has_items_to_sell_to_town(character_name: str):
    cursor = Quick_SQL.db_connection()
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
    cursor = Quick_SQL.db_connection()
    query = "Select * " \
            "From Link_Character_Items " \
            "Where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_items_on_sale(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Main_Trade " \
            "where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_item(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character = '{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_exists(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "Select Character_Name " \
            "From Main_Characters " \
            "Where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_class(character_name: str, class_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Link_Character_Class " \
            "where Character = '{}' AND Class = '{}'".format(character_name, class_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_professions(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Link_Character_Skills " \
            "where Character = '{}'".format(character_name)
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


def player_stat_roll(discord_id: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "From Discord_Roll " \
            "where Discord_ID = '{}' ".format(discord_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True
