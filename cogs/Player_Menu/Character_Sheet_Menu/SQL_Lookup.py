import Connections
from Quick_Python import run_query


def character_count_classes(character_id: str):
    query = "select Count(*) Total " \
            "From Link_Character_Class " \
            "Where Character_ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return result.Total


def character_class_by_number(character_id: str, number: int):
    query = "Select Class " \
            "From Link_Character_Class " \
            "Where Character_ID = ? and Number = ?"
    cursor = run_query(query, [character_id, number])
    result = cursor.fetchone()
    return result.Class


def character_sum_class_levels(character_id: str):
    query = "select SUM(Level) Total " \
            "from Link_Character_Class " \
            "where Character_ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return result.Total


def character_xp(character_id: str):
    query = "Select * " \
            "From Main_Characters " \
            "Where ID = ?"
    cursor = run_query(query, [character_id])
    character = cursor.fetchone()
    return character.XP


def character_stats(character_id: str):
    query = "select " \
            "Strength as STR, " \
            "Dexterity as DEX, " \
            "Constitution as CON, " \
            "Intelligence as INT, " \
            "Wisdom as WIS, " \
            "Charisma as CHA " \
            "From Main_Characters " \
            "where ID = ?"
    cursor = run_query(query, [character_id])
    results = cursor.fetchone()
    return results


def character_class_and_levels(character_id: str):
    query = "Select * " \
            "From Link_Character_Class " \
            "Where Character_ID = ? " \
            "Order by Level desc, Number "
    cursor = run_query(query, [character_id])
    rows = cursor.fetchall()
    response = []
    for row in rows:
        if row.Sub_Class is None:
            response.append("{} : {}".format(row.Class, row.Level))
        else:
            response.append("{} {}: {}".format(row.Class, row.Sub_Class, row.Level))
    return response


def character_class_list(character_id: str):
    query = "Select distinct Class " \
            "From Link_Character_Class " \
            "Where Character_ID = ?"
    cursor = run_query(query, [character_id])
    rows = cursor.fetchall()
    response = []
    for row in rows:
        response.append(row.Class)
    return response


def character_class_level_by_class(character_id: str, character_class: str):
    query = "select * " \
            "from Link_Character_Class " \
            "where Character_ID = ? and Class = ?"
    cursor = run_query(query, [character_id, character_class])
    class_lookup = cursor.fetchone()
    return class_lookup.Level


def character_inventory(character_id: str):
    query = "Select * " \
            "From Link_Character_Items " \
            "Where Character_ID = ? " \
            "Order by Item "
    cursor = run_query(query, [character_id])
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


def info_skills():
    query = "select Name from Info_Skills Where Job = 'True' ORDER BY Name "
    cursor = run_query(query)
    rows = cursor.fetchall()
    skills = []
    for row in rows:
        skills.append(row.Name)
    return skills


def info_classes():
    query = "select Class from Info_Classes group by Class ORDER BY Class"
    cursor = run_query(query)
    rows = cursor.fetchall()
    classes = []
    for row in rows:
        classes.append(row.Class)
    return classes


def subclasses(class_choice: str):
    query = "Select Sub_Class from Info_Subclass " \
            "Where Class = ? " \
            "ORDER BY Sub_Class "
    cursor = run_query(query, [class_choice])
    rows = cursor.fetchall()
    classes = []
    for row in rows:
        classes.append(row.Sub_Class)
    return classes


def character_feats(character_id: str):
    query = "Select * " \
            "From Link_Character_Feats " \
            "Where Character_ID = ?"
    cursor = run_query(query, [character_id])
    rows = cursor.fetchall()
    feats = []
    for row in rows:
        feats.append(row.Feat)
    return feats


def character_skills(character_id: str):
    query = "Select * " \
            "From Link_Character_Skills " \
            "Where Character_ID = ?"
    cursor = run_query(query, [character_id])
    rows = cursor.fetchall()
    skills = []
    for row in rows:
        if row.Proficiency == 1:
            skills.append(row.Skill)
        else:
            skills.append(row.Skill + " (D)")
    return skills


def character_max_spell_by_level(class_name: str, class_level):
    query = "select * " \
            "from Info_Max_Spell_Level " \
            "where Class = ?"
    cursor = run_query(query, [class_name])
    result = cursor.fetchone()
    return result[class_level]


def character_class_subclass(character_id: str, class_name: str):
    query = "Select * " \
            "from Link_character_Class " \
            "where Character_ID = ? and Class = ? "
    cursor = run_query(query, [character_id, class_name])
    result = cursor.fetchone()
    return result.Sub_Class


def character_spells_by_class(character_id: str, class_name: str):
    sub_class = character_class_subclass(character_id, class_name)
    sub_class = str(sub_class) + "%"
    character_name = character_name_by_character_id(character_id)
    query = "select B.* " \
            "from Link_Character_Spells A " \
            "left Join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where A.Character_ID = ? and (Origin = ? or Origin like ?) " \
            "order by Level, Name "
    cursor = run_query(query, [character_id, class_name, sub_class])
    rows = cursor.fetchall()
    # TODO: Determine if return_list should mention '<character_name> <class_name> spell list'
    # return_list = ["{} {} spell list".format(character_name, class_name)]
    return_list = []
    for row in rows:
        if row.Name is not None:
            return_list.append("Level {} Spell : {}".format(row.Level, row.Name))
    return return_list


def character_spells_in_book(character_id: str):
    query = "select C.* " \
            "from Link_Spell_Book_Spells A " \
            "left join Main_Spell_Book B " \
            "on A.Spell_Book_ID = B.ID " \
            "left join Info_Spells C " \
            "on A.Spell = C.Name " \
            "Where B.Owner_ID = ? and B.Type = 'Core' " \
            "order by C.Level, C.Name "
    cursor = run_query(query, [character_id])
    rows = cursor.fetchall()
    return_list = []
    for row in rows:
        return_list.append("Level {} Spell : {}".format(row.Level, row.Name))
    return return_list


def character_known_spells_by_class(character_id: str, class_name: str):
    sub_class = character_class_subclass(character_id, class_name)
    query = "select count(*) as Total " \
            "from Link_Character_Spells A " \
            "left Join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where A.Character_ID = ? and (Origin = ? or Origin = ?)"
        
    cursor = run_query(query, [character_id, class_name, sub_class])
    result = cursor.fetchone()
    return result.Total


def spells_wizard_free_spells(character_id: str):
    query = "select * " \
            "from Link_Character_Class " \
            "where Character_ID = ? and Class = 'Wizard' "
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    if result is None:
        return 0
    if result.Free_Book_Spells is None:
        return 0
    return result.Free_Book_Spells


def spells_known_by_level(class_name: str, class_level: int):
    query = "Select * " \
            "From Info_Spells_Known " \
            "Where Class = ?"
    cursor = run_query(query, [class_name])
    result = cursor.fetchone()
    return result[class_level]


def class_spells_by_level(class_name: str, sub_class: str, level: int):
    query = "select b.* " \
            "from Link_Class_Spells A " \
            "left join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where Level = ? and (Class = ? or Class = ?) " \
            "order by name"
    cursor = run_query(query, [level, class_name, sub_class])
    rows = cursor.fetchall()
    return_list = []
    for row in rows:
        return_list.append(row.Name)
    return return_list


def class_spells_at_and_below_level(class_name: str, level: int):
    query = "select b.* " \
            "from Link_Class_Spells A " \
            "left join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where Level <= ? and Class = ? " \
            "order by name"
    cursor = run_query(query, [level, class_name])
    rows = cursor.fetchall()
    return_list = []
    for row in rows:
        return_list.append(row.Name)
    return return_list


def character_known_wizard_spells_by_level(character_id: str, spell_level: int):
    query = "Select Spell " \
            "From Main_Spell_Book A " \
            "Left join Link_Spell_book_Spells B " \
            "on A.ID = B.Spell_Book_ID " \
            "left join Info_Spells C " \
            "on B.Spell = C.Name " \
            "Where A.Owner_ID = ? and A.Type = 'Core' and C.Level = ?"
    cursor = run_query(query, [character_id, spell_level])
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row.Spell)
    return result


def character_known_spells_by_class_and_level(character_id: str, class_name: str, spell_level: int):
    sub_class = character_class_subclass(character_id, class_name)
    query = "select Spell " \
            "from Link_Character_Spells A " \
            "left Join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where A.Character_ID = ? " \
            "and B.Level = ? " \
            "and (Origin = ? or Origin = ?) "\
        
    cursor = run_query(query, [character_id, spell_level, class_name, sub_class])
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row.Spell)
    return result


def spell_book(character_id: str):
    query = "select * " \
            "from Main_Spell_book " \
            "Where Owner_ID = ? and Type = 'Core'"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return result.ID


def spell_origin(class_name: str, spell_name: str):
    query = "Select * " \
            "From Link_Class_Spells " \
            "Where Class = ? and Spell = ?"
    cursor = run_query(query, [class_name, spell_name])
    result = cursor.fetchone()
    if result is None:
        return None
    return result.Class


def wizard_spell_number(character_id: str, class_name: str, ):
    query = "select * " \
            "From Link_Character_Class " \
            "WHERE Character_ID = ? AND Class = ?"
    cursor = run_query(query, [character_id, class_name])
    result = cursor.fetchone()
    return result.Free_Book_Spells


def character_name_by_character_id(character_id: str):
    query = "Select * " \
            "From Main_Characters " \
            "Where ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return result.Character_Name
