import Quick_SQL

'''''''''''''''''''''''''''''''''''''''''
############Info_Discord###############
'''''''''''''''''''''''''''''''''''''''''


def player_name_by_id(user_id: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Info_Discord where ID= '{}'".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def player_id_by_name(name: str):
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


'''''''''''''''''''''''''''''''''''''''''
############Main_character###############
'''''''''''''''''''''''''''''''''''''''''


def character_list(discord_id: str):
    cursor = Quick_SQL.db_connection()
    query = "select Character_Name from Main_Characters where Discord_ID = '{}'".format(discord_id)
    cursor.execute(query)
    rows = cursor.execute(query)
    response = []
    for row in rows:
        response.append(row.Character_Name)
    return response


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


'''''''''''''''''''''''''''''''''''''''''
###########Link_Character_Items##########
'''''''''''''''''''''''''''''''''''''''''


def character_item_quantity(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Link_Character_Items where Character='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item.Quantity


def character_inventory(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Link_Character_Items where Character='{}' order by Item".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


'''''''''''''''''''''''''''''''''''''''''
###########Link_Character_Class##########
'''''''''''''''''''''''''''''''''''''''''


def character_class_by_order(character_name: str, order: int):
    cursor = Quick_SQL.db_connection()
    query = "select * from Link_Character_Class where Character='{}' and Number = '{}'".format(character_name, order)
    cursor.execute(query)
    class_lookup = cursor.fetchone()
    return class_lookup.Class, class_lookup.Level


def character_class_level_by_class(character_name: str, character_class: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Link_Character_Class " \
            "where Character='{}' and Class = '{}'".format(character_name, character_class)
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


def shop_item(item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Info_Item where Name = '{}'".format(item_name)
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


def log_xp(level: int):
    cursor = Quick_SQL.db_connection()
    query = "select * from Info_XP Where Level = {}".format(level)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.XP_To_Level/20


'''''''''''''''''''''''''''''''''''''''''
###########Crafting##############
'''''''''''''''''''''''''''''''''''''''''


def character_crafting_points(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "Select * " \
            "From Main_Crafting " \
            "Where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    response = cursor.fetchone()
    return response


def character_skill_profession(character_name: str):
    cursor = Quick_SQL.db_connection()

    query = "Select A.Skill " \
            "From Link_Character_Skills A " \
            "Left Join Info_Skills B " \
            "On A.Skill = B.Name " \
            "left join Link_Character_Items C " \
            "on B.Tools = C.Item " \
            "where A.Character = '{}' and C.Character = '{}' and B.Job = 1 " \
            "order by A.Skill ".format(character_name, character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    skill_list = []
    for row in rows:
        skill_list.append(row.Skill)
    return skill_list


def profession_item_list(profession: str, item_type: str, gold: float):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Info_Item " \
            "Where Crafting = '{}' and Type = '{}' and Value <= '{}' " \
            "order by Type,Name".format(profession, item_type, gold*2)
    cursor.execute(query)
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append(row.Name)
    return results


def profession_item_type_list(profession: str, gold: float):
    cursor = Quick_SQL.db_connection()
    query = "Select Type from Info_Item " \
            "Where Crafting = '{}' and Value <= '{}' " \
            "group by Type order by Type".format(profession, gold*2)
    cursor.execute(query)
    rows = cursor.fetchall()
    item_types = []
    for row in rows:
        item_types.append(row.Type)
    return item_types


def item_detail(item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "Select * " \
            "From Info_Item " \
            "Where Name = '{}' ".format(item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def profession_choice(skill: str):
    cursor = Quick_SQL.db_connection()
    query = "Select Craft " \
            "From Link_Skills_Recipies " \
            "Where Skill = '{}'" \
            "Order by craft".format(skill)
    cursor.execute(query)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row.Craft)
    return result


'''''''''''''''''''''''''''''''''''''''''
##############Main_Trade#################
'''''''''''''''''''''''''''''''''''''''''


def trade_item(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * from Main_Trade where Character='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


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


def trade_sellers_list(character_name: str, price: float):
    cursor = Quick_SQL.db_connection()
    query = "select Distinct Character " \
            "from Main_Trade " \
            "where Character != '{}' and Price <= '{}' " \
            "order by Character".format(character_name, price)
    cursor.execute(query)
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append(row.Character)
    return result


def trade_seller_item_list(character_name: str, price: float):
    cursor = Quick_SQL.db_connection()
    query = "select Item, Price " \
            "from Main_Trade " \
            "where Character = '{}' and Price <= '{}' " \
            "order by Item".format(character_name, price)
    cursor.execute(query)
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append("{} - {}g".format(row.Item, row.Price))
    return result


def character_inventory_sell_list(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character='{}' and Item not in (select Item from Main_Trade where Character = '{}') " \
            "order by Item".format(character_name,character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items
