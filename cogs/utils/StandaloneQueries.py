from Quick_Python import run_query
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
