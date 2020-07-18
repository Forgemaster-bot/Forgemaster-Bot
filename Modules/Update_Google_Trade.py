import Quick_Python
import Connections
from Quick_Python import run_query


def trade_create(character_id: str, item_name: str):  # [Character], [Item]
    trade_sheet = Connections.google_sheet("Player Trade")
    print_row = len(trade_sheet.col_values(1)) + 1

    trade_item = lookup_trade_item(character_id, item_name)
    character_name = character_name_by_character_id(trade_item.Character_ID)
    trade_item_list = [character_name, trade_item.Item,
                       trade_item.Price, trade_item.Quantity]
    trade_sheet.insert_row(trade_item_list, print_row)


def trade_update(character_id: str, item_name):  # [Character],[Item]
    trade_sheet = Connections.google_sheet("Player Trade")
    seller_list = trade_sheet.col_values(1)
    item_list = trade_sheet.col_values(2)
    character_name = character_name_by_character_id(character_id)
    trade_row = Quick_Python.find_trade_row(character_name, seller_list, item_name, item_list)
    trade_item = lookup_trade_item(character_id, item_name)
    trade_item_quantity = trade_item.Quantity
    trade_sheet.update_cell(trade_row, 4, trade_item_quantity)


def trade_delete(character_id: str, item_name):  # [Character],[Item]
    trade_sheet = Connections.google_sheet("Player Trade")
    seller_list = trade_sheet.col_values(1)
    item_list = trade_sheet.col_values(2)
    character_name = character_name_by_character_id(character_id)
    trade_row = Quick_Python.find_trade_row(character_name, seller_list, item_name, item_list)
    trade_sheet.delete_row(trade_row)


def lookup_trade_item(character_id: str, item_name: str):
    query = "select * from Main_Trade where Character_ID = ? AND Item = ?"
    cursor = run_query(query, [character_id, item_name])
    item = cursor.fetchone()
    return item


def character_name_by_character_id(character_id: str):
    query = "select * from Main_Characters where ID = ?"
    cursor = run_query(query, [character_id])
    result = cursor.fetchone()
    return result.Character_Name
