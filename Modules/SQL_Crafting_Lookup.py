import Quick_SQL


def character_skill_profession(character_name: str):
    cursor = Quick_SQL.db_connection()
    query = "Select A.* " \
            "From Link_Character_Skills A " \
            "Left Join Info_Skills B " \
            "On A.Skill = B.Name " \
            "where Character = '{}' and B.Job = 1".format(character_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    skill_list = []
    for row in rows:
        skill_list.append(row.Skill)
    return skill_list

