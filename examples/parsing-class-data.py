import os
import json
import re
import Connections

add_to_database = True
print_query = True
only_one_additionalSpells = True

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

uses_short_name = ['Cleric']
ignore = ['Circle of the Land', 'Gunslinger', 'Echo Knight', 'Order', 'Circle of Spores']

class_files = os.path.join('examples', 'data')
for class_file in os.listdir(class_files):

    with open(os.path.join(class_files, class_file), "r") as f:
        data = json.load(f)

    disallowed_sources = ['EGW', 'ERLW', 'EEG', 'GGR', 'MOT', 'Stream', 'Twitter', 'UAEberron', 'PSA', 'PSK',
                          'UAModernMagic', 'Livestream']

    with Connections.sql_db_connection() as cursor:
        for dndclass in data['class']:
            parent = dndclass.get('name')
            print(f"{bcolors.HEADER}{parent}{bcolors.ENDC}")
            for subclass in dndclass['subclasses']:
                name_source_data = subclass.get('shortName' if parent in uses_short_name else 'name')
                name_source_data = re.split("[(|)]", name_source_data)
                name = name_source_data[0].strip()
                source = subclass.get('source')

                if source in disallowed_sources:
                    print(f"'{source}' - Not allowed. Skipping '{name}'")
                    continue
                elif name in ignore:
                    print(f"'{name}' - In ignore list. Skipping")
                    continue
                # print(f"\nparent='{parent}'; name='{name}'; source='{source}'")
                query = f"SELECT Class FROM [Info_Subclass] WHERE [Class] = ? AND [Sub_Class] = ?"
                args = [parent, name]
                #if print_query: print(f"query=\"{query}\" args={args}")
                cursor.execute(query, args)
                subclass_info = cursor.fetchval()

                if subclass_info is None:
                    print(f">{bcolors.BOLD}{name}{bcolors.ENDC}")
                    query = f"INSERT INTO [Info_Subclass]([Class],[Sub_Class]) VALUES(?,?)"
                    args = [parent, name]
                    if print_query: print(f"query=\"{query}\" args={args}")
                    if add_to_database: cursor.execute(query, args)
                #else:
                #    print(f"{name}")

                subclass_spells = subclass.get("additionalSpells", [])
                if only_one_additionalSpells and len(subclass_spells) > 1:
                    print(f"\t{bcolors.FAIL}Multiple items found under {name} additionalSpells... May need to input by hand.{bcolors.ENDC}")
                    continue

                for known_type in subclass_spells:
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
                                    print(f"\t{bcolors.FAIL}ERROR: '{spell}' does not exist in [Info_Spells]{bcolors.ENDC}")
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
                                print(f"\t{bcolors.BOLD}+{spell}{bcolors.ENDC}")
                                query = f"INSERT INTO [Link_Class_Spells]([Class],[Spell]) VALUES(?,?)"
                                args = [name, spell]
                                if print_query: print(f"\tquery=\"{query}\" args={args}")
                                if add_to_database: cursor.execute(query, args)
    print("\n#########################################\n")
