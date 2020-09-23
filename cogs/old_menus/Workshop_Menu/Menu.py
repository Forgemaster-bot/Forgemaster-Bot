
import Crafting.Utils
from old_menus.Workshop_Menu import Scripts



async def profession_choice(self, command, character_id):
    # collect information about how much crafting can be done
    option_list = Scripts.profession_list(character_id)
    option_question = "Please enter the number of the profession to use."
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


'''''''''''''''''''''''''''''''''''''''''
#############Worker options###############
'''''''''''''''''''''''''''''''''''''''''


async def work_menu(self, command, discord_id, character_id):
    # get target name
    target_name = await work_character_choice(self, command, character_id)
    if target_name == "exit" or target_name == "stop":
        return target_name

    if not Scripts.working_check(target_name):
        await command.message.author.send("{} has already started working this week and cannot hire help"
                                          .format(target_name))
        return "stop"
    # confirm the transaction
    confirm = await work_confirm(self, command, discord_id, character_id, target_name)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return "stop"


async def work_character_choice(self, command, character_id):
    choice_question = "Type the name of the character you want to work for this week."
    choice = await self.character_name_lookup(command, choice_question, character_id)
    return choice


async def work_confirm(self, command, discord_id, character_id, target_name):
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want work for {} this week? [Yes/No]".format(target_name)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("working...")
        log = "{} is now working for {} this week".format(character_name, target_name)
        await Scripts.work_confirm(self, discord_id, character_id, target_name, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
##############Craft Scroll###############
'''''''''''''''''''''''''''''''''''''''''


async def new_craft_scroll_menu(ctx, character):
    await ctx.message.author.send("Craft Scroll Menu: Type **STOP** at any time to go back or **EXIT** to quit.")
    choice = await Crafting.Utils.query_until_data(ctx, character.get_class_dict(), 'your available classes')
    return await craft_scroll_menu(ctx.cog, ctx, character.info.discord_id, character.info.character_id, choice.name)


async def craft_scroll_menu(self, command, discord_id, character_id: str, class_name: str):
    welcome_message = "Craft {} Scroll Menu: Type **STOP** at any time to go back to the player menu."\
        .format(class_name)
    await command.message.author.send(welcome_message)

    gold_limit = Scripts.crafting_limit(character_id)
    spell_level_choice = await craft_scroll_level_choice(self, command, character_id, class_name, gold_limit)
    if spell_level_choice == "exit" or spell_level_choice == "stop":
        return spell_level_choice

    spell_choice = await craft_scroll_spell_choice(self, command, character_id, class_name, spell_level_choice)
    if spell_choice == "exit" or spell_choice == "stop":
        return spell_choice

    confirm = await create_scroll_confirm(self, command, discord_id, character_id, spell_level_choice, spell_choice)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return "stop"


async def craft_scroll_level_choice(self, command, character_id, class_name, gold_limit: float):
    option_list = Scripts.craft_scroll_level_options(character_id, class_name, gold_limit)
    option_question = "What spell level is the scroll you want to craft?"
    choice = await self.answer_from_list(command, option_question, option_list)
    result = choice.replace("Level ", "").replace(" spell", "")
    return result


async def craft_scroll_spell_choice(self, command, character_id, class_name, spell_level: int):
    option_list = Scripts.craft_scroll_spell_options(character_id, class_name, spell_level)
    option_question = "Which spell would you like to create a scroll of?"
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def create_scroll_confirm(self, command, discord_id, character_id, spell_level: int, spell_name):
    character_name = Scripts.get_character_name(character_id)
    gold_cost = Scripts.scroll_gold_cost(spell_level)
    question = "Do you want to create a scroll of {} for {}g? [Yes/No]".format(spell_name, gold_cost)
    log = "{} created a scroll of {}.".format(character_name, spell_name)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("creating scroll...")
        await Scripts.create_scroll_confirm(self, command, discord_id, character_id, spell_level, spell_name, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
##############scribe spell###############
'''''''''''''''''''''''''''''''''''''''''


async def scribe_spell_menu(self, command, discord_id, character_id: str):
    gold_quantity = Scripts.gold_quantity(character_id)
    ability_bonus = Scripts.scribe_roll_bonus(character_id)
    welcome_message = "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n" \
                      "Scribe spell Menu: Type **STOP** at any time to go back to the player menu. \n" \
                      "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n" \
                      "Options for scribing and details regarding cost:\n" \
                      "\tDC Check: \n" \
                      "\t\t- Cost = 50gp x spell level;\n" \
                      "\t\t- Additionally, you must meet meet a DC of 10 + spell level or it will fail to copy. " \
                      "**Failure will destroy scrolls**, but spellbooks will remain intact.\n" \
                      "\tGuaranteed: \n" \
                      "\t\t- Cost = 200gp x spell level;\n" \
                      "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n" \
                      "You currently have {}gp and +{} to your DC roll.\n"\
        .format(gold_quantity, ability_bonus)
    await command.message.author.send(welcome_message)

    # Determine if wizard wants to be guaranteed the result
    is_guaranteed = await scribe_modifier_choice(self, command)
    if is_guaranteed == "exit" or is_guaranteed == "stop":
        return "exit"

    # Display list of spells and get user to pick spell based on available gold
    spell_choice = await scribe_spell_choice(self, command, character_id, gold_quantity, is_guaranteed)
    if spell_choice == "exit" or spell_choice == "stop":
        return spell_choice

    # Confirm the costs and roll withe user
    confirm = \
        await scribe_spell_confirm(self, command, discord_id, character_id, spell_choice, ability_bonus, is_guaranteed)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return "stop"


async def scribe_modifier_choice(self, command):
    option_question = "Which option would you like to continue scribing with?"
    # Create list for asking user
    option_random = "DC Check"
    option_guaranteed = "Guaranteed"
    option_list = [option_random, option_guaranteed]
    # Ask user question
    choice = await self.answer_from_list(command, option_question, option_list)
    # Check the answer
    if choice == "exit" or choice == "stop":
        return choice
    elif choice == option_guaranteed:
        return True
    return False


async def scribe_spell_choice(self, command, character_id, reagent_quantity, is_guaranteed):
    option_list = Scripts.scribe_spell_list(character_id, reagent_quantity, is_guaranteed)
    option_question = "Which spell would you like to learn?"
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def scribe_spell_confirm(self, command, discord_id, character_id, spell, ability_bonus, is_guaranteed):
    spell_detail = spell.split(":")
    spell_level = spell_detail[0].replace("[Level ", "").replace(" Spell]", "")
    spell_name = spell_detail[1].replace(";\t From", "").replace("**", "").lstrip()
    spell_origin = spell_detail[2].lstrip()

    # Determine costs
    reagent_cost = int(spell_level) * (50*4 if is_guaranteed else 50)
    skill_dc = 0 if is_guaranteed else (int(spell_level)+10)

    question = "Scribing **{}** from **{}** will cost **{}gp** and you must pass a **DC[{}]** Arcana roll.\n" \
               "Do you want to try and scribe this spell into your spellbook? [Yes/No]\n" \
        .format(spell_name, spell_origin, reagent_cost, skill_dc)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Attempting to scribe...")
        await Scripts.scribe_spell_confirm(self, command, discord_id, character_id, spell_name,
                                           spell_origin, spell_level, ability_bonus, reagent_cost, skill_dc)
    return "stop"
