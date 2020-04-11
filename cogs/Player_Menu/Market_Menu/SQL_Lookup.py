import Connections


def character_gold(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    character = cursor.fetchone()
    return character.Gold


def character_inventory(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "Select * " \
            "From Link_Character_Items " \
            "Where Character='{}' and Item not in (select Item from Main_Trade where Character = '{}') " \
            "Order by Item".format(character_name, character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


def character_owner(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Main_Characters where Character_Name='{}'".format(character_name)
    cursor.execute(query)
    result = cursor.fetchone()
    return int(result.Discord_ID)


def character_recycle_inventory_list(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "from Link_Character_Items " \
            "where Character='{}' and Item in (select Name from Info_Item) " \
            "order by Item".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        if row.Quantity == 1:
            items.append(row.Item)
        else:
            items.append(row.Item + " ({})".format(row.Quantity))
    return items


def character_item(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * from Link_Character_Items where Character='{}' AND Item = '{}'".format(character_name, item_name)
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


def trade_goods_types(character_name: str, gold_limit: float):
    cursor = Connections.sql_db_connection()
    query = "Select distinct b.Type " \
            "From Main_Trade a " \
            "Left join Info_Item b " \
            "On a.Item = b.Name " \
            "Where a.Price <= '{}' and a.Character != '{}' " \
            "Order by Type".format(gold_limit, character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    response = []
    for row in rows:
        if row.Type is None:
            response.append("Other")
        else:
            response.append(row.Type)
    response.sort()
    return response


def trade_goods_items_by_type(character_name: str, gold_limit: float, item_type: str):
    cursor = Connections.sql_db_connection()
    if item_type == "Other":
        query = "select a.Item " \
                "from Main_Trade a " \
                "left join Info_Item b " \
                "on a.Item = b.Name " \
                "where b.Type is null and a.price <= '{}' and a.Character != '{}' " \
                "group by a.Item " \
                "order by Item".format(gold_limit, character_name)
    else:
        query = "select a.Item " \
                "from Main_Trade a " \
                "left join Info_Item b " \
                "on a.Item = b.Name " \
                "where b.Type = '{}' and a.price <= '{}' " \
                "group by a.Item " \
                "order by Item".format(item_type, gold_limit)
    cursor.execute(query)
    item_name_list = cursor.fetchall()
    response = []
    for items in item_name_list:
        item_details = trade_item_not_sold_by_character(character_name, items.Item)
        if item_details is not None:
            response.append("{}: {}g each with {} for sale".format(item_details.Item, item_details.Price,
                                                                   item_details.Quantity))
    return response


def trade_item_not_sold_by_character(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Main_Trade " \
            "Where Item = '{}' and Character != '{}' " \
            "order by Price, Quantity desc".format(item_name, character_name)
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


def character_items_for_sale(character_name: str):
    cursor = Connections.sql_db_connection()
    query = "select Item, Price " \
            "from Main_Trade " \
            "where Character = '{}' " \
            "order by Item".format(character_name)
    cursor.execute(query)
    result = []
    rows = cursor.fetchall()
    for row in rows:
        result.append("{} - {}g".format(row.Item, row.Price))
    return result


def trade_item__character(character_name: str, item_name: str):
    cursor = Connections.sql_db_connection()
    query = "select * " \
            "From Main_Trade " \
            "Where Item = '{}' and Character = '{}' " \
            "order by Price, Quantity desc".format(item_name, character_name)
    cursor.execute(query)
    item = cursor.fetchone()
    return item
