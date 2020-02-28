import Quick_SQL


def character_classes(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Link_Character_Class WHERE Character ='{}'".format(character_name)
    cursor.execute(query)
    cursor.commit()


def character_feat(character_name: str, feat: str):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Link_Character_Feats WHERE Character ='{}' AND Feat = '{}'".format(character_name, feat)
    cursor.execute(query)
    cursor.commit()


def character_item(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Link_Character_Items WHERE Character ='{}' AND Item = '{}'".format(character_name,item_name)
    cursor.execute(query)
    cursor.commit()


def character(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Main_Characters WHERE Character_Name ='{}'".format(character_name)
    cursor.execute(query)
    cursor.commit()


def clear_character_links(character_name: str):
    cursor = Quick_SQL.db_connection()
    clear_class = "DELETE FROM Link_Character_Class WHERE Character ='{}'".format(character_name)
    clear_inventory = "DELETE FROM Link_Character_Items WHERE Character ='{}'".format(character_name)
    clear_feats = "DELETE FROM Link_Character_Feats WHERE Character ='{}'".format(character_name)
    cursor.execute(clear_class)
    cursor.execute(clear_feats)
    cursor.execute(clear_inventory)
    cursor.commit()


def character_skill(character_name: str, skill: str):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Link_Character_Skills " \
            "WHERE Character ='{}' AND Skill = '{}'".format(character_name, skill)
    cursor.execute(query)
    cursor.commit()


def discord_roll(discord_id):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Discord_Roll " \
            "WHERE Discord_ID ='{}'".format(discord_id)
    cursor.execute(query)
    cursor.commit()


def trade_sale(character_name: str, item_name: str):
    cursor = Quick_SQL.db_connection()
    query = "DELETE FROM Main_Trade WHERE Character ='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    cursor.commit()
