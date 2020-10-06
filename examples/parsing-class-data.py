import os
import json
import re
import Connections

class_files = os.path.join('examples', 'data')
for class_file in os.listdir(class_files):

    with open(os.path.join(class_files, class_file), "r") as f:
        data = json.load(f)

    # allowed_sources = ['UA', 'PHB', 'SCAG', 'DMG', 'XGE', 'UAClericDivineDomains', 'UAOrderDomain',
    #                    'UAClericDruidWizard', 'UA2020SubclassesPt2']
    disallowed_sources = ['EGW', 'ERLW', 'EEG', 'GGR', 'MOT', 'Stream', 'Twitter', 'UAEberron', 'PSA', 'PSK',
                          'UAModernMagic']

    with Connections.sql_db_connection() as cursor:
        for dndclass in data['class']:
            parent = dndclass.get('name')
            for subclass in dndclass['subclasses']:
                name_source_data = re.split("[(|)]", subclass.get('shortName'))
                name = name_source_data[0].strip()
                source = subclass.get('source')

                if source in disallowed_sources:
                    print(f"'{source}' - Not allowed. Skipping '{name}'")
                    continue
                # print(f"\nparent='{parent}'; name='{name}'; source='{source}'")

                query = f"SELECT Class FROM [Info_Subclass] WHERE [Class] = ? AND [Sub_Class] = ?"
                args = [parent, name]
                print(f"query=\"{query}\" args={args}")
                cursor.execute(query, args)
                subclass_info = cursor.fetchval()

                # if subclass_info is None:
                #     query = f"INSERT INTO [Info_Subclass]([Class],[Sub_Class]) VALUES(?,?)"
                #     args = [parent, name]
                #     print(f"query=\"{query}\" args={args}")
                #     cursor.execute(query, args)

                # for known_type in subclass.get("additionalSpells", []):
                #     for type_values in known_type.values():
                #         for level_values in type_values.values():
                #             for spell in level_values:
                #                 print(f"Spell = {spell}")
                #                 # spell = spell.replace("'", "''")
                #                 query = f"SELECT [Name] FROM [Info_Spells] WHERE [Name] = ?"
                #                 args = [spell]
                #                 # print(f"query=\"{query}\" args={args}")
                #                 cursor.execute(query, args)
                #                 correct_spelling = cursor.fetchval()
                #                 if correct_spelling is None:
                #                     print(f"ERROR: '{spell}' does not exist in [Info_Spells]")
                #                     continue
                #                 spell = correct_spelling
                #
                #                 query = f"SELECT Spell FROM [Link_Class_Spells] WHERE [Class] = ? AND [Spell] = ?"
                #                 args = [name, spell]
                #                 # print(f"query=\"{query}\" args={args}")
                #                 cursor.execute(query, args)
                #                 linked_spell = cursor.fetchval()
                #                 if linked_spell is not None:
                #                     # print(f"'{spell}' already in [Link_Class_Spells] for subclass '{name}'")
                #                     continue
                #
                #                 query = f"INSERT INTO [Link_Class_Spells]([Class],[Spell]) VALUES(?,?)"
                #                 args = [name, spell]
                #                 print(f"query=\"{query}\" args={args}")
                #                 cursor.execute(query, args)
