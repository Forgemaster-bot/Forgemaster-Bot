from Player_Menu.Character_Sheet_Menu import SQL_Check
from Player_Menu.Character_Sheet_Menu import SQL_Lookup
from Player_Menu.Character_Sheet_Menu import SQL_Update
from Player_Menu.Character_Sheet_Menu import SQL_Insert
from Player_Menu.Character_Sheet_Menu import SQL_Delete
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
        class_name = SQL_Lookup.character_class_by_number(character_name, rows + 1)
        if SQL_Check.character_can_subclass(character_name, class_name):
            menu_list.append("Pick your subclass for {}".format(class_name))

        class_level = SQL_Lookup.character_class_level_by_class(character_name, class_name)
        if SQL_Check.class_is_spell_caster(character_name, class_name, class_level):
            if character_has_spells_to_view(character_name, class_name):
                menu_list.append("View your {} spells".format(class_name))
            if character_can_learn_spell(character_name, class_name, class_level):
                menu_list.append("Learn a new {} spell".format(class_name))
            if character_can_forget_spell(character_name, class_name):
                menu_list.append("Forget a {} spell".format(class_name))
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


def character_has_spells_to_view(character_name: str, class_name: str):
    # if wizard
    if class_name == 'Wizard':
        if SQL_Check.wizard_has_spells(character_name):
            return True
        else:
            return False
    # if learner caster
    elif SQL_Check.class_learn_spells(class_name):
        if SQL_Check.character_has_spells_by_class(character_name, class_name):
            return True
        else:
            return False
    return True


def character_can_learn_spell(character_name: str, class_name: str, class_level: int):
    if class_name == 'Wizard':
        wizard_spells = SQL_Lookup.spells_wizard_free_spells(character_name)
        if wizard_spells > 0:
            return True
    elif SQL_Check.class_learn_spells(class_name):
        character_spell_known = int(SQL_Lookup.character_known_spells_by_class(character_name, class_name))
        class_spells_known = int(SQL_Lookup.spells_known_by_level(class_name, class_level))
        if character_spell_known < class_spells_known:
            return True
    return False


def character_can_forget_spell(character_name: str, class_name: str):
    if SQL_Check.class_learn_spells(class_name):
        if SQL_Check.character_class_can_replace_spell(character_name, class_name):
            return True
    return False


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


async def level_up_confirm(self, character_name: str, class_name: str, discord_id: str, log: str):
    # get inputs data
    if SQL_Check.character_has_class(character_name, class_name):
        SQL_Update.character_class_level(character_name, class_name)
    else:
        number = SQL_Lookup.character_count_classes(character_name) + 1
        SQL_Insert.character_class(character_name, class_name, 1, number)

    # update spell options
    if SQL_Check.character_class_can_replace_spell(character_name, class_name):
        SQL_Update.character_forget_spell(character_name, class_name)
    if class_name == 'Wizard':
        SQL_Update.character_wizard_spell(character_name, class_name, 2)

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
################Spells##################
'''''''''''''''''''''''''''''''''''''''''


def spells_level_options(character_name: str, class_name: str):
    class_level = SQL_Lookup.character_class_level_by_class(character_name, class_name)
    max_spell_level = SQL_Lookup.character_max_spell_by_level(class_name, class_level)
    return_list = []
    for rows in range(1, max_spell_level+1):
        return_list.append("Level {} Spells".format(rows))
    return return_list


def class_must_learn_spells(class_name: str):
    return SQL_Check.class_learn_spells(class_name)


def view_spells_by_level(character_name: str, class_name: str, spell_level: int):
    sub_class = SQL_Lookup.character_class_subclass(character_name, class_name)
    spell_list = SQL_Lookup.class_spells_by_level(class_name, sub_class, spell_level)
    return Quick_Python.list_to_table(spell_list)


def view_spells_list_all_spells(character_name: str, class_name: str):
    spell_list = SQL_Lookup.character_spells_by_class(character_name, class_name)
    return Quick_Python.list_to_table(spell_list)


def view_spells_all_book_spells(character_name: str):
    spell_list = SQL_Lookup.character_spells_in_book(character_name)
    if len(spell_list) == 0:
        return "You dont have any spells written in your spell book"
    return Quick_Python.list_to_table(spell_list)


def learnable_spells_by_level(character_name: str, class_name: str, spell_level: int):
    sub_class = SQL_Lookup.character_class_subclass(character_name, class_name)

    if class_name == 'Wizard':
        known_spells = SQL_Lookup.character_known_wizard_spells_by_level(character_name, spell_level)
        if theurgy_check(sub_class, spell_level, known_spells):
            all_spells = SQL_Lookup.class_spells_by_level(class_name, 'Cleric', spell_level)
        else:
            all_spells = SQL_Lookup.class_spells_by_level(class_name, sub_class, spell_level)
    else:
        known_spells = SQL_Lookup.character_known_spells_by_class_and_level(character_name, class_name, spell_level)
        all_spells = SQL_Lookup.class_spells_by_level(class_name, sub_class, spell_level)
    for spell in known_spells:
        if spell in all_spells:
            all_spells.remove(spell)
    return all_spells


def theurgy_check(sub_class: str, spell_level, known_spells: list):
    domain = sub_class.replace("School of Theurgy ", "")
    domain_spells = SQL_Lookup.class_spells_at_and_below_level(domain, spell_level)
    for spell in known_spells:
        if spell in domain_spells:
            domain_spells.remove(spell)
    if len(domain_spells) > 0:
        return False
    return True


async def learning_spell_confirm(self, discord_id, character_name: str, class_name: str, spell_name: str, log):
    if class_name == 'Wizard':
        book_id = SQL_Lookup.spell_book(character_name)
        SQL_Insert.spell_book_spell(book_id, spell_name)
        # update number of free spells they have
        spell_number = SQL_Lookup.wizard_spell_number(character_name, class_name)
        SQL_Update.character_wizard_spell(character_name, class_name, spell_number - 1)
    else:
        spell_origin = SQL_Lookup.spell_origin(class_name, spell_name)
        if spell_origin is None:
            spell_origin = SQL_Lookup.character_class_subclass(character_name, class_name)
        SQL_Insert.character_spell(character_name, spell_origin, spell_name)
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)


def forget_spells_list(character_name: str, class_name: str, ):
    options = SQL_Lookup.character_spells_by_class(character_name, class_name)
    return options


async def forget_spell_confirm(self, discord_id, character_name: str, class_name: str, spell_name: str, log):
    spell_origin = SQL_Lookup.spell_origin(class_name, spell_name)
    if spell_origin is None:
        sub_class = SQL_Lookup.character_class_subclass(character_name, class_name)
        spell_origin = SQL_Lookup.spell_origin(sub_class, spell_name)
    SQL_Delete.character_forget_spell(character_name, spell_origin, spell_name)
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)

'''''''''''''''''''''''''''''''''''''''''
###############Utility##################
'''''''''''''''''''''''''''''''''''''''''


def profession_list():
    result = SQL_Lookup.info_skills()
    return result
