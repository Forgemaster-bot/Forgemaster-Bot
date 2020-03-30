import Connections


def move_to_graveyard(character_name: str, reason: str):
    cursor = Connections.sql_db_connection()
    death = "Insert into Main_Graveyard (Discord_ID,Character_Name,Race,Background,XP," \
            "Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,Gold,Reason) " \
            "SELECT Discord_ID,Character_Name,Race,Background,XP," \
            "Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma,Gold,'{}' " \
            "FROM Main_Characters " \
            "WHERE Character_Name = '{}'".format(reason, character_name)
    cursor.execute(death)
    cursor.commit()


def character_item(character_name: str, item_name: str, quantity: int):
    cursor = Connections.sql_db_connection()
    link_class_insert = "insert into Link_Character_Items (Character,Item,Quantity) " \
                        "values ('{}','{}','{}')".format(character_name, item_name, quantity)
    cursor.execute(link_class_insert)
    cursor.commit()
