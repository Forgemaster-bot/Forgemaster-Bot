import Connections
from Quick_Python import run_query


def character_skills(character_id: str):
    query = "select * from Link_Character_Skills where Character_ID = ?"
    cursor = run_query(query, [character_id])
    rows = cursor.fetchall()
    skills = []
    for row in rows:
        if row.Proficiency == 1:
            skills.append(row.Skill)
        else:
            skills.append(row.Skill + " (D)")
    return skills


def character_essences(character_id: str):
    query = "select * " \
            "from Link_Character_Items " \
            "where Character_ID = ? " \
            "and item in ( select Name from Info_Item where Type = 'Essence') " \
            "order by Item"
    cursor = run_query(query, [character_id])
    rows = cursor.fetchall()
    essences = []
    for row in rows:
        if row.Quantity == 1:
            essences.append(row.Item)
        else:
            essences.append(row.Item + " ({})".format(row.Quantity))
    return essences


def character_gold(character_id: str):
    query = "select * from Main_Characters where ID = ?"
    cursor = run_query(query, [character_id])
    character = cursor.fetchone()
    return character.Gold


def character_crafting(character_id: str):
    query = "Select * " \
            "From Main_Crafting " \
            "Where Character_ID = ?"
    cursor = run_query(query, [character_id])
    response = cursor.fetchone()
    return response


def character_profession_list(character_id: str):
    query = "Select Skill " \
            "From Link_Character_Skills " \
            "Where Character_ID = ?" \
            "Order by Skill"
    cursor = run_query(query, [character_id])
    rows = cursor.fetchall()
    profession_list = []
    for row in rows:
        profession_list.append(row.Skill)
    return profession_list


def profession_tool(profession: str):
    query = "select Tools " \
            "from Info_Skills " \
            "Where Name = ?"
    cursor = run_query(query, [profession])
    result = cursor.fetchone()
    return result.Tools


def profession_item_type_list(profession: str, gold_limit: float):
    gold_value = gold_limit * 2
    query = "Select Type from Info_Item " \
            "Where Crafting = ? and Value <= ? " \
            "group by Type order by Type"
    cursor = run_query(query, [profession, gold_value])
    rows = cursor.fetchall()
    item_types = []
    for row in rows:
        item_types.append(row.Type)
    return item_types


def profession_item_list(profession: str, item_type: str, gold: float):
    query = "select * " \
            "from Info_Item " \
            "Where Crafting = ? and Type = ? and Value <= ? " \
            "order by Name"
    cursor = run_query(query, [profession, item_type, gold*2])
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append(row.Name)
    return results


def item_value(item_name: str):
    query = "Select * " \
            "From Info_Item " \
            "Where Name = ? "
    cursor = run_query(query, [item_name])
    item = cursor.fetchone()
    return item.Value


def character_item_quantity(character_id: str, item_name: str):
    query = "Select * " \
            "From Link_Character_Items " \
            "Where Character_ID = ? AND Item = ?"
    cursor = run_query(query, [character_id, item_name])
    item = cursor.fetchone()
    return item.Quantity


def profession_consumable_name(profession: str):
    query = "Select * " \
            "From Info_Skills " \
            "Where Name = ?"
    cursor = run_query(query, [profession])
    result = cursor.fetchone()
    return result.Consumable_Name


def recipe_essence_list(profession: str, name: str):
    query = "Select * " \
            "From Info_Crafting_Recipes " \
            "Where Skill = ? and Name = ? "
    cursor = run_query(query, [profession, name])
    result = cursor.fetchone()
    return result


def character_known_recipe(character_id: str, profession: str):
    query = "Select * " \
            "From Link_Character_Recipe " \
            "Where Character_ID = ? and Skill = ?"
    cursor = run_query(query, [character_id, profession])
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append(row.Recipe)
    return result


def recipe(profession: str, name: str):
    query = "Select * " \
            "From Info_Crafting_Recipes " \
            "Where Skill = ? and Name = ? "
    cursor = run_query(query, [profession, name])
    result = cursor.fetchone()
    return result


def character_inventory_essence_count(character_id: str):
    query = "select * " \
            "from Link_Character_Items " \
            "where Character_ID = ? and Item in (select Name from Info_Item where Type = 'Essence') " \
            "order by Item"
    cursor = run_query(query, [character_id])
    rows = cursor.fetchall()
    essence = 0
    for row in rows:
        essence = essence + row.Quantity
    return essence


def profession_recipes(profession: str):
    query = "Select * " \
            "From Info_Crafting_Recipes " \
            "Where Skill = ?"
    cursor = run_query(query, [profession])
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append(row.Name)
    return result


def recipe_by_essence(profession: str, essence_1: str, essence_2):
    query = "Select * " \
            "From Info_Crafting_Recipes " \
            "Where Skill = ? and Essence_1 = ? and Essence_2 = ?"
    cursor = run_query(query, [profession, essence_1, essence_2])
    result = cursor.fetchone()
    if result is None:
        return ""
    return result.Name


def character_known_recipe_details(character_id: str, profession: str):
    query = "Select CAST(b.Name AS TEXT)," \
                    "CAST(b.Description AS TEXT)," \
                    "CAST(b.Essence_1 AS TEXT)," \
                    "CAST(b.Essence_2 AS TEXT) " \
            "From Link_Character_Recipe a " \
            "left join Info_Crafting_Recipes b " \
            "on a.Recipe = b.Name and a.Skill = b.Skill " \
            "Where a.Character_ID = ? and a.Skill = ?"
    cursor = run_query(query, [character_id, profession])
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append("{} : {} : **{}** : **{}** ".format(row.Name, row.Description, row.Essence_1, row.Essence_2))
    return result


def character_owner(character_id: str):
    query = "select * from Main_Characters where ID =?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return int(result.Discord_ID)


def character_count_classes(character_id: str):
    query = "Select Count(*) Total " \
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


def character_class_level_by_class(character_id: str, character_class: str):
    query = "select * " \
            "from Link_Character_Class " \
            "where Character_ID = ? and Class = ?"
    cursor = run_query(query, [character_id, character_class])
    class_lookup = cursor.fetchone()
    return class_lookup.Level


def class_max_spell_by_level(class_name: str, class_level):
    query = "select * " \
            "from Info_Max_Spell_Level " \
            "where Class = ?"
    cursor = run_query(query, [class_name])
    result = cursor.fetchone()
    return result[class_level]


def character_spell_level_list_by_class(character_id: str, class_name: str):
    sub_class = character_class_subclass(character_id, class_name)
    query = "select Level " \
            "from Link_Character_Spells A " \
            "left Join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where Character_ID = ? and (Origin = ? or Origin = ?) " \
            "Group By Level " \
            "Order by Level"
    cursor = run_query(query, [character_id, class_name, sub_class])
    result = cursor.fetchall()
    return result


def character_spell_level_list_spell_book(character_id: str):
    query = "select Level " \
            "from Link_Spell_Book_Spells A " \
            "left join Main_Spell_Book B " \
            "on A.Spell_Book_ID = B.ID " \
            "left join Info_Spells C " \
            "on A.Spell = C.Name " \
            "Where Owner_ID = ? " \
            "Group By Level " \
            "Order By Level"
    cursor = run_query(query, [character_id])
    result = cursor.fetchall()
    return result


def character_known_spells_by_class_and_level(character_id: str, class_name: str, spell_level: int):
    sub_class = character_class_subclass(character_id, class_name)
    sub_class = str(sub_class) + "%"
    query = "select Spell " \
            "from Link_Character_Spells A " \
            "left Join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where Character_ID = ? " \
            "and B.Level = ? " \
            "and (Origin = ? or Origin like ?) "
        
    cursor = run_query(query, [character_id, spell_level, class_name, sub_class])
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row.Spell)
    return result


def character_known_wizard_spells_by_level(character_id: str, spell_level: int):
    query = "Select Spell " \
            "From Main_Spell_Book A " \
            "Left join Link_Spell_book_Spells B " \
            "on A.ID = B.Spell_Book_ID " \
            "left join Info_Spells C " \
            "on B.Spell = C.Name " \
            "Where A.Owner_ID = ? and C.Level = ?"
    cursor = run_query(query, [character_id, spell_level])
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row.Spell)
    return result


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


def character_class_subclass(character_id: str, subclass: str):
    query = "Select * " \
            "from Link_character_Class " \
            "where Character_ID = ? and Class = ? "
    cursor = run_query(query, [character_id, subclass])
    result = cursor.fetchone()
    if result.Sub_Class is None:
        return None
    return result.Sub_Class


def spell_consumable_cost(spell_name: str):
    query = "Select * " \
            "From Info_Spells " \
            "Where Name = ?"
    cursor = run_query(query, [spell_name])
    result = cursor.fetchone()
    return result.Consumable_Cost


def character_total_level(character_id: str):
    query = "select SUM(Level) Total from Link_Character_Class where Character_ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return result.Total


def proficiency_bonus(level: int):
    query = "select *" \
            "From Info_XP " \
            "Where Level = ?"
    cursor = run_query(query, [level])
    result = cursor.fetchone()
    return result.Proficiency_Bonus


def character_intelligence(character_id: str):
    query = "select * from Main_Characters where ID = ?"
    cursor = run_query(query, [character_id])
    character = cursor.fetchone()
    return character.Intelligence


def character_has_arcane_proficiency(character_id: str):
    query = "select * " \
            "from Link_Character_Skills " \
            "Where Character_ID = ? and Skill = 'Arcana'"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    if result is None:
        return 0
    return result.Proficiency


def character_wizard_spells_known(character_id: str):
    query = "Select Spell " \
            "From Main_Spell_Book A " \
            "Left join Link_Spell_book_Spells B " \
            "on A.ID = B.Spell_Book_ID " \
            "left join Info_Spells C " \
            "on B.Spell = C.Name " \
            "Where A.Owner_ID = ? and A.Type = 'Core' "
    cursor = run_query(query, [character_id])
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row.Spell)
    return result


def character_scribe_spell_options(character_id: str, spell_limit: int):
    query = "select * " \
            "from ( " \
            "select B.Name,B.Level,A.Origin " \
            "from ( " \
            "select replace(item,'Scroll of ','') as Spell, 'a scroll' as Origin " \
            "from Link_Character_Items " \
            "where Character_ID = ? and item like 'Scroll of %' ) A " \
            "left join Info_Spells B " \
            "on A.Spell = B.Name " \
            "union all " \
            "select c.Name, C.Level, A.Name " \
            "from Main_Spell_book A " \
            "left join Link_Spell_book_Spells B " \
            "on A.ID = B.Spell_Book_ID " \
            "left join Info_Spells C " \
            "on B.Spell = C.Name " \
            "where A.Owner_ID = ? and B.Known = 0 " \
            "union all " \
            "select B.Name,B.Level, A.Owner + ' Spell Book' as Owner " \
            "from Main_Wizard_Spell_Share A " \
            "left join Info_Spells B " \
            "on A.Spell = B.Name " \
            "where A.Target_ID = ?) A " \
            "where A.Name not in (Select Spell " \
            "from Link_Spell_book_Spells A " \
            "left join Main_Spell_book B " \
            "on A.Spell_Book_ID = B.ID " \
            "where B.Owner_ID = ?) " \
            "and Level <= ? " \
            "Order by Level,Name"
    cursor = run_query(query, [character_id, character_id, character_id, character_id, spell_limit])
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append("Level {} Spell: {} From: {}".format(row.Level, row.Name, row.Origin))
    return result


def spell_book(character_id: str):
    query = "select * " \
            "from Main_Spell_book " \
            "Where Owner_ID = ? and Type = 'Core'"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return result.ID


def character_name_by_character_id(character_id: str):
    query = "select * from Main_Characters where ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return result.Character_Name


def character_id_by_character_name(character_name: str):
    query = "select * from Main_Characters where Character_Name = ?"
    cursor = run_query(query, [character_name])
    result = cursor.fetchone()
    return result.ID
