import Connections
from Quick_Python import run_query


def info_skills():
    query = "select Name from Info_Skills Where Job = 'True' ORDER BY Name"
    cursor = run_query(query)
    rows = cursor.fetchall()
    skills = []
    for row in rows:
        skills.append(row.Name)
    return skills


def info_classes():
    query = "select Class from Info_Classes ORDER BY Class "
    cursor = run_query(query)
    rows = cursor.fetchall()
    classes = []
    for row in rows:
        classes.append(row.Class)
    return classes
