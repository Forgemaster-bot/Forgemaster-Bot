from Player_Menu.Character_Sheet_Menu import SQL_Lookup
import Connections


def character_on_crafting_table(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Crafting " \
            "where Character_ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_is_artificer_with_tools(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select A.Character_ID, A.Class, B.Item from " \
            "(select Character_ID, Class " \
            "from Link_Character_Class " \
            "where Character_ID = '{}' and Class = 'Artificer' and Level > 2) A " \
            "left join  " \
            "(select Character_ID, Item " \
            "from Link_Character_Items " \
            "where Character_ID = '{}' and Item = 'Tinker tools') B " \
            "on a.Character_Id = B.Character_ID".format(character_id, character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_item(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character_ID = '{}' AND Item = '{}'".format(character_id, item_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_item_quantity(character_id: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character_ID = '{}' AND Item = '{}' AND Quantity >= '{}'".format(character_id, item_name, quantity)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_crafted_this_week(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Crafting " \
            "where Character_ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return True
    if result.Crafting_Value != 50:
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

    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Info_Max_Spell_Level " \
            "where Class = '{}'".format(class_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    if result[class_level] > 0:
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


def wizard_has_spells(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select count(*) as Total " \
            "from Main_Spell_Book A " \
            "left join Link_Spell_book_Spells B " \
            "on A.ID = B.Spell_Book_ID " \
            "where Owner_ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Total > 0:
        return True
    return False


def character_has_spells_by_class(character_id: str, class_name: str):
    sub_class = SQL_Lookup.character_class_subclass(character_id, class_name)
    cursor = Connections.sql_db_connection()
    query = "select count(*) as Total " \
            "from Link_Character_Spells A " \
            "left Join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where Character_ID = '{}' and (Origin = '{}' or Origin = '{}')" \
        .format(character_id, class_name, sub_class)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Total > 0:
        return True
    return False


def character_has_tome(character_id):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Spell_Book " \
            "where Owner_ID = '{}' and Type = 'Tome'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True

