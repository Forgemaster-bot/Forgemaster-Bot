import os
import json
import re
import Connections

cleric_file = os.path.join('examples', 'data', 'class-cleric.json')

with open(cleric_file, "r") as f:
    data = json.load(f)

allowed_sources = ['UA', 'PHB', 'SCAG', 'DMG', 'XGE', 'UAClericDivineDomains', 'UAOrderDomain', 'UAClericDruidWizard',
                   'UA2020SubclassesPt2']

with Connections.sql_db_connection() as cursor:
    for dndclass in data['class']:
        parent = dndclass.get('name')
        for subclass in dndclass['subclasses']:
            name_source_data = re.split("[(|)]", subclass.get('name'))

            name = name_source_data[0].strip()
            source = subclass.get('source')

            if source not in allowed_sources:
                print(f"Skipping '{name}' subclass as '{source}' is not allowed.")
                continue
            print(f"\nname='{name}'; source='{source}'")

            query = f"SELECT Class FROM [Info_Subclass] WHERE [Class] = ? AND [Sub_Class] = ?"
            args = [parent, name]
            # print(f"query=\"{query}\" args={args}")
            cursor.execute(query, args)
            subclass_info = cursor.fetchval()

            if subclass_info is None:
                query = f"INSERT INTO [Info_Subclass]([Class],[Sub_Class]) VALUES(?,?)"
                args = [parent, name]
                print(f"query=\"{query}\" args={args}")
                cursor.execute(query, args)

            for known_type in subclass.get("additionalSpells"):
                for type_values in known_type.values():
                    for level_values in type_values.values():
                        for spell in level_values:
                            # spell = spell.replace("'", "''")
                            query = f"SELECT [Name] FROM [Info_Spells] WHERE [Name] = ?"
                            args = [spell]
                            # print(f"query=\"{query}\" args={args}")
                            cursor.execute(query, args)
                            correct_spelling = cursor.fetchval()
                            if correct_spelling is None:
                                print(f"ERROR: '{spell}' does not exist in [Info_Spells]")
                                continue
                            spell = correct_spelling

                            query = f"SELECT Spell FROM [Link_Class_Spells] WHERE [Class] = ? AND [Spell] = ?"
                            args = [name, spell]
                            # print(f"query=\"{query}\" args={args}")
                            cursor.execute(query, args)
                            linked_spell = cursor.fetchval()
                            if linked_spell is not None:
                                # print(f"'{spell}' already in [Link_Class_Spells] for subclass '{name}'")
                                continue

                            query = f"INSERT INTO [Link_Class_Spells]([Class],[Spell]) VALUES(?,?)"
                            args = [name, spell]
                            print(f"query=\"{query}\" args={args}")
                            cursor.execute(query, args)
