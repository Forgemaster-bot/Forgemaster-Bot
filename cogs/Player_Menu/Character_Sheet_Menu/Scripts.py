from Player_Menu.Character_Sheet_Menu import SQL_Check
from Player_Menu.Character_Sheet_Menu import SQL_Lookup
from Player_Menu.Character_Sheet_Menu import SQL_Update
from Player_Menu.Character_Sheet_Menu import SQL_Insert
import Update_Google_Roster
import Connections
import Quick_Python


def menu(character_name: str):
    menu_list = ["View inventory"]
    character_level = SQL_Lookup.character_sum_class_levels(character_name)
    character_xp = SQL_Lookup.character_xp(character_name)
    if SQL_Check.character_can_level_up(character_level, character_xp):
        menu_list.append("Level up your character")
    if not SQL_Check.character_has_professions(character_name):
        menu_list.append("Pick your free crafting profession")
    number_of_classes = SQL_Lookup.character_count_classes(character_name)
    for rows in range(number_of_classes):
        if SQL_Check.character_can_subclass(character_name, rows+1):
            class_name = SQL_Lookup.character_class_by_number(character_name, rows + 1)
            menu_list.append("Pick your subclass for {}".format(class_name))
        # if class can cast spells
        # show spells for class

    menu_list.append("View spell book")
    return menu_list


def character_info(character_name: str):
    character_list = ["**Name:** {}".format(character_name)]
    # classes
    classes_and_levels = Quick_Python.list_to_string(SQL_Lookup.character_class_and_levels(character_name))
    character_list.append("**Class:** {}".format(classes_and_levels))
    # stats
    stats = SQL_Lookup.character_stats(character_name)
    character_list.append("**Stats:** STR: {}, DEX: {}, CON: {}, INT: {}, WIS: {}, CHA: {}"
                          .format(stats.STR, stats.DEX, stats.CON, stats.INT, stats.WIS, stats.CHA))
    # feats
    feats = SQL_Lookup.character_feats(character_name)
    if len(feats) > 0:
        character_list.append("**Feats:** {}".format(Quick_Python.list_to_string(feats)))
    # professions
    professions = SQL_Lookup.character_skills(character_name)
    if len(professions) > 0:
        character_list.append("**Professions:** {}".format(Quick_Python.list_to_string(professions)))
    return Quick_Python.list_to_table(character_list)


'''''''''''''''''''''''''''''''''''''''''
###############Inventory##################
'''''''''''''''''''''''''''''''''''''''''


def inventory_list(character_name):
    item_list = SQL_Lookup.character_inventory(character_name)
    result = Quick_Python.list_to_string(item_list)
    return result


'''''''''''''''''''''''''''''''''''''''''
###############Leveling##################
'''''''''''''''''''''''''''''''''''''''''


def character_classes(character_name: str):
    classes_and_levels = SQL_Lookup.character_class_and_levels(character_name)
    result = Quick_Python.list_to_string(classes_and_levels)
    return result


def level_up_options(character_name: str):
    class_number = SQL_Lookup.character_count_classes(character_name)
    if class_number == 3:
        class_list = SQL_Lookup.character_class_list(character_name)
    else:
        current_classes = SQL_Lookup.character_class_list(character_name)
        character_stats = SQL_Lookup.character_stats(character_name)
        class_list = []
        if character_stats.INT > 12:
            class_list.append("Artificer")
        if character_stats.STR > 12:
            class_list.append("Barbarian")
        if character_stats.CHA > 12:
            class_list.append("Bard")
        if character_stats.WIS > 12:
            class_list.append("Cleric")
        if character_stats.WIS > 12:
            class_list.append("Druid")
        if character_stats.STR > 12 or character_stats.DEX > 12:
            class_list.append("Fighter")
        if character_stats.DEX > 12 and character_stats.WIS > 12:
            class_list.append("Monk")
        if character_stats.STR > 12 and character_stats.CHA > 12:
            class_list.append("Paladin")
        if character_stats.DEX > 12 and character_stats.WIS > 12:
            class_list.append("Ranger")
        if character_stats.DEX > 12:
            class_list.append("Rogue")
        if character_stats.CHA > 12:
            class_list.append("Sorcerer")
        if character_stats.CHA > 12:
            class_list.append("Warlock")
        if character_stats.INT > 12:
            class_list.append("Wizard")
        for classes in current_classes:
            if classes not in class_list:
                class_list.append(classes)
        class_list.sort()
    return class_list


async def level_up(self, character_name: str, character_class: str, discord_id: str, log: str):
    # get inputs data
    if SQL_Check.character_has_class(character_name, character_class):
        SQL_Update.character_class_level(character_name, character_class)
    else:
        number = SQL_Lookup.character_count_classes(character_name) + 1
        SQL_Insert.character_class(character_name, character_class, 1, number)

    Update_Google_Roster.update_classes(character_name)
    Update_Google_Roster.update_level(character_name)
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)
    return


'''''''''''''''''''''''''''''''''''''''''
###############Subclass##################
'''''''''''''''''''''''''''''''''''''''''


def subclass_options(class_choice):
    choice_list = SQL_Lookup.subclasses(class_choice)
    return choice_list


async def subclass_confirm(self, character_name: str, class_choice: str, subclass: str, discord_id: str, log: str):
    # update class details
    SQL_Update.character_subclass(character_name, class_choice, subclass)

    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)


'''''''''''''''''''''''''''''''''''''''''
##############Profession#################
'''''''''''''''''''''''''''''''''''''''''


async def give_profession(self, character_name: str, profession_name: str, discord_id: str, log: str):
    # get inputs data
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)
    SQL_Insert.character_profession(character_name, profession_name, 1)
    Update_Google_Roster.update_skill(character_name)
    return


'''''''''''''''''''''''''''''''''''''''''
###############Utility##################
'''''''''''''''''''''''''''''''''''''''''


def profession_list():
    result = SQL_Lookup.info_skills()
    return result
