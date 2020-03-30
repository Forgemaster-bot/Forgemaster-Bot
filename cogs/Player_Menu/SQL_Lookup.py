import Connections


def character_gold_total(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.Gold


def character_item_quantity(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Link_Character_Items where Character='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item.Quantity


def character_inventory(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Link_Character_Items " \
            "Where Character='{}' and Item not in (select Item from Main_Trade where Character = '{}') " \
            "Order by Item".format(character_name, character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


def character_inventory_essence(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character='{}' and Item in (select Name from Info_Item where Type = 'Essence') " \
            "order by Item".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


def character_inventory_essence_count(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character='{}' and Item in (select Name from Info_Item where Type = 'Essence') " \
            "order by Item".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    essence = 0
    for row in rows:
        essence = essence + row.Quantity
    return essence


def character_sellable_inventory_list(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character='{}' and Item in (select Name from Info_Item) " \
            "order by Item".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


def character_main_crafting(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Main_Crafting " \
            "Where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    response = cursor.fetchone()
    return response


def character_profession_list(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select Skill " \
            "From Link_Character_Skills " \
            "Where Character = '{}'" \
            "Order by Skill".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    skill_list = []
    for row in rows:
        skill_list.append(row.Skill)
    return skill_list


def character_sum_class_levels(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select SUM(Level) Total from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def character_owner(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return int(result.Discord_ID)


def character_xp(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.XP


def item_detail(item_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Item " \
            "Where Name = '{}' ".format(item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def item_value(item_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Item " \
            "Where Name = '{}' ".format(item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item.Value


def player_character_list(discord_id: str):
    cursor = Connections.sql_db_connection()
    query = "select Character_Name from Main_Characters where Discord_ID = '{}'".format(discord_id)
    cursor.execute(query)
    rows = cursor.execute(query)
    response = []
    for row in rows:
        response.append(row.Character_Name)
    return response


def profession_craft_options(profession: str):
    cursor = Connections.sql_db_connection()
    query = "Select Craft " \
            "From Link_Skills_Recipies " \
            "Where Skill = '{}'" \
            "Order by craft".format(profession)
    cursor.execute(query)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row.Craft)
    return result


def profession_item_type_list(profession: str, gold_limit: float):
    cursor = Connections.sql_db_connection()
    gold_value = gold_limit * 2
    query = "Select Type from Info_Item " \
            "Where Crafting = '{}' and Value <= '{}' " \
            "group by Type order by Type".format(profession, gold_value)
    cursor.execute(query)
    rows = cursor.fetchall()
    item_types = []
    for row in rows:
        item_types.append(row.Type)
    return item_types


def profession_item_list(profession: str, item_type: str, gold: float):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_Item " \
            "Where Crafting = '{}' and Type = '{}' and Value <= '{}' " \
            "order by Name".format(profession, item_type, gold*2)
    cursor.execute(query)
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append(row.Name)
    return results


def profession_tool(profession: str):
    cursor = Connections.sql_db_connection()
    query = "select Tools " \
            "from Info_Skills " \
            "Where Name = '{}'".format(profession)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Tools


def character_count_classes(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select Count(*) Total from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def character_class_list(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select distinct Class from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    response = []
    for row in rows:
        response.append(row.Class)
    return response


def info_classes():
    cursor = Connections.sql_db_connection()
    query = "select Name from Info_Classes ORDER BY Name"
    cursor.execute(query)
    rows = cursor.fetchall()
    classes = []
    for row in rows:
        classes.append(row.Name)
    return classes


def info_skills():
    cursor = Connections.sql_db_connection()
    query = "select Name from Info_Skills Where Job = 'True' ORDER BY Name"
    cursor.execute(query)
    rows = cursor.fetchall()
    skills = []
    for row in rows:
        skills.append(row.Name)
    return skills


def character_class_and_levels(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select Class, Level " \
            "From Link_Character_Class " \
            "Where Character = '{}' " \
            "Order by Level,Number".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    response = []
    for row in rows:
        response.append("{}/{}".format(row.Class, row.Level))
    return response


def character_class_level_by_class(character_name: str, character_class: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Class " \
            "where Character='{}' and Class = '{}'".format(character_name, character_class)
    cursor.execute(query)
    class_lookup = cursor.fetchone()
    return class_lookup.Level


def trade_goods_types(character_name: str, gold_limit: float):
    cursor = Connections.sql_db_connection()
    query = "Select distinct b.Type " \
            "From Main_Trade a " \
            "Left join Info_Item b " \
            "On a.Item = b.Name " \
            "Where a.Price <= '{}' and a.Character != '{}' " \
            "Order by Type".format(gold_limit, character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    response = []
    for row in rows:
        if row.Type is None:
            response.append("Other")
        else:
            response.append(row.Type)
    response.sort()
    return response


def trade_goods_items_by_type(character_name: str, gold_limit: float, item_type: str):
    cursor = Connections.sql_db_connection()
    if item_type == "Other":
        query = "select a.Item " \
                "from Main_Trade a " \
                "left join Info_Item b " \
                "on a.Item = b.Name " \
                "where b.Type is null and a.price <= '{}' and a.Character != '{}' " \
                "group by a.Item " \
                "order by Item".format(gold_limit, character_name)
    else:
        query = "select a.Item " \
                "from Main_Trade a " \
                "left join Info_Item b " \
                "on a.Item = b.Name " \
                "where b.Type = '{}' and a.price <= '{}' " \
                "group by a.Item " \
                "order by Item".format(item_type, gold_limit)
    cursor.execute(query)
    item_name_list = cursor.fetchall()
    response = []
    for items in item_name_list:
        item_details = trade_item_not_sold_by_character(character_name, items.Item)
        if item_details is not None:
            response.append("{}: {}g each with {} for sale".format(item_details.Item, item_details.Price,
                                                                   item_details.Quantity))
    return response


def trade_item_not_sold_by_character(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Main_Trade " \
            "Where Item = '{}' and Character != '{}' " \
            "order by Price, Quantity desc".format(item_name, character_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def trade_item_sold_by_character(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Main_Trade " \
            "Where Item = '{}' and Character = '{}' " \
            "order by Price, Quantity desc".format(item_name, character_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def trade_item_cheapest_on_sale(item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Main_Trade " \
            "Where Item = '{}' " \
            "order by Price, Quantity desc".format(item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def character_items_for_trade(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select Item, Price " \
            "from Main_Trade " \
            "where Character = '{}' " \
            "order by Item".format(character_name)
    cursor.execute(query)
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append("{} - {}g".format(row.Item, row.Price))
    return result


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


def player_name_by_id(user_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Info_Discord where ID= '{}'".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def recipe_by_essence(profession: str, essence_1: str, essence_2):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Crafting_Recipes " \
            "Where Skill = '{}' and Essence_1 = '{}' and Essence_2 = '{}'".format(profession, essence_1, essence_2)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def recipe_essence_list(profession: str, name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Crafting_Recipes " \
            "Where Skill = '{}' and Name = '{}' ".format(profession, name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Essence_1, result.Essence_2


def recipe_essence_and_description_list(profession: str, name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Crafting_Recipes " \
            "Where Skill = '{}' and Name = '{}' ".format(profession, name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Essence_1, result.Essence_2, result.Short_Description


def recipe_by_profession(profession: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Crafting_Recipes " \
            "Where Skill = '{}'".format(profession)
    cursor.execute(query)
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append(row.Name)
    return result


def character_known_recipe(character_name: str, profession: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Link_Character_Recipe " \
            "Where character = '{}' and Skill = '{}'".format(character_name, profession)
    cursor.execute(query)
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append(row.Recipe)
    return result


def profession_consumable_name(profession: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Skills " \
            "Where Name = '{}'".format(profession)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Consumable_Name


def character_known_recipe_details(character_name: str, profession: str):
    cursor = Connections.sql_db_connection()
    query = "Select b.Name,b.Description,b.Essence_1, b.Essence_2 " \
            "From Link_Character_Recipe a " \
            "left join Info_Crafting_Recipes b " \
            "on a.Recipe = b.Name and a.Skill = b.Skill " \
            "Where a.character = '{}' and a.Skill = '{}'".format(character_name, profession)
    cursor.execute(query)
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append("{} : {} : **{}** : **{}** ".format(row.Name, row.Description, row.Essence_1, row.Essence_2))
    return result
