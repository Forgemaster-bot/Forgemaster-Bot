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

    character_insert = "insert into Main_Characters (Discord_ID,Character_Name,Race,Background,XP," \
                       "Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,Gold) " \
                       "values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"\
                       .format(discord_id, character_name, race, background, xp,
                               strength, dexterity, constitution, intelligence, wisdom, charisma, gold)

    cursor.execute(character_insert)
    cursor.commit()


def character_class(character_name: str, class_name: str, level: int, number: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Class (Character,Class,Level,Number) " \
                        "values ('{}','{}','{}','{}')".format(character_name, class_name, level, number)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_item(character_name: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Items (Character,Item,Quantity) " \
                        "values ('{}','{}','{}')".format(character_name, item_name, quantity)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_feat(character_name: str, feat_name: str):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Feats (Character,Feat) " \
                        "values ('{}','{}')".format(character_name, feat_name)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_skill(character_name: str, skill_name: str, proficiency: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Skills (Character,Skill,Proficiency) " \
                        "values ('{}','{}','{}')".format(character_name, skill_name, proficiency)
    cursor.execute(link_class_insert)
    cursor.commit()
