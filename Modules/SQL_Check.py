import Quick_SQL
import SQL_Lookup


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


def feat_exists(name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Info_Feats " \
            "where Name = '{}'".format(name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


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


def character_selling_item(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Main_Trade " \
            "where Character = '{}' AND Item = '{}'".format(character_name, item_name)
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


def player_owns_character(character_name: str, discord_id: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Main_Characters " \
            "where Character_Name = '{}' AND Discord_ID = '{}'".format(character_name, discord_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def level_up_check(character_name: str):
    character_level = SQL_Lookup.character_sum_class_levels(character_name)
    character_xp = SQL_Lookup.character_xp(character_name)
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Info_XP " \
            "where Level='{}'".format(character_level)
    cursor.execute(query)
    xp_sheet = cursor.fetchone()
    if character_xp > xp_sheet.XP:
        return "Yes"
    return "No"


'''''''''''''''''''''''''''''''''''''''''''''''''''
###################CRAFTING#######################
'''''''''''''''''''''''''''''''''''''''''''''''''''


def character_has_crafted(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Main_Crafting " \
            "where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_crafting_left(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Main_Crafting " \
            "where Character_Name = '{}' and Crafting_Value = 0 and Crafting_Point = 0".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_crafting_skill(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "Select count(*) as Total " \
            "From Link_Character_Skills A " \
            "Left Join Info_Skills B " \
            "On A.Skill = B.Name " \
            "where Character = '{}' and B.Job = 1".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_multiple_profession(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "Select count(*) as Total " \
            "From Link_Character_Skills A " \
            "Left Join Info_Skills B " \
            "On A.Skill = B.Name " \
            "where Character = '{}' and B.Job = 1".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Total > 1:
        return True
    return False


def profession_has_multiple_choice(profession: str):
    cursor = Quick_SQL.db_connection()
    query = "select A.Name, B.Total as Mundane, C.Total as Recipe " \
            "from Info_Skills A  " \
            "Left join (select Crafting, count(crafting) as Total from Info_Item where Crafting is not null group by Crafting) B on A.Name = B.Crafting " \
            "left join (select Skill, count(skill) as Total from Info_Crafting_Recipes group by skill) C on A.Name = C.Skill " \
            " where A.Job = 1 and A.Name = '{}'".format(profession)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Mundane is not None and result.Recipe is not None:
        return True
    return False
