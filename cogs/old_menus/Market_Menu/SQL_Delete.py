import Connections
from Quick_Python import run_query


def character_item(character_id: str, item_name: str):
    query = "DELETE FROM Link_Character_Items WHERE Character_ID = ? AND Item = ?"
    cursor = run_query(query, [character_id, item_name])
    cursor.commit()


def trade_sale(character_id: str, item_name: str):
    query = "DELETE FROM Main_Trade WHERE Character_ID =? AND Item = ?"
    cursor = run_query(query, [character_id, item_name])
    cursor.commit()
