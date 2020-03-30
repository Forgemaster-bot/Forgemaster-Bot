from Mod_Menu import SQL_Lookup
import Quick_SQL
import Quick_Python


def character_sheet(character: list):
    cursor = Quick_SQL.db_connection()

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
