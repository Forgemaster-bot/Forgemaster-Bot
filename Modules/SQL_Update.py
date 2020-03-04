import Quick_SQL
import SQL_Lookup
import Quick_Python


def character_xp(character_name: str, xp: int):
    cursor = Quick_SQL.db_connection()
    new_xp = SQL_Lookup.character_xp(character_name) + int(xp)

    query = "UPDATE Main_Characters " \
            "SET XP = {} " \
            "WHERE Character_Name = '{}'".format(new_xp, character_name)
    cursor.execute(query)
    cursor.commit()
    return new_xp


def character_gold(character_name: str, gold: float):
    cursor = Quick_SQL.db_connection()
    new_gold = SQL_Lookup.character_gold(character_name) + int(gold)

    query = "UPDATE Main_Characters " \
            "SET Gold = '{}' " \
            "WHERE Character_Name = '{}'".format(new_gold, character_name)
    cursor.execute(query)
    cursor.commit()
    return new_gold


def character_item_quantity(character_name: str, item_name: str, quantity: int):
    # calculate new total
    new_amount = SQL_Lookup.character_item_quantity(character_name, item_name) + quantity
    cursor = Quick_SQL.db_connection()
    query = "UPDATE Link_Character_Items set Quantity = '{}' " \
            "WHERE Character = '{}' AND Item = '{}'".format(new_amount, character_name, item_name)
    cursor.execute(query)
    cursor.commit()


def character_class_level(character_name: str, character_class: str):
    cursor = Quick_SQL.db_connection()
    current_level = int(SQL_Lookup.character_class_level_by_class(character_name, character_class))
    new_level = current_level + 1
    query = "UPDATE Link_Character_Class " \
            "SET Level = '{}' " \
            "WHERE Character = '{}' AND Class = '{}'".format(new_level, character_name, character_class)
    cursor.execute(query)
    cursor.commit()


def character_stat_change(character_name: str, ability: str, value: int):
    cursor = Quick_SQL.db_connection()

    current_stat = int(SQL_Lookup.character_ability_score(character_name, ability))
    new_value = current_stat + int(value)
    ability_name = Quick_Python.ability_name_convert(ability)
    query = "UPDATE Main_Characters " \
            "SET {} = '{}' " \
            "WHERE Character_Name = '{}'".format(ability_name, new_value, character_name)
    cursor.execute(query)
    cursor.commit()
    return new_value


def character_sheet(character_sheet: list):
    cursor = Quick_SQL.db_connection()

    # update Main_character Table
    discord_id = SQL_Lookup.player_id_by_name(character_sheet[0])
    character_name = character_sheet[2]
    race = character_sheet[2]
    background = character_sheet[3]
    xp = character_sheet[7]
    strength = character_sheet[10]
    dexterity = character_sheet[11]
    constitution = character_sheet[12]
    intelligence = character_sheet[13]
    wisdom = character_sheet[14]
    charisma = character_sheet[15]
    gold = character_sheet[16]
    main_update = "UPDATE Main_Characters " \
                  "SET " \
                  "Discord_ID = '{}',Race = '{}',Background = '{}'," \
                  "XP = '{}', Strength = '{}', Dexterity = '{}', Constitution = '{}', " \
                  "Intelligence = '{}', Wisdom = '{}', Charisma = '{}', Gold = '{}' " \
                  "WHERE Character_Name = '{}'" \
        .format(discord_id, race, background,
                xp, strength, dexterity, constitution,
                intelligence, wisdom, charisma, gold,
                character_name)

    cursor.execute(main_update)
    cursor.commit()


def character_owner(character_name: str, discord_id:str):
    cursor = Quick_SQL.db_connection()
    query = "UPDATE Main_Characters " \
            "SET Discord_ID = '{}'" \
            "WHERE Character_Name = '{}'".format(discord_id, character_name)
    cursor.execute(query)
    cursor.commit()


def player_name(discord_name: str, discord_id: str):
    cursor = Quick_SQL.db_connection()
    query = "UPDATE Info_Discord " \
            "SET Name = '{}' " \
            "WHERE ID = '{}'".format(discord_name, discord_id)
    cursor.execute(query)
    cursor.commit()


def trade_quantity(character_name: str, item_name: str, quantity: int):
    # calculate new total
    new_amount = SQL_Lookup.trade_item_quantity(character_name, item_name) + quantity
    cursor = Quick_SQL.db_connection()
    query = "UPDATE Main_Trade set Quantity = '{}' " \
            "WHERE Character = '{}' AND Item = '{}'".format(new_amount, character_name, item_name)
    cursor.execute(query)
    cursor.commit()
