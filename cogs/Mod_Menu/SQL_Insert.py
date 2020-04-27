import Connections


def character_create(character_sheet: list):
    cursor = Connections.sql_db_connection()
    discord_id = character_sheet[0].lstrip()
    character_name = character_sheet[1].lstrip()
    race = character_sheet[2].lstrip()
    background = character_sheet[3].lstrip()
    xp = 0
    strength = character_sheet[5].lstrip()
    dexterity = character_sheet[6].lstrip()
    constitution = character_sheet[7].lstrip()
    intelligence = character_sheet[8].lstrip()
    wisdom = character_sheet[9].lstrip()
    charisma = character_sheet[10].lstrip()
    gold = character_sheet[11].lstrip()

    character_insert = "insert into Main_Characters (ID, Discord_ID,Character_Name,Race,Background,XP," \
                       "Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,Gold) " \
                       "values (NEWID(),'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"\
                       .format(discord_id, character_name, race, background, xp,
                               strength, dexterity, constitution, intelligence, wisdom, charisma, gold)

    cursor.execute(character_insert)
    cursor.commit()


def character_class(character_id: str, class_name: str, level: int, number: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Class (Character_ID,Class,Level,Number) " \
                        "values ('{}','{}','{}','{}')".format(character_id, class_name, level, number)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_item(character_id: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Items (Character_ID, Item,Quantity) " \
                        "values ('{}','{}','{}')".format(character_id, item_name, quantity)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_feat(character_id: str,  feat_name: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Feats (Character_ID, Character,Feat) " \
                        "values ('{}','{}')".format(character_id, feat_name)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_skill(character_id: str, skill_name: str, proficiency: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Skills (Character_ID,Skill,Proficiency) " \
                        "values ('{}','{}','{}')".format(character_id, skill_name, proficiency)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_spell_book(character_id: str, character_name: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Main_Spell_Book (ID, Owner_ID, Name,Type) " \
                        "values (NEWID(),'{}','{} Spell book','Core')".format(character_id, character_name)
    cursor.execute(link_class_insert)
    cursor.commit()
