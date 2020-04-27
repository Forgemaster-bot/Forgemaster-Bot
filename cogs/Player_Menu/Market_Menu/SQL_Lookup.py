import Connections


def character_gold(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Main_Characters where ID = '{}'".format(character_id)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.Gold


def character_inventory(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Link_Character_Items " \
            "Where Character_ID = '{}' and Item not in (select Item from Main_Trade where Character_ID = '{}') " \
            "Order by Item".format(character_id, character_id)
    cursor.execute(query)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


def character_owner(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return int(result.Discord_ID)


def character_recycle_inventory_list(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character_ID = '{}' and Item in (select Name from Info_Item) " \
            "order by Item".format(character_id)
    cursor.execute(query)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


def character_item(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character_ID = '{}' AND Item = '{}'".format(character_id, item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def item_detail(item_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Info_Item " \
            "Where Name = '{}' ".format(item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def trade_goods_types(character_id: str, gold_limit: float):
    cursor = Connections.sql_db_connection()
    query = "Select distinct Type " \
            "From Main_Trade " \
            "Where Price <= '{}' and Character_ID != '{}' " \
            "Order by Type".format(gold_limit, character_id)
    cursor.execute(query)
    rows = cursor.fetchall()
    response = []
    for row in rows:
        response.append(row.Type)
    response.sort()
    return response


def trade_goods_items_by_type(character_id: str, gold_limit: float, item_type: str):
    cursor = Connections.sql_db_connection()
    query = "select Item " \
            "from Main_Trade " \
            "where Type = '{}' and price <= '{}' and Character_ID != '{}' " \
            "group by Item " \
            "order by Item".format(item_type, gold_limit, character_id)
    cursor.execute(query)
    item_name_list = cursor.fetchall()
    response = []
    for items in item_name_list:
        item_details = trade_item_not_sold_by_character(character_id, items.Item)
        if item_details is not None:
            response.append("{}: {}g each with {} for sale".format(item_details.Item, item_details.Price,
                                                                   item_details.Quantity))
    return response


def trade_item_not_sold_by_character(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Main_Trade " \
            "Where Item = '{}' and Character_ID != '{}' " \
            "order by Price, Quantity desc".format(item_name, character_id)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def trade_item_cheapest_on_sale(item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Main_Trade " \
            "Where Item = '{}' " \
            "order by Price, Quantity desc".format(item_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def character_items_for_sale(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select Item, Price " \
            "from Main_Trade " \
            "where Character_ID = '{}' " \
            "order by Item".format(character_id)
    cursor.execute(query)
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append("{} - {}g".format(row.Item, row.Price))
    return result


def trade_item_character(character_id: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Main_Trade " \
            "Where Item = '{}' and Character_ID = '{}' " \
            "order by Price, Quantity desc".format(item_name, character_id)
    cursor.execute(query)
    item = cursor.fetchone()
    return item


def character_spell_level_list_spell_book(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select Level " \
            "from Link_Spell_Book_Spells A " \
            "left join Main_Spell_Book B " \
            "on A.Spell_Book_ID = B.ID " \
            "left join Info_Spells C " \
            "on A.Spell = C.Name " \
            "Where Owner_ID = '{}' " \
            "Group By Level " \
            "Order By Level".format(character_id)
    cursor.execute(query)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append("Level {} spell".format(row.Level))
    return result


def character_known_wizard_spells_by_level(character_id: str, spell_level: int):
    cursor = Connections.sql_db_connection()
    query = "Select DISTINCT Spell " \
            "From Main_Spell_Book A " \
            "Left join Link_Spell_book_Spells B " \
            "on A.ID = B.Spell_Book_ID " \
            "left join Info_Spells C " \
            "on B.Spell = C.Name " \
            "Where A.Owner_ID = '{}' " \
            "and C.Level = '{}' " \
            "and Spell in (select Spell from Link_Class_Spells where Class = 'Wizard')".format(character_id,
                                                                                               spell_level)
    cursor.execute(query)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row.Spell)
    return result


def character_name_by_character_id(character_id: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where ID = '{}'".format(character_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.Character_Name


def character_id_by_character_name(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name = '{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result.ID
