import Connections


def move_to_graveyard(character_id: str, reason: str):
    cursor = Connections.sql_db_connection()
    death = "Insert into Main_Graveyard (ID, Discord_ID,Character_Name,Race,Background,XP," \
            "Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,Gold,Reason) " \
            "SELECT ID, Discord_ID,Character_Name,Race,Background,XP," \
            "Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,Gold,'{}' " \
            "FROM Main_Characters " \
            "WHERE ID = '{}'".format(reason, character_id)
    cursor.execute(death)
    cursor.commit()


def character_item(character_id: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Items (Character_ID,Item,Quantity) " \
                        "values ('{}','{}','{}')".format(character_id, item_name, quantity)
    cursor.execute(link_class_insert)
    cursor.commit()
