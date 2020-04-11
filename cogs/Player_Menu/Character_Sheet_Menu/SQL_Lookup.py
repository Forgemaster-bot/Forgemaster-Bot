import Connections


def character_count_classes(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select Count(*) Total from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def character_class_by_number(character_name: str, number: int):
    cursor = Connections.sql_db_connection()
    query = "Select Class " \
            "From Link_Character_Class " \
            "Where Character = '{}' and Number = '{}'".format(character_name, number)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Class


def character_sum_class_levels(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select SUM(Level) Total from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def character_xp(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.XP


def character_stats(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select " \
            "Strength as STR," \
            "Dexterity as DEX, " \
            "Constitution as CON, " \
            "Intelligence as INT, " \
            "Wisdom as WIS, " \
            "Charisma as CHA " \
            "From Main_Characters " \
            "where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    results = cursor.fetchone()
    return results


def character_class_and_levels(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Link_Character_Class " \
            "Where Character = '{}' " \
            "Order by Level,Number".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    response = []
    for row in rows:
        if row.Sub_Class is None:
            response.append("{} : {}".format(row.Class, row.Level))
        else:
            response.append("{} {}: {}".format(row.Class, row.Sub_Class, row.Level))
    return response


def character_class_list(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select distinct Class from Link_Character_Class where Character = '{}'".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    response = []
    for row in rows:
        response.append(row.Class)
    return response


def character_class_level_by_class(character_name: str, character_class: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Class " \
            "where Character='{}' and Class = '{}'".format(character_name, character_class)
    cursor.execute(query)
    class_lookup = cursor.fetchone()
    return class_lookup.Level


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


def info_skills():
    cursor = Connections.sql_db_connection()
    query = "select Name from Info_Skills Where Job = 'True' ORDER BY Name"
    cursor.execute(query)
    rows = cursor.fetchall()
    skills = []
    for row in rows:
        skills.append(row.Name)
    return skills


def info_classes():
    cursor = Connections.sql_db_connection()
    query = "select Class from Info_Classes group by Class ORDER BY Class"
    cursor.execute(query)
    rows = cursor.fetchall()
    classes = []
    for row in rows:
        classes.append(row.Class)
    return classes


def subclasses(class_choice: str):
    cursor = Connections.sql_db_connection()
    query = "Select Sub_Class from Info_Subclass " \
            "Where Class = '{}'" \
            "ORDER BY Sub_Class".format(class_choice)
    cursor.execute(query)
    rows = cursor.fetchall()
    classes = []
    for row in rows:
        classes.append(row.Sub_Class)
    return classes


def character_feats(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Link_Character_Feats where Character='{}'".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    feats = []
    for row in rows:
        feats.append(row.Feat)
    return feats


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
