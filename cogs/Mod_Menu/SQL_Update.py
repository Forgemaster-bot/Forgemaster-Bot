from Mod_Menu import SQL_Lookup
import Connections
import Quick_Python


def character_sheet(character: list):
    cursor = Connections.sql_db_connection()

    # update Main_character Table
    discord_id = SQL_Lookup.player_id_by_name(character[0])
    character_name = character[2]
    race = character[2]
    background = character[3]
    xp = character[7]
    strength = character[10]
    dexterity = character[11]
    constitution = character[12]
    intelligence = character[13]
    wisdom = character[14]
    charisma = character[15]
    gold = character[16]
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


def character_stat_change(character_id: str, ability: str, value: int):
    cursor = Connections.sql_db_connection()

    current_stat = int(SQL_Lookup.character_ability_score(character_id, ability))
    new_value = current_stat + int(value)
    ability_name = Quick_Python.ability_name_convert(ability)
    query = "UPDATE Main_Characters " \
            "SET {} = '{}' " \
            "WHERE ID = '{}'".format(ability_name, new_value, character_id)
    cursor.execute(query)
    cursor.commit()
    return new_value


def character_item_quantity(character_id: str, item_name: str, quantity: int):
    # calculate new total
    new_amount = SQL_Lookup.character_item_quantity(character_id, item_name) + quantity
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Items set Quantity = '{}' " \
            "WHERE Character_ID = '{}' AND Item = '{}'".format(new_amount, character_id, item_name)
    cursor.execute(query)
    cursor.commit()


def character_wizard_spell(character_id: str, class_name: str):
    cursor = Connections.sql_db_connection()
    query = "UPDATE Link_Character_Class " \
            "SET Free_Wizard_Spells = 6 " \
            "WHERE ID = '{}' AND Class = '{}'".format(character_id, class_name)
    cursor.execute(query)
    cursor.commit()
