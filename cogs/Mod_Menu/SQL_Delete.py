import Connections


def character_feat(character_id: str, feat: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM " \
            "Link_Character_Feats " \
            "WHERE Character_ID ='{}' AND Feat = '{}'".format(character_id, feat)
    cursor.execute(query)
    cursor.commit()


def character_skill(character_id: str, skill: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Link_Character_Skills " \
            "WHERE Character_ID ='{}' AND Skill = '{}'".format(character_id, skill)
    cursor.execute(query)
    cursor.commit()


def character_item(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "DELETE FROM Link_Character_Items " \
            "WHERE Character_ID = '{}' AND Item = '{}'".format(character_id, item_name)
    cursor.execute(query)
    cursor.commit()
