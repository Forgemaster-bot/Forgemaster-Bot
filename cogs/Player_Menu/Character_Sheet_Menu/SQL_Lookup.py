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
            "Strength as STR, " \
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
            "Order by Level desc,Number ".format(character_name)
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
            "Order by Item ".format(character_name, character_name)
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
    query = "select Name from Info_Skills Where Job = 'True' ORDER BY Name "
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
            "Where Class = '{}' " \
            "ORDER BY Sub_Class ".format(class_choice)
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


def character_max_spell_by_level(class_name: str, class_level):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_Max_Spell_Level " \
            "where Class = '{}'".format(class_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result[class_level]


def character_class_subclass(character_name: str, subclass: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "from Link_character_Class " \
            "where Character = '{}' and Class = '{}' ".format(character_name, subclass)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Sub_Class


def character_spells_by_class(character_name: str, class_name: str):
    sub_class = character_class_subclass(character_name, class_name)
    cursor = Connections.sql_db_connection()
    query = "select B.* " \
            "from Link_Character_Spells A " \
            "left Join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where Character_name = '{}' and (Origin = '{}' or Origin = '{}') " \
            "order by Level, Name ".format(character_name, class_name, sub_class)
    cursor.execute(query)
    rows = cursor.fetchall()
    return_list = []
    for row in rows:
        return_list.append("Level {} Spell : {}".format(row.Level, row.Name))
    return return_list


def character_spells_in_book(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select C.* " \
            "from Link_Spell_Book_Spells A " \
            "left join Main_Spell_Book B " \
            "on A.Spell_Book_ID = B.ID " \
            "left join Info_Spells C " \
            "on A.Spell = C.Name " \
            "Where Owner = '{}' " \
            "order by Level, Name ".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    return_list = []
    for row in rows:
        return_list.append("Level {} Spell : {}".format(row.Level, row.Name))
    return return_list


def character_known_spells_by_class(character_name: str, class_name: str):
    sub_class = character_class_subclass(character_name, class_name)
    cursor = Connections.sql_db_connection()
    query = "select count(*) as Total " \
            "from Link_Character_Spells A " \
            "left Join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where Character_name = '{}' and (Origin = '{}' or Origin = '{}')"\
        .format(character_name, class_name, sub_class)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Total


def spells_wizard_free_spells(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Class " \
            "where Character='{}' and Class = 'Wizard' ".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return 0
    if result.Free_Wizard_Spells is None:
        return 0
    return result.Free_Wizard_Spells


def spells_known_by_level(class_name: str, class_level: int):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Spells_Known " \
            "Where Class = '{}'".format(class_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result[class_level + 1]


def class_spells_by_level(class_name: str, sub_class: str, level: int):
    cursor = Connections.sql_db_connection()
    query = "select b.* " \
            "from Link_Class_Spells A " \
            "left join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where Level = '{}' and (Class = '{}' or Class = '{}') " \
            "order by name".format(level, class_name, sub_class)
    cursor.execute(query)
    rows = cursor.fetchall()
    return_list = []
    for row in rows:
        return_list.append(row.Name)
    return return_list


def class_spells_at_and_below_level(class_name: str, level: int):
    cursor = Connections.sql_db_connection()
    query = "select b.* " \
            "from Link_Class_Spells A " \
            "left join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where Level <= '{}' and Class = '{}' " \
            "order by name".format(level, class_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    return_list = []
    for row in rows:
        return_list.append(row.Name)
    return return_list


def character_known_wizard_spells_by_level(character_name: str, spell_level: int):
    cursor = Connections.sql_db_connection()
    query = "Select Spell " \
            "From Main_Spell_Book A " \
            "Left join Link_Spell_book_Spells B " \
            "on A.ID = B.Spell_Book_ID " \
            "left join Info_Spells C " \
            "on B.Spell = C.Name " \
            "Where A.owner = '{}' and C.Level = '{}'".format(character_name, spell_level)
    cursor.execute(query)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row.Spell)
    return result


def character_known_spells_by_class_and_level(character_name: str, class_name: str, spell_level: int):
    sub_class = character_class_subclass(character_name, class_name)
    cursor = Connections.sql_db_connection()
    query = "select Spell " \
            "from Link_Character_Spells A " \
            "left Join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where Character_name = '{}' " \
            "and B.Level = {} " \
            "and (Origin = '{}' or Origin = '{}') "\
        .format(character_name, spell_level, class_name, sub_class)
    cursor.execute(query)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row.Spell)
    return result


def spell_book(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Spell_book " \
            "Where Owner = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.ID


def spell_origin(class_name: str, spell_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Link_Class_Spells " \
            "Where Class = '{}' and Spell = '{}'".format(class_name, spell_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return None
    return result.Class


def wizard_spell_number(character_name: str, class_name: str, ):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Link_Character_Class " \
            "WHERE Character = '{}' AND Class = '{}'".format(character_name, class_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Free_Wizard_Spells
