import Connections
from Quick_Python import run_query


def character_feat(character_id: str, feat: str):
    query = "DELETE FROM " \
            "Link_Character_Feats " \
            "WHERE Character_ID =? AND Feat = ?"
    cursor = run_query(query, [character_id, feat])
    cursor.commit()


def character_skill(character_id: str, skill: str):
    query = "DELETE FROM Link_Character_Skills " \
            "WHERE Character_ID =? AND Skill = ?"
    cursor = run_query(query, [character_id, skill])
    cursor.commit()


def character_item(character_id: str, item_name: str):
    query = "DELETE FROM Link_Character_Items " \
            "WHERE Character_ID = ? AND Item = ?"
    cursor = run_query(query, [character_id, item_name])
    cursor.commit()
