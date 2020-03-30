import Quick_Python
from Utility_Menu import SQL_Lookup


def info_skills():
    skill_list = SQL_Lookup.info_skills()
    reply = Quick_Python.stitch_string(skill_list)
    return reply


def info_classes():
    class_list = SQL_Lookup.info_classes()
    reply = Quick_Python.stitch_string(class_list)
    return reply
