import Connections
from Quick_Python import run_query


def character_item(character_id: str, item_name: str, quantity: int):
    query = "insert into Link_Character_Items (Character_ID ,Item,Quantity) " \
                        "values (?,?,?)"
    cursor = run_query(query, [character_id, item_name, quantity])
    cursor.commit()


def trade_sell(character_id: str, item_name: str, quantity: int, price: float, item_type: str):
    query = "insert into Main_Trade (Character_ID,item,Quantity,Price, Type) " \
            "values (?,?,?,?,?)"
    cursor = run_query(query, [character_id, item_name, quantity, price, item_type])
    cursor.commit()


def share_spell(target_id: str, spell_name: str, owner_name: str):
    query = "insert into Main_Wizard_Spell_Share (Target_ID,Spell,Owner) " \
            "values (?,?,?)"
    cursor = run_query(query, [target_id, spell_name, owner_name])
    cursor.commit()
