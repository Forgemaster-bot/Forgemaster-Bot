import gspread
from oauth2client.service_account import ServiceAccountCredentials


# return the sheet of your choice from the roster
def sheet(name: str):
    # connecting to google
    scope = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Credentials\GoogleAPI.json', scope)
    client = gspread.authorize(credentials)
    worksheet = client.open_by_key("1LzFoY8OT6ZbYL4lF10Ngz93lqYr97pP3iv8B3crdNyI").worksheet(name)
    return worksheet


def find_trade_seller(name: str, item: str):
    worksheet = sheet("Trade")
    row_count = len(worksheet.col_values(1))+1
    for row in range(row_count):
        if row in [0, 1]:
            continue
        # check name on row vs list
        if worksheet.cell(row, 1).value == name.lstrip() and worksheet.cell(row, 2).value == item.lstrip():
            return row
    return 0
