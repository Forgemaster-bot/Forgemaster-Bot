import SQL_Lookup
import Quick_Google
import Quick_Python


def trade_create(character_name: str, item_name: str):  # [Character], [Item]
    trade_sheet = Quick_Google.sheet("Player Trade")
    print_row = len(trade_sheet.col_values(1)) + 1

    trade_item = SQL_Lookup.trade_item(character_name, item_name)
    trade_item_list = [trade_item.Character, trade_item.Item,
                       trade_item.Price, trade_item.Quantity]
    trade_sheet.insert_row(trade_item_list, print_row)


def trade_update(character_name: str, item_name):  # [Character],[Item]
    trade_sheet = Quick_Google.sheet("Player Trade")
    trade_row = Quick_Python.find_trade(trade_sheet.col_values(1), character_name,
                                        trade_sheet.col_values(2), item_name)

    trade_item = SQL_Lookup.trade_item(character_name, item_name)
    trade_item_quantity = trade_item.Quantity
    trade_sheet.update_cell(trade_row, 3, trade_item_quantity)


def trade_delete(character_name: str, item_name):  # [Character],[Item]
    trade_sheet = Quick_Google.sheet("Player Trade")
    seller_list = trade_sheet.col_values(1)
    item_list = trade_sheet.col_values(2)
    trade_row = 0
    for row in range(len(seller_list)):
        if seller_list[row] == character_name:
            character_index = row
            list_item_name = item_list[character_index]
            if list_item_name == item_name:
                trade_row = character_index + 1
                break
    trade_sheet.delete_row(trade_row)
