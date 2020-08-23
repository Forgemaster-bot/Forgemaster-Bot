from Player_Menu.Character_Sheet_Menu import SQL_Check
from Player_Menu.Character_Sheet_Menu import SQL_Lookup
from Player_Menu.Character_Sheet_Menu import SQL_Update
from Player_Menu.Character_Sheet_Menu import SQL_Insert
from Player_Menu.Character_Sheet_Menu import SQL_Delete
import Update_Google_Roster
import Connections
import Quick_Python
from Character.Character import Character


# def menu(character: Character):
#     # Check for conditional menu conditions
#     can_level_up = character.can_level_up()
#     has_profession = any(character.skills)
#     available_subclasses = [c for c in character.classes if not c.subclass_is_picked()]
#     is_warlock = character.has_class("Warlock")
#     is_divine_soul = character.has_subclass("Divine Soul")
#
#     menu_list = []
#     menu_list.append("View inventory")
#     menu_list.append("Level up your character" if can_level_up else None)
#     menu_list.append("Pick your free crafting profession" if has_profession else None)
#     menu_list.append("Pick your subclass for {}".format(c) for c in available_subclasses)
#     menu_list.append("Warlock Pack Boon choice" if is_warlock else None)
#     menu_list.append("Divine Soul affinity spell choice" if is_divine_soul else None)
#     return menu_list


def menu(character_id: str):
    menu_list = ["View inventory"]
    character_level = SQL_Lookup.character_sum_class_levels(character_id)
    character_xp = SQL_Lookup.character_xp(character_id)
    if SQL_Check.character_can_level_up(character_level, character_xp):
        menu_list.append("Level up your character")
    if not SQL_Check.character_has_professions(character_id):
        menu_list.append("Pick your free crafting profession")
    number_of_classes = SQL_Lookup.character_count_classes(character_id)
    for rows in range(number_of_classes):
        class_name = SQL_Lookup.character_class_by_number(character_id, rows + 1)
        if SQL_Check.character_can_subclass(character_id, class_name):
            menu_list.append("Pick your subclass for {}".format(class_name))
        class_level = SQL_Lookup.character_class_level_by_class(character_id, class_name)
        if SQL_Check.class_choice(character_id, class_name):
            sub_class_name = SQL_Lookup.character_class_subclass(character_id, class_name)
            if class_name == 'Warlock':
                menu_list.append("Warlock Pack Boon choice")
            elif sub_class_name == 'Divine Soul':
                menu_list.append("Divine Soul affinity spell choice".format(sub_class_name))
        if SQL_Check.class_is_spell_caster(character_id, class_name, class_level):
            if character_has_spells_to_view(character_id, class_name):
                menu_list.append("View your {} spells".format(class_name))
            if character_can_learn_spell(character_id, class_name, class_level):
                menu_list.append("Learn a new {} spell".format(class_name))
            if character_can_forget_spell(character_id, class_name):
                menu_list.append("Forget a {} spell".format(class_name))

    return menu_list


def character_info(character_id: str):
    character = Character(character_id)
    return character.formatted_character_info()


def character_has_spells_to_view(character_id: str, class_name: str):
    # if wizard
    if class_name == 'Wizard':
        if SQL_Check.wizard_has_spells(character_id):
            return True
        else:
            return False
    # if learner caster
    elif SQL_Check.class_learn_spells(class_name):
        if SQL_Check.character_has_spells_by_class(character_id, class_name):
            return True
        else:
            return False
    return True


def character_can_learn_spell(character_id: str, class_name: str, class_level: int):
    if class_name == 'Wizard':
        wizard_spells = SQL_Lookup.spells_wizard_free_spells(character_id)
        if wizard_spells > 0:
            return True
    elif SQL_Check.class_learn_spells(class_name):
        character_spell_known = int(SQL_Lookup.character_known_spells_by_class(character_id, class_name))
        class_spells_known = int(SQL_Lookup.spells_known_by_level(class_name, class_level))
        if character_spell_known < class_spells_known:
            return True
    return False


def character_can_forget_spell(character_id: str, class_name: str):
    if SQL_Check.class_learn_spells(class_name):
        if SQL_Check.character_class_can_replace_spell(character_id, class_name):
            return True
    return False


def get_character_name(character_id: str):
    character_name = SQL_Lookup.character_name_by_character_id(character_id)
    return character_name


'''''''''''''''''''''''''''''''''''''''''
###############Inventory##################
'''''''''''''''''''''''''''''''''''''''''


def inventory_list(character_id):
    item_list = SQL_Lookup.character_inventory(character_id)
    result = Quick_Python.list_to_string(item_list)
    return result


'''''''''''''''''''''''''''''''''''''''''
###############Leveling##################
'''''''''''''''''''''''''''''''''''''''''


def character_classes(character_id: str):
    classes_and_levels = SQL_Lookup.character_class_and_levels(character_id)
    result = Quick_Python.list_to_string(classes_and_levels)
    return result


def level_up_options(character_id: str):
    class_number = SQL_Lookup.character_count_classes(character_id)
    if class_number == 3:
        class_list = SQL_Lookup.character_class_list(character_id)
    else:
        current_classes = SQL_Lookup.character_class_list(character_id)
        character_stats = SQL_Lookup.character_stats(character_id)
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


def wizard_update_core_spellbook(character_id: str):
    book_id = SQL_Lookup.spell_book(character_id)
    if book_id is None:
        character_name = SQL_Lookup.character_name_by_character_id(character_id)
        SQL_Insert.character_spell_book(character_id, character_name, 'Core')
        book_id = SQL_Lookup.spell_book(character_id)
    return book_id


def wizard_update_spellslots(character_id: str, class_name: str, is_first_level: bool):
    num_spells = SQL_Lookup.spells_wizard_free_spells(character_id)
    # Give 2 spell slots; except if their a first level wizard give them 6 spells slots
    additional_slots = 6 if is_first_level else 2
    SQL_Update.character_free_spell(character_id, class_name, num_spells + additional_slots)


async def level_up_confirm(self, character_id: str, class_name: str, discord_id: str, log: str):
    # get inputs data
    is_first_level = False
    if SQL_Check.character_has_class(character_id, class_name):
        SQL_Update.character_class_level(character_id, class_name)
    else:
        is_first_level = True
        number = SQL_Lookup.character_count_classes(character_id) + 1
        SQL_Insert.character_class(character_id, class_name, 1, number)

    # update spell options
    if SQL_Check.class_can_replace_spell(class_name):
        SQL_Update.character_forget_spell_allow(character_id, class_name)
    if class_name == 'Wizard':
        wizard_update_spellslots(character_id, class_name, is_first_level)
        wizard_update_core_spellbook(character_id)

    if SQL_Lookup.character_sum_class_levels(character_id) > 6:
        SQL_Update.update_player_character_total(discord_id)

    Update_Google_Roster.update_classes(character_id)
    Update_Google_Roster.update_level(character_id)
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)
    return


'''''''''''''''''''''''''''''''''''''''''
###############Subclass##################
'''''''''''''''''''''''''''''''''''''''''


def subclass_options(class_choice):
    choice_list = SQL_Lookup.subclasses(class_choice)
    return choice_list


async def subclass_confirm(self, character_id: str, class_choice: str, subclass: str, discord_id: str, log: str):
    # update class details
    SQL_Update.character_subclass(character_id, class_choice, subclass)
    if subclass == 'Divine Soul':
        SQL_Update.character_sub_class_option(character_id, "Sorcerer", True)
    if class_choice == 'Warlock':
        SQL_Update.character_sub_class_option(character_id, "Warlock", True)
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)


'''''''''''''''''''''''''''''''''''''''''
##############Profession#################
'''''''''''''''''''''''''''''''''''''''''


async def give_profession(self, character_id: str, profession_name: str, discord_id: str, log: str):
    # get inputs data
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)
    SQL_Insert.character_profession(character_id, profession_name, 1)
    Update_Google_Roster.update_skill(character_id)
    return


'''''''''''''''''''''''''''''''''''''''''
################Spells##################
'''''''''''''''''''''''''''''''''''''''''


def spells_level_options(character_id: str, class_name: str):
    class_level = SQL_Lookup.character_class_level_by_class(character_id, class_name)
    max_spell_level = SQL_Lookup.character_max_spell_by_level(class_name, class_level)
    return_list = []
    for rows in range(1, max_spell_level+1):
        return_list.append("Level {} Spells".format(rows))
    return return_list


def class_must_learn_spells(class_name: str):
    return SQL_Check.class_learn_spells(class_name)


def view_spells_by_level(character_id: str, class_name: str, spell_level: int):
    sub_class = SQL_Lookup.character_class_subclass(character_id, class_name)
    spell_list = SQL_Lookup.class_spells_by_level(class_name, sub_class, spell_level)
    return Quick_Python.list_to_table(spell_list)


def view_spells_list_all_spells(character_id: str, class_name: str):
    spell_list = SQL_Lookup.character_spells_by_class(character_id, class_name)
    return Quick_Python.list_to_table(spell_list)


def view_spells_all_book_spells(character_id: str):
    spell_list = SQL_Lookup.character_spells_in_book(character_id)
    if len(spell_list) == 0:
        return "You dont have any spells written in your spell book"
    return Quick_Python.list_to_table(spell_list)


def learnable_spells_by_level(character_id: str, class_name: str, spell_level: int):
    sub_class = SQL_Lookup.character_class_subclass(character_id, class_name)

    if class_name == 'Wizard':
        known_spells = SQL_Lookup.character_known_wizard_spells_by_level(character_id, spell_level)
        if theurgy_check(sub_class, spell_level, known_spells):
            all_spells = SQL_Lookup.class_spells_by_level(class_name, 'Cleric', spell_level)
        else:
            all_spells = SQL_Lookup.class_spells_by_level(class_name, sub_class, spell_level)
    else:
        known_spells = SQL_Lookup.character_known_spells_by_class_and_level(character_id, class_name, spell_level)
        all_spells = SQL_Lookup.class_spells_by_level(class_name, sub_class, spell_level)
    for spell in known_spells:
        if spell in all_spells:
            all_spells.remove(spell)
    return all_spells


def theurgy_check(sub_class: str, spell_level, known_spells: list):
    if sub_class is None:
        return False
    domain = sub_class.replace("School of Theurgy ", "")
    domain_spells = SQL_Lookup.class_spells_at_and_below_level(domain, spell_level)
    for spell in known_spells:
        if spell in domain_spells:
            domain_spells.remove(spell)
    if len(domain_spells) > 0:
        return True
    return False


async def learning_spell_confirm(self, discord_id, character_id: str, class_name: str, spell_name: str, log):
    if class_name == 'Wizard':
        # insert spell into spell book
        book_id = wizard_update_core_spellbook(character_id)
        SQL_Insert.spell_book_spell(book_id, spell_name)
        # update number of free spells they have
        spell_number = SQL_Lookup.wizard_spell_number(character_id, class_name)
        SQL_Update.character_free_spell(character_id, class_name, spell_number - 1)

    else:
        spell_origin = SQL_Lookup.spell_origin(class_name, spell_name)
        if spell_origin is None:
            spell_origin = SQL_Lookup.character_class_subclass(character_id, class_name)
        SQL_Insert.character_spell(character_id, spell_origin, spell_name)
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log.replace("''", "'"))


def forget_spells_list(character_id: str, class_name: str, ):
    options = SQL_Lookup.character_spells_by_class(character_id, class_name)
    return options


async def forget_spell_confirm(self, discord_id, character_id: str, class_name: str, spell_name: str, log):
    spell_origin = SQL_Lookup.spell_origin(class_name, spell_name)
    if spell_origin is None:
        sub_class = SQL_Lookup.character_class_subclass(character_id, class_name)
        spell_origin = SQL_Lookup.spell_origin(sub_class, spell_name)

    SQL_Delete.character_forget_spell(character_id, spell_origin, spell_name)
    SQL_Update.character_forget_spell_stop(character_id, class_name)

    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)


'''''''''''''''''''''''''''''''''''''''''
###########Sub_Class Choices#############
'''''''''''''''''''''''''''''''''''''''''


async def divine_soul_confirm(self, discord_id, character_id: str, spell_name: str, log):
    SQL_Insert.character_spell(character_id, "Divine Soul affinity", spell_name)
    SQL_Update.character_sub_class_option(character_id, "Sorcerer", False)
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log.replace("''", "'"))


async def warlock_tome_confirm(self, discord_id, character_id: str, reply: str, log):
    if reply == 'Yes':
        character_name = SQL_Lookup.character_name_by_character_id(character_id)
        SQL_Insert.character_spell_book(character_id, character_name, 'Tome')
        SQL_Update.character_free_spell(character_id, "Warlock", 2)
    SQL_Update.character_sub_class_option(character_id, "Warlock", False)
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log.replace("''", "'"))

'''''''''''''''''''''''''''''''''''''''''
###############Utility##################
'''''''''''''''''''''''''''''''''''''''''


def profession_list():
    result = SQL_Lookup.info_skills()
    return result
