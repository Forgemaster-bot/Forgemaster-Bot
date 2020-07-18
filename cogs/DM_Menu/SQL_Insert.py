import Connections
from Quick_Python import run_query


def move_to_graveyard(character_id: str, reason: str):
    query = "Insert into Main_Graveyard (ID, Discord_ID,Character_Name,Race,Background,XP," \
            "Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,Gold,Reason) " \
            "SELECT ID, Discord_ID,Character_Name,Race,Background,XP," \
            "Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,Gold,? " \
            "FROM Main_Characters " \
            "WHERE ID = ?"
    cursor = run_query(query, [reason, character_id])
    cursor.commit()


def character_item(character_id: str, item_name: str, quantity: int):
    query = "insert into Link_Character_Items (Character_ID,Item,Quantity) values (?,?,?)"
    cursor = run_query(query, [character_id, item_name, quantity])
    cursor.commit()
