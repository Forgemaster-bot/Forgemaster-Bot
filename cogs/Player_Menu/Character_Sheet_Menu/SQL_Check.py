from Player_Menu.Character_Sheet_Menu import SQL_Lookup
import Connections


def character_can_level_up(character_level:int, character_xp: int):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_XP " \
            "where Level='{}'".format(character_level)
    cursor.execute(query)
    xp_sheet = cursor.fetchone()
    if character_xp >= xp_sheet.XP:
        return True
    return False


def character_can_subclass(character_name: str, class_name: str):
    cursor = Connections.sql_db_connection()
    query = "select a.Class,a.Level,B.Sub_Class_Level,A.Sub_Class " \
            "from ( " \
            "select Class,level, Sub_Class " \
            "from Link_Character_Class  " \
            "where Character = '{}' and Class = '{}' " \
            ") a " \
            "left join ( " \
            "select Class, Sub_Class_Level from Info_Classes " \
            "where Class = '{}'" \
            "group by Class, Sub_Class_Level) b " \
            "on a.Class = b.Class".format(character_name, class_name, class_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Sub_Class is None:
        if result.Level >= result.Sub_Class_Level:
            return True
    return False


def character_has_professions(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Skills " \
            "where Character = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_class(character_name: str, class_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Class " \
            "where Character = '{}' AND Class = '{}'".format(character_name, class_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def class_is_spell_caster(character_name: str, class_name: str, class_level: int):
    if class_name == 'Rogue':
        if SQL_Lookup.character_class_subclass(character_name, class_name) == "Arcane Trickster":
            return True
        else:
            return False
    if class_name == 'Fighter':
        if SQL_Lookup.character_class_subclass(character_name, class_name) == "Eldritch Knight":
            return True
        else:
            return False

    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_Max_Spell_Level " \
            "where Class = '{}'".format(class_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    if result[class_level + 1] > 0:
        return True
    return False


def wizard_has_spells(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select count(*) as Total " \
            "from Main_Spell_Book A " \
            "left join Link_Spell_book_Spells B " \
            "on A.ID = B.Spell_Book_ID " \
            "where Owner = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Total > 0:
        return True
    return False


def class_learn_spells(class_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_Spells_Known " \
            "where Class = '{}'".format(class_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_spells_by_class(character_name: str, class_name: str):
    sub_class = SQL_Lookup.character_class_subclass(character_name, class_name)
    cursor = Connections.sql_db_connection()
    query = "select count(*) as Total " \
            "from Link_Character_Spells A " \
            "left Join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where Character_name = '{}' and (Origin = '{}' or Origin = '{}')" \
        .format(character_name, class_name, sub_class)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Total > 0:
        return True
    return False


def character_class_can_replace_spell(character_name: str, class_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select *" \
            "From Link_Character_Class " \
            "Where Character = '{}' and Class = '{}'".format(character_name, class_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Replace_Spell:
        return True
    return False
