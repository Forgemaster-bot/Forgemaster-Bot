from Player_Menu.Character_Sheet_Menu import SQL_Lookup
import Connections
from Quick_Python import run_query


def character_can_level_up(character_level: int, character_xp: int):
    query = "select * " \
            "from Info_XP " \
            "where Level=?"
    cursor = run_query(query, [character_level])
    xp_sheet = cursor.fetchone()
    if character_xp >= xp_sheet.XP:
        return True
    return False


def character_can_subclass(character_id: str, class_name: str):
    query = "select a.Class,a.Level,B.Sub_Class_Level,A.Sub_Class " \
            "from ( " \
            "select Class,level, Sub_Class " \
            "from Link_Character_Class  " \
            "where Character_ID = ? and Class = ? " \
            ") a " \
            "left join ( " \
            "select Class, Sub_Class_Level from Info_Classes " \
            "where Class = ?" \
            "group by Class, Sub_Class_Level) b " \
            "on a.Class = b.Class"
    cursor = run_query(query, [character_id, class_name, class_name])
    result = cursor.fetchone()
    if result.Sub_Class is None:
        if result.Level >= result.Sub_Class_Level:
            return True
    return False


def character_has_professions(character_id: str):
    query = "select * " \
            "from Link_Character_Skills " \
            "where Character_ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_class(character_id: str, class_name: str):
    query = "select * " \
            "from Link_Character_Class " \
            "where Character_ID = ? AND Class = ?"
    cursor = run_query(query, [character_id, class_name])
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def class_is_spell_caster(character_id: str, class_name: str, class_level: int):
    if class_name == 'Rogue':
        if SQL_Lookup.character_class_subclass(character_id, class_name) == "Arcane Trickster":
            return True
        else:
            return False
    if class_name == 'Fighter':
        if SQL_Lookup.character_class_subclass(character_id, class_name) == "Eldritch Knight":
            return True
        else:
            return False

    query = "select * " \
            "from Info_Max_Spell_Level " \
            "where Class = ?"
    cursor = run_query(query, [class_name])
    result = cursor.fetchone()
    if result is None:
        return False
    if result[class_level] > 0:
        return True
    return False


def wizard_has_spells(character_id: str):
    query = "select count(*) as Total " \
            "from Main_Spell_Book A " \
            "left join Link_Spell_book_Spells B " \
            "on A.ID = B.Spell_Book_ID " \
            "where Owner_ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    if result.Total > 0:
        return True
    return False


def class_learn_spells(class_name: str):
    query = "select * " \
            "from Info_Spells_Known " \
            "where Class = ?"
    cursor = run_query(query, [class_name])
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_spells_by_class(character_id: str, class_name: str):
    sub_class = SQL_Lookup.character_class_subclass(character_id, class_name)
    query = "select count(*) as Total " \
            "from Link_Character_Spells A " \
            "left Join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where A.Character_ID = ? and (Origin = ? or Origin = ?)" \
        
    cursor = run_query(query, [character_id, class_name, sub_class])
    result = cursor.fetchone()
    if result.Total > 0:
        return True
    return False


def character_class_can_replace_spell(character_id: str, class_name: str):
    query = "Select *" \
            "From Link_Character_Class " \
            "Where Character_ID = ? and Class = ?"
    cursor = run_query(query, [character_id, class_name])
    result = cursor.fetchone()
    if result.Replace_Spell:
        return True
    return False


def class_can_replace_spell(class_name: str):
    query = "Select *" \
            "From Info_Spells_Known " \
            "Where Class = ?"
    cursor = run_query(query, [class_name])
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def class_choice(character_id: str, class_name: str):
    query = "Select * " \
            "From Link_Character_Class " \
            "Where Character_ID = ? and Class = ?"
    cursor = run_query(query, [character_id, class_name])
    result = cursor.fetchone()
    if result.Class_Choice:
        return True
    return False
