import Connections


def clear_character_links(character_name: str):
    cursor = Connections.sql_db_connection()
    clear_class = "DELETE FROM Link_Character_Class WHERE Character ='{}'".format(character_name)
    clear_inventory = "DELETE FROM Link_Character_Items WHERE Character ='{}'".format(character_name)
    clear_feats = "DELETE FROM Link_Character_Feats WHERE Character ='{}'".format(character_name)
    cursor.execute(clear_class)
    cursor.execute(clear_feats)
    cursor.execute(clear_inventory)
    cursor.commit()


def character_feat(character_name: str, feat: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Link_Character_Feats WHERE Character ='{}' AND Feat = '{}'".format(character_name, feat)
    cursor.execute(query)
    cursor.commit()


def character_skill(character_name: str, skill: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Link_Character_Skills " \
            "WHERE Character ='{}' AND Skill = '{}'".format(character_name, skill)
    cursor.execute(query)
    cursor.commit()


def character_item(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Link_Character_Items WHERE Character ='{}' AND Item = '{}'".format(character_name, item_name)
    cursor.execute(query)
    cursor.commit()
