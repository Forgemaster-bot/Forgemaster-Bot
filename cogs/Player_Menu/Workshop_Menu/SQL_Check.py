import Connections


def character_on_crafting_table(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Crafting " \
            "where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_is_artificer_with_tools(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select A.Character, A.Class, B.Item from " \
            "(select Character, Class " \
            "from Link_Character_Class " \
            "where Character = '{}' and Class = 'Artificer' and Level > 2) A " \
            "left join  " \
            "(select character, Item " \
            "from Link_Character_Items " \
            "where Character = '{}' and Item = 'Tinker tools') B " \
            "on a.Character = B.Character".format(character_name, character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_item(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character = '{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_item_quantity(character_name: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character = '{}' AND Item = '{}' AND Quantity >= '{}'".format(character_name, item_name, quantity)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    return True


def character_has_crafted_this_week(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Crafting " \
            "where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Crafting_Value != 50:
        return False
    return True
