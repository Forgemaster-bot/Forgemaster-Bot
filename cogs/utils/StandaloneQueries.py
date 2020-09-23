import uuid
from typing import Optional

from Quick_Python import run_query
import Quick_Python
import Connections
from Character.Tables.InfoMaxSpellLevel import InfoMaxSpellLevel
from Character.Tables.InfoSpellsKnown import InfoSpellsKnown

def select_possible_subclasses(class_choice: str):
    query = "Select Sub_Class from Info_Subclass " \
            "Where Class = ? " \
            "ORDER BY Sub_Class "
    cursor = run_query(query, [class_choice])
    rows = cursor.fetchall()
    return [row.Sub_Class for row in rows]

def class_max_spell_level(character_class) -> int:
    data = InfoMaxSpellLevel.get_data()
    return data[character_class.name][character_class.level] if character_class.name in data else 0

def max_spells_known_per_level(character_class) -> int:
    data = InfoSpellsKnown.get_data()
    return data[character_class.name][character_class.level] if character_class.name in data else 0

def get_character_name(character_id: uuid.UUID) -> Optional[str]:
    with Connections.sql_db_connection() as cursor:
        query = "SELECT [Character_Name] FROM [Main_Characters] WHERE [ID] = ?"
        args = [character_id]
        Quick_Python.log_transaction(query, args)
        cursor.execute(query, args)
        return cursor.fetchval()

def crafting_limit(character_id, gold):
    with Connections.sql_db_connection() as cursor:
        query = "SELECT * FROM [Main_Crafting] WHERE Character_ID = ?"
        args = [character_id]
        Quick_Python.log_transaction(query, args)
        cursor.execute(query, args)
        crafting = cursor.fetchone()
        if crafting is None:
            query = "INSERT INTO [Main_Crafting] (Character_ID, Crafting_Value, Labour_Points) " \
                    "OUTPUT Inserted.* " \
                    "VALUES (?, '50', '0')"
            Quick_Python.log_transaction(query, args)
            cursor.execute(query, args)
            crafting = cursor.fetchone()
    if crafting.Labour_Points == 1:
        limit_list = [gold, 250]
    elif crafting.Labour_Points == 2:
        limit_list = [gold, 2500]
    elif crafting.Labour_Points > 2:
        limit_list = [gold, 25000]
    else:
        limit_list = [gold, crafting.Crafting_Value]
    return min(limit_list)

def update_crafting_value(character_id, new_total):
    with Connections.sql_db_connection() as cursor:
        query = "SELECT * FROM [Main_Crafting] WHERE Character_ID = ?"
        args = [character_id]
        Quick_Python.log_transaction(query, args)
        cursor.execute(query, args)
        crafting = cursor.fetchone()
        if crafting is None:
            query = "INSERT INTO [Main_Crafting] (Character_ID, Crafting_Value, Labour_Points) " \
                    "OUTPUT Inserted.* " \
                    "VALUES (?, '50', '0')"
            Quick_Python.log_transaction(query, args)
            cursor.execute(query, args)
            crafting = cursor.fetchone()
        query = "UPDATE [Main_Crafting] SET [Crafting_Value] = ? WHERE [Character_ID] = ?"
        args = [new_total, character_id]
        Quick_Python.log_transaction(query, args)
        cursor.execute(query, args)

def select_tool(profession) -> str:
    with Connections.sql_db_connection() as cursor:
        query = "SELECT [Tools] FROM Info_Skills WHERE [Name] = ?"
        args = [profession]
        Quick_Python.log_transaction(query, args)
        cursor.execute(query, args)
        return cursor.fetchval()

def get_items_by_profession_and_cost(profession: str, gold: float):
    with Connections.sql_db_connection() as cursor:
        query = "SELECT CAST([Type] AS TEXT) data, Value, Name FROM Info_Item " \
                    "WHERE [Crafting] = ? and [Value] <= ? " \
                    "ORDER BY [Type]"
        args = [profession, gold]
        Quick_Python.log_transaction(query, args)
        cursor.execute(query, args)
        return cursor.fetchall()
