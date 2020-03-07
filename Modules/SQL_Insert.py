import Quick_SQL


def character_create(character_sheet: list):
    cursor = Quick_SQL.db_connection()
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
    cursor = Quick_SQL.db_connection()
    link_class_insert = "insert into Link_Character_Class (Character,Class,Level,Number) " \
                        "values ('{}','{}','{}','{}')".format(character_name, class_name, level, number)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_item(character_name: str, item_name: str, quantity: int):
    cursor = Quick_SQL.db_connection()
    link_class_insert = "insert into Link_Character_Items (Character,Item,Quantity) " \
                        "values ('{}','{}','{}')".format(character_name, item_name, quantity)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_feat(character_name: str, feat_name: str):
    cursor = Quick_SQL.db_connection()
    link_class_insert = "insert into Link_Character_Feats (Character,Feat) " \
                        "values ('{}','{}')".format(character_name, feat_name)
    cursor.execute(link_class_insert)
    cursor.commit()


def character_skill(character_name: str, skill_name: str, proficiency: int):
    cursor = Quick_SQL.db_connection()
    link_class_insert = "insert into Link_Character_Skills (Character,Skill,Proficiency) " \
                        "values ('{}','{}','{}')".format(character_name, skill_name, proficiency)
    cursor.execute(link_class_insert)
    cursor.commit()


def move_to_graveyard(character_name: str, reason: str):
    cursor = Quick_SQL.db_connection()
    death = "Insert into Main_Graveyard (Discord_ID,Character_Name,Race,Background,XP," \
            "Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,Gold,Reason) " \
            "SELECT Discord_ID,Character_Name,Race,Background,XP," \
            "Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,Gold,'{}' " \
            "FROM Main_Characters " \
            "WHERE Character_Name = '{}'".format(reason, character_name)
    cursor.execute(death)
    cursor.commit()


def new_item(name: str, description: str, weight: float):
    cursor = Quick_SQL.db_connection()
    link_class_insert = "insert into Info_Item (Name,Description,Weight) " \
                        "values ('{}','{}','{}')".format(name, description, weight)
    cursor.execute(link_class_insert)
    cursor.commit()


def sync_players(user_id: str, name: str):
    cursor = Quick_SQL.db_connection()
    query = "insert into Info_Discord (ID,Name) values ('{}','{}')".format(user_id, name)
    cursor.execute(query)
    cursor.commit()


def trade_sell(character_name: str, item_name: str, quantity: int, price: int):
    cursor = Quick_SQL.db_connection()
    query = "insert into Main_Trade (Character,item,Quantity,Price) " \
            "values ('{}','{}','{}','{}')".format(character_name, item_name, quantity, price)
    cursor.execute(query)
    cursor.commit()


def discord_roll(discord_id: str, stat_array: list):
    cursor = Quick_SQL.db_connection()
    link_class_insert = "insert into Discord_Roll (Discord_ID,Roll_1,Roll_2,Roll_3,Roll_4,Roll_5,Roll_6) " \
                        "values ('{}','{}','{}','{}','{}','{}','{}')".format(discord_id,
                                                                             stat_array[0], stat_array[1],
                                                                             stat_array[2], stat_array[3],
                                                                             stat_array[4], stat_array[5])
    cursor.execute(link_class_insert)
    cursor.commit()


'''''''''''''''''''''''''''''''''''''''''
################Crafting#################
'''''''''''''''''''''''''''''''''''''''''


def crafting_point(character_name: str):
    cursor = Quick_SQL.db_connection()
    insert = "insert into Main_crafting (character_Name,Crafting_Point,Crafting_Value,Labour_Points) " \
             "values ('{}','1','100','0')".format(character_name)
    cursor.execute(insert)
    cursor.commit()
