import Connections


def character_skills(character_name: str):
    cursor = Connections.sql_db_connection()
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


def character_essences(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character= '{}' " \
            "and item in ( select Name from Info_Item where Type = 'Essence') " \
            "order by Item".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    essences = []
    for row in rows:
        if row.Quantity == 1:
            essences.append(row.Item)
        else:
            essences.append(row.Item + " ({})".format(row.Quantity))
    return essences


def character_gold(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.Gold


def character_crafting(character_name: str):
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
    profession_list = []
    for row in rows:
        profession_list.append(row.Skill)
    return profession_list


def profession_tool(profession: str):
    cursor = Connections.sql_db_connection()
    query = "select Tools " \
            "from Info_Skills " \
            "Where Name = '{}'".format(profession)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Tools


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


def item_value(item_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Item " \
            "Where Name = '{}' ".format(item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item.Value


def character_item_quantity(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Link_Character_Items where Character='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item.Quantity


def profession_consumable_name(profession: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Skills " \
            "Where Name = '{}'".format(profession)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Consumable_Name


def recipe_essence_list(profession: str, name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Crafting_Recipes " \
            "Where Skill = '{}' and Name = '{}' ".format(profession, name)
    cursor.execute(query)
    result = cursor.fetchone()
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


def recipe(profession: str, name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Crafting_Recipes " \
            "Where Skill = '{}' and Name = '{}' ".format(profession, name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result


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


def profession_recipes(profession: str):
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


def character_owner(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return int(result.Discord_ID)
