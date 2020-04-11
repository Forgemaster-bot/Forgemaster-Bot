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


def character_can_subclass(character_name: str, class_slot: int):
    cursor = Connections.sql_db_connection()
    query = "select a.Class,a.Level,B.Sub_Class_Level,A.Sub_Class " \
            "from ( " \
            "select Class,level, Sub_Class " \
            "from Link_Character_Class  " \
            "where Character = '{}' and Number = '{}' " \
            ") a " \
            "left join ( " \
            "select Class, Sub_Class_Level from Info_Classes " \
            "where Class in (select Class from Link_Character_Class where Character = '{}' and Number = '{}') " \
            "group by Class, Sub_Class_Level) b " \
            "on a.Class = b.Class".format(character_name, class_slot, character_name, class_slot)
    cursor.execute(query)
    result = cursor.fetchone()
    if result.Sub_Class is None:
        if result.Level >= result.Sub_Class_Level:
            return True
    return False


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
