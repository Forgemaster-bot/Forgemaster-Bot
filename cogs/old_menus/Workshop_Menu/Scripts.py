from old_menus.Workshop_Menu import SQL_Lookup
from old_menus.Workshop_Menu import SQL_Check
from old_menus.Workshop_Menu import SQL_Insert
from old_menus.Workshop_Menu import SQL_Update
from old_menus.Workshop_Menu import SQL_Delete
import Quick_Python
import Connections
import Update_Google_Roster
import random


def menu(character_id: str):
    if not SQL_Check.character_on_crafting_table(character_id):
        SQL_Insert.crafting(character_id)
    menu_list = ["Create a mundane item",
                 "Create a consumable item",
                 "Experiment with thaumstyn"]
    # "Create a recipe guide",
    # if caster
    number_of_classes = SQL_Lookup.character_count_classes(character_id)
    for rows in range(number_of_classes):
        class_name = SQL_Lookup.character_class_by_number(character_id, rows + 1)
        class_level = SQL_Lookup.character_class_level_by_class(character_id, class_name)
        if SQL_Check.class_is_spell_caster(character_id, class_name, class_level):
            if character_has_spells_to_view(character_id, class_name):
                menu_list.append("Create a scroll from your {} spells".format(class_name))
            if class_name == 'Wizard':
                menu_list.append("Scribe a spell into your spell book")
            if class_level == 'Warlock' and SQL_Check.character_has_tome(character_id):
                menu_list.append("Scribe a ritual into your book of shadows")
    menu_list.append("Work for someone this week")
    return menu_list


def character_info(character_id: str):
    character_list = []
    # Professions
    professions = SQL_Lookup.character_skills(character_id)
    if len(professions) > 0:
        character_list.append("**Professions:** {}".format(Quick_Python.list_to_string(professions)))
    # Essences
    essence_list = Quick_Python.list_to_string(SQL_Lookup.character_essences(character_id))
    character_list.append("**Essences:** {}".format(essence_list))
    # crafting details
    crafting = SQL_Lookup.character_crafting(character_id)
    character_list.append("**Crafting fund:** {}g **Workers:** {}".format(crafting.Crafting_Value,
                                                                          crafting.Labour_Points))
    # character gold
    gold = SQL_Lookup.character_gold(character_id)
    character_list.append("**Gold:** {}g".format(gold))
    return Quick_Python.list_to_table(character_list)


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


def get_character_name(character_id: str):
    character_name = SQL_Lookup.character_name_by_character_id(character_id)
    return character_name


def update_character_gold(character_id: str, reagent_cost):
    SQL_Update.character_gold(character_id, reagent_cost * -1)
    Update_Google_Roster.update_gold_group([character_id])

'''''''''''''''''''''''''''''''''''''''''
################Crafting##################
'''''''''''''''''''''''''''''''''''''''''


def crafting_limit(character_id: str):
    gold = SQL_Lookup.character_gold(character_id) * 2
    crafting = SQL_Lookup.character_crafting(character_id)
    craft_value = crafting.Crafting_Value

    if crafting.Labour_Points == 1:
        limit_list = [gold, 250]
    elif crafting.Labour_Points == 2:
        limit_list = [gold, 2500]
    elif crafting.Labour_Points > 2:
        limit_list = [gold, 25000]
    else:
        limit_list = [gold, craft_value]
    return min(limit_list)


def profession_list(character_id: str):
    result = SQL_Lookup.character_profession_list(character_id)
    return result


def character_has_profession_tools(character_id, profession: str):
    if SQL_Check.character_is_artificer_with_tools(character_id):
        return True, ""
    tool = SQL_Lookup.profession_tool(profession)
    if not SQL_Check.character_has_item(character_id, tool):
        character_name = SQL_Lookup.character_name_by_character_id(character_id)
        return False, "{} doesnt own a set of {} to craft with".format(character_name, tool)
    return True, ""


'''''''''''''''''''''''''''''''''''''''''
#################Working#################
'''''''''''''''''''''''''''''''''''''''''


def working_check(target_name: str):
    target_id = SQL_Lookup.character_id_by_character_name(target_name)
    result = SQL_Check.character_has_crafted_this_week(target_id)
    return result


async def work_confirm(self, discord_id, character_id: str, target_name, log):
    target_id = SQL_Lookup.character_id_by_character_name(target_name)
    employer_details = SQL_Lookup.character_crafting(target_id)
    if employer_details is None:
        SQL_Insert.crafting(target_id)
        new_labour = 1
        new_craft_value = 50
    else:
        new_labour = employer_details.Labour_Points + 1
        new_craft_value = employer_details.Crafting_Value
    # remove point from player
    SQL_Update.character_crafting(character_id, 0, 0)
    # add labour to employer
    SQL_Update.character_crafting(target_id, new_craft_value, new_labour)

    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)
    target_discord = self.bot.get_user(SQL_Lookup.character_owner(target_id))
    if target_discord is not None:
        await target_discord.send(log)


'''''''''''''''''''''''''''''''''''''''''
#############Scroll crafting#############
'''''''''''''''''''''''''''''''''''''''''


def craft_scroll_level_options(character_id: str, class_name: str, gold_limit):
    if gold_limit < 25:
        return []
    elif gold_limit < 50:
        spell_limit = 1
    elif gold_limit < 100:
        spell_limit = 2
    elif gold_limit < 250:
        spell_limit = 3
    elif gold_limit < 500:
        spell_limit = 4
    else:
        spell_limit = 4

    if class_name == 'Wizard':
        spell_level_list = SQL_Lookup.character_spell_level_list_spell_book(character_id)
    elif SQL_Check.class_learn_spells(class_name):
        spell_level_list = SQL_Lookup.character_spell_level_list_by_class(character_id, class_name)
    else:
        class_level = SQL_Lookup.character_class_level_by_class(character_id, class_name)
        max_spell_level = SQL_Lookup.class_max_spell_by_level(class_name, class_level)
        spell_level_list = []
        for row in range(1, max_spell_level + 1):
            row_list = [row, ""]
            spell_level_list.append(row_list)
    return_list = []
    for row in spell_level_list:
        # if row is null due to the ability being a racial then just skip it
        if not row:
            continue
        elif row[0] <= spell_limit:
            return_list.append("Level {} spell".format(row[0]))
    return return_list


def craft_scroll_spell_options(character_id: str, class_name: str, spell_level: int):
    if class_name == 'Wizard':
        spell_level_list = SQL_Lookup.character_known_wizard_spells_by_level(character_id, spell_level)
    elif SQL_Check.class_learn_spells(class_name):
        spell_level_list = SQL_Lookup.character_known_spells_by_class_and_level(character_id, class_name, spell_level)
    else:
        sub_class = SQL_Lookup.character_class_subclass(character_id, class_name)
        spell_level_list = SQL_Lookup.class_spells_by_level(class_name, sub_class, spell_level)
    return spell_level_list


def scroll_gold_cost(spell_level: int):
    if spell_level == '1':
        gold_cost = 30
    elif spell_level == '2':
        gold_cost = 50
    elif spell_level == '3':
        gold_cost = 100
    elif spell_level == '4':
        gold_cost = 250
    else:
        gold_cost = 500
    return gold_cost


async def create_scroll_confirm(self, command, discord_id, character_id, spell_level: int, spell_name, log):
    # update reagent
    reagent_cost = SQL_Lookup.spell_consumable_cost(spell_name)
    if reagent_cost > 0:
        reagent_total = SQL_Lookup.character_item_quantity(character_id, 'Universal Reagent')
        if reagent_cost > reagent_total:
            msg = "You do not have enough Universal Reagent for the consumable cost of the scroll"
            await command.message.author.send(msg)
            return "stop"
        else:
            SQL_Update.character_item_quantity(character_id, 'Universal Reagent', int(reagent_cost)*-1)
    # update gold
    gold_cost = scroll_gold_cost(spell_level)
    SQL_Update.character_gold(character_id, gold_cost*-1)

    # update crafting
    craft_details = SQL_Lookup.character_crafting(character_id)
    new_craft_value = int(craft_details[1]) - gold_cost
    if new_craft_value < 0:
        new_craft_value = 0
    SQL_Update.character_crafting(character_id, new_craft_value, 0)

    # create scroll in inventory
    item_name = "Scroll of {}".format(spell_name)
    if SQL_Check.character_has_item(character_id, item_name):
        SQL_Update.character_item_quantity(character_id, item_name, 1)
    else:
        SQL_Insert.character_item(character_id, item_name, 1)

    # add to logs
    Update_Google_Roster.update_items(character_id)
    Update_Google_Roster.update_gold_group([character_id])
    Connections.sql_log_private_command(discord_id, log)
    await Connections.log_to_discord(self, log)

'''''''''''''''''''''''''''''''''''''''''
#############Scribe Spell################
'''''''''''''''''''''''''''''''''''''''''


def get_item_quantity(character_id: str, item_name: str):
    return SQL_Lookup.character_item_quantity(character_id, item_name)


def reagent_quantity(character_id: str):
    item = 'Universal Reagent'
    return get_item_quantity(character_id, item)


def gold_quantity(character_id: str):
    return SQL_Lookup.character_gold(character_id)


def scribe_roll_bonus(character_id: str):
    arcane_prof = SQL_Lookup.character_has_arcane_proficiency(character_id)
    total_level = SQL_Lookup.character_total_level(character_id)
    prof_bonus = SQL_Lookup.proficiency_bonus(total_level)
    intelligence = SQL_Lookup.character_intelligence(character_id)
    total = int(arcane_prof * prof_bonus) + int((intelligence-10)/2)
    return total


def scribe_spell_list(character_id: str, reagent_limit: int, is_guaranteed: bool):
    # if the wizard wants a guaranteed scribe, then it'll cost 4x the modifier
    modifier = 50*4 if is_guaranteed else 50
    spell_limit = int(reagent_limit/modifier)
    spell_list = SQL_Lookup.character_scribe_spell_options(character_id, spell_limit)
    return spell_list


async def scribe_spell_confirm(self, command, discord_id, character_id, spell_name, spell_origin,
                               spell_level, ability_bonus, reagent_cost, skill_dc):
    item_consumed = 'Gold'
    character_name = get_character_name(character_id)

    # Perform skill check
    ability_roll = random.randint(1, 20)
    if skill_dc > ability_roll + ability_bonus:
        log = "**FAILURE**: {} rolled [{} + {}] against DC[{}]. **{}** was **not** copied into their spell book." \
            .format(character_name, ability_roll, ability_bonus, skill_dc, spell_name)
    else:
        log = "**SUCCESS**: {} rolled [{} + {}] against a DC[{}]. **{}** was copied into their spell book." \
            .format(character_name, ability_roll, ability_bonus, skill_dc, spell_name)
        book_id = SQL_Lookup.spell_book(character_id)
        SQL_Insert.spell_book_spell(book_id, spell_name)

    # Update users gold
    update_character_gold(character_id, reagent_cost)

    # Update item quantities
    if spell_origin == "a scroll":
        item_name = "Scroll of {}".format(spell_name)
        item_quantity = SQL_Lookup.character_item_quantity(character_id, item_name)
        if item_quantity > 1:
            SQL_Update.character_item_quantity(character_id, item_name, 1)
        else:
            SQL_Delete.character_item(character_id, item_name)
        log = "{} **{}** was consumed.".format(log, item_name)
    elif " Spell Book" in spell_origin:
        SQL_Delete.wizard_spell_share(character_id, spell_origin.replace(" Spell Book", ""), spell_name)

    # add to logs
    Update_Google_Roster.update_items(character_id)
    Connections.sql_log_private_command(discord_id, "Scribing: " + log)
    await Connections.log_to_discord(self, "Scribing:" + log)
    await command.author.send(log)
    return
