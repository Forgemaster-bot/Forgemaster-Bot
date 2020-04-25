from Player_Menu.Workshop_Menu import Scripts


async def main_menu(self, command, discord_id: int, character_id: str):
    while True:
        choice = await menu_options(self, command, character_id)
        if choice == "Create a mundane item":
            while True:
                menu = await mundane_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif choice == "Create a consumable item":
            while True:
                menu = await consumable_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif choice == "Create a recipe guide":
            await command.message.author.send("coming soon")
        elif choice == "Experiment with essences":
            while True:
                menu = await experiment_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif choice == "View your recipes":
            while True:
                menu = await recipe_menu(self, command, character_id)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif "Create a scroll from your " in choice:
            while True:
                class_choice = choice.replace("Create a scroll from your ", "").replace(" spells", "")
                menu = await craft_scroll_menu(self, command, discord_id, character_id, class_choice)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif choice == "Scribe a spell into your spell book":
            while True:
                menu = await scribe_spell_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif choice == "Work for someone this week":
            while True:
                menu = await work_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif choice == "exit" or choice == "stop":
            return choice


async def menu_options(self, command, character_id):
    option_list = Scripts.menu(character_id)
    details = Scripts.character_info(character_id)
    option_question = "Workshop Menu: " \
                      "Type **STOP** at any time to go back to the player menu \n" \
                      "{} \n" \
                      "What would you like to do?".format(details)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def profession_choice(self, command, character_id):
    # collect information about how much crafting can be done
    option_list = Scripts.profession_list(character_id)
    option_question = "Please enter the number of the profession to use."
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


'''''''''''''''''''''''''''''''''''''''''
################Mundane##################
'''''''''''''''''''''''''''''''''''''''''


async def mundane_menu(self, command, discord_id, character_id: str):
    gold_limit = Scripts.crafting_limit(character_id)
    if gold_limit == 0:
        await command.message.author.send("you cannot craft any more this week")
        return "stop"
    profession = await profession_choice(self, command, character_id)
    if profession == "exit" or profession == "stop":
        return profession

    character_has_tools = Scripts.character_has_profession_tools(character_id, profession)
    if not character_has_tools[0]:
        await command.message.author.send(character_has_tools[1])
        return

    # get the type of item they want to craft
    item_type = await mundane_type_choice(self, command, profession, gold_limit)
    if item_type == "exit" or item_type == "stop":
        return item_type

    # get the name of the item
    item_name = await mundane_item_choice(self, command, profession, gold_limit, item_type)
    if item_name == "exit" or item_name == "stop":
        return item_name
    # get the quantity
    quantity = await mundane_quantity(self, command, gold_limit, item_name)
    if quantity == "exit" or quantity == "stop":
        return quantity

    # confirm crafting
    confirm = await craft_mundane_confirm(self, command, discord_id, character_id, item_name, quantity)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return


async def mundane_type_choice(self, command, profession, gold_limit):
    option_list = Scripts.mundane_item_type(profession, gold_limit)
    option_question = "What type of item do you want to craft?".format(profession)
    if len(option_list) == 1:
        choice = option_list[0]
    else:
        choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def mundane_item_choice(self, command, profession, gold_limit, item_type):
    option_list = Scripts.mundane_item(profession, gold_limit, item_type)
    option_question = "What item do you want to craft?"
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def mundane_quantity(self, command, gold_limit, item_name):
    item_craft_cost = Scripts.mundane_craft_cost(item_name)
    maximum = int(gold_limit / item_craft_cost)
    if item_craft_cost > 50 or maximum == 1:
        choice = 1
    else:
        quantity_question = "It costs {}g to make each {}, with your current supply of gold and time " \
                            "you can make up to {}. How many would you like to make?" \
            .format(item_craft_cost, item_name, maximum)
        choice = await self.answer_with_int_number(command, quantity_question, maximum)
    return choice


async def craft_mundane_confirm(self, command, discord_id, character_id, item_name, quantity: int):
    item_craft_cost = Scripts.mundane_craft_cost(item_name)
    total_cost = item_craft_cost * quantity
    character_name = Scripts.get_character_name(character_id)
    await command.author.send("Do you want to craft {} {} for {}g? [yes/no]"
                              .format(quantity, item_name, total_cost))
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("crafting..")
        log = "{} made {} {} for {}g".format(character_name, quantity, item_name, total_cost)
        await Scripts.mundane_create(self, discord_id, character_id, item_name, quantity, log)
        await command.author.send(log)
        return
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
##############Consumable#################
'''''''''''''''''''''''''''''''''''''''''


async def consumable_menu(self, command, discord_id, character_id: str):
    character_name = Scripts.get_character_name(character_id)
    # Profession
    profession = await profession_choice(self, command, character_id)
    if profession == "exit" or profession == "stop":
        return profession
    consumable_type = Scripts.consumable_type_name(profession)

    # has profession tools
    character_has_tools = Scripts.character_has_profession_tools(character_id, profession)
    if not character_has_tools[0]:
        await command.message.author.send(character_has_tools[1])
        return "stop"

    # get essence and recipe lists
    essence_inventory = Scripts.consumables_essences_in_inventory(character_id)
    recipe_list = Scripts.consumables_recipe_list(character_id, profession, essence_inventory)
    if len(recipe_list) == 0:
        await command.message.author.send("{} does not have the materials to craft any recipes that "
                                          "they know for making a {}".format(character_name, consumable_type))
        return "stop"

    # check player can afford to make consumable
    gold_limit = Scripts.crafting_limit(character_id)
    if profession.lower() == "cook":
        minimum_gold = 25
        message = "As a cook you can create a snack for 25g. Snacks can only have one effect"
    else:
        minimum_gold = 10
        message = "As a {} you can create a {} that have up to 5 effects, each effect costs 10g and two essences." \
            .format(profession, consumable_type)

    if gold_limit < minimum_gold:
        await command.message.author.send("{} does not have enough crafting funds to craft {}"
                                          .format(character_name, consumable_type))
        return "stop"

    # create loop to add each effect to consumable
    await command.message.author.send(message)
    effect_list = []
    while True:
        # stop when they run out of essences
        if len(recipe_list) == 0:
            await command.message.author.send("{} doesnt have enough essences to add another effect"
                                              .format(character_name))
            break
        # Stop if cook with one effect
        if profession == "cook" and len(effect_list) == 1:
            break
        # stop once you hit five effects
        if len(effect_list) == 5:
            await command.message.author.send("the {} have reached five effects".format(consumable_type))
            break
        # stop if they run out of money
        if (len(effect_list) + 1) * 10 > gold_limit:
            await command.message.author.send("{} cannot afford to add any more effects".format(character_name))
            break

        recipe = await consumable_effect(self, command, consumable_type, effect_list, recipe_list, essence_inventory)
        if recipe == "exit" or recipe == "stop":
            return recipe
        elif recipe == "craft":
            break
        else:
            # Update list of effects in the consumable, available essences to use and available recipes
            effect_list.append(recipe)
            essence_inventory = Scripts.consumable_update_essence_inventory(profession, recipe, essence_inventory)
            recipe_list = Scripts.consumables_recipe_list(character_id, profession, essence_inventory)
    # end crafting if no effects chosen
    if len(effect_list) == 0:
        await command.message.author.send("You cannot craft a {} without any effects".format(consumable_type))
        return

    confirm = await craft_consumable_confirm(self, command, discord_id, character_id, profession, effect_list)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return


async def consumable_effect(self, command, consumable_type, effect_list: list, recipe_list: list, inventory):
    option_question = Scripts.consumable_option_question(consumable_type, effect_list, inventory)
    choice = await self.answer_from_list_craft(command, option_question, recipe_list)
    choice_details = choice.split(" :")
    return choice_details[0]


async def craft_consumable_confirm(self, command, discord_id, character_id, profession, effect_list):
    character_name = Scripts.get_character_name(character_id)
    consumable_type = Scripts.consumable_type_name(profession)
    cleaned_effect_list = Scripts.consumable_merge_effects(effect_list)
    if profession == "cook":
        cost = 25
    else:
        cost = len(effect_list)*10
    await command.author.send("Do you want to craft a {} with: {} \nFor {}g? [yes/no]"
                              .format(consumable_type, cleaned_effect_list, cost))
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("crafting..")
        log = "{} made a {} of {} for {}g".format(character_name, consumable_type, cleaned_effect_list, cost)
        await Scripts.consumable_create(self, discord_id, character_id, profession, consumable_type,
                                        cleaned_effect_list, effect_list, cost, log)
        await command.author.send(log)
        return
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
##############Experiment#################
'''''''''''''''''''''''''''''''''''''''''


async def experiment_menu(self, command, discord_id, character_id: str):
    character_name = Scripts.get_character_name(character_id)
    gold_limit = Scripts.crafting_limit(character_id)
    if gold_limit == 0:
        await command.message.author.send("you cannot craft any more this week")
        return "stop"

    profession = await profession_choice(self, command, character_id)
    if profession == "exit" or profession == "stop":
        return profession

    character_has_tools = Scripts.character_has_profession_tools(character_id, profession)
    if not character_has_tools[0]:
        await command.message.author.send(character_has_tools[1])
        return "stop"

    total_character_essence = Scripts.experiment_essence_quantity(character_id)
    if total_character_essence < 2:
        await command.message.author.send("{} does not have enough essences to experiment with".format(character_name))
        return "stop"
    if gold_limit < 20:
        await command.message.author.send("{} does not have enough gold or time to experiment".format(character_name))
        return "stop"

    # get the first essence
    essence_list = Scripts.experiment_essence_list(character_id, profession)
    essence_1 = await experiment_first_essence(self, command, essence_list)
    if essence_1 == "exit" or essence_1 == "stop":
        return essence_1

    # get the second essence
    essence_list = Scripts.experiment_possible_essence_combination(character_id, profession, essence_1)
    essence_2 = await experiment_second_essence(self, command, essence_list)
    if essence_2 == "exit" or essence_2 == "stop":
        return essence_2
    confirm = await craft_experiment_confirm(self, command, discord_id, character_id, profession, essence_1, essence_2)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return


async def experiment_first_essence(self, command, option_list):
    option_question = "Please enter the number for the first essence you want to experiment with."
    choice = await self.answer_from_list(command, option_question, option_list)
    choice_details = choice.split(" (")
    return choice_details[0]


async def experiment_second_essence(self, command, essence_list):
    option_question = "Please enter the for the second essence to use."
    choice = await self.answer_from_list(command, option_question, essence_list)
    choice_details = choice.split(" (")
    return choice_details[0]


async def craft_experiment_confirm(self, command, discord_id, character_id, profession, essence_1, essence_2):
    character_name = Scripts.get_character_name(character_id)
    await command.author.send("Do you want to experiment using {} and {} as a {} for 20g? [yes/no]"
                              .format(essence_1, essence_2, profession))
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("crafting..")
        recipe_name = Scripts.experiment_name(profession, essence_1, essence_2)
        if recipe_name == "":
            recipe_name = Scripts.experiment_name(profession, essence_2, essence_1)

        log = "{} experimented with {} and {} as a {} and discovered {}"\
            .format(character_name, essence_1, essence_2, profession, recipe_name)
        await Scripts.experiment_create(self, discord_id, character_id, profession, recipe_name, essence_1, essence_2,
                                        log)
        await command.author.send(log)
        return "stop"
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
##############Recipe List################
'''''''''''''''''''''''''''''''''''''''''


async def recipe_menu(self, command, character_id: str):
    profession = await profession_choice(self, command, character_id)
    if profession == "exit" or profession == "stop":
        return profession

    response = Scripts.recipe_list(character_id, profession)
    await command.message.author.send(response)


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
    question = "Do you want work for {} this week?".format(target_name)
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
    question = "Do you want to create a scroll of {}?".format(spell_name.replace("''", "'"))
    log = "{} created a scroll of {}.".format(character_name, spell_name.replace("''", "'"))
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
    reagent_quantity = Scripts.reagent_quantity(character_id)
    ability_bonus = Scripts.scribe_roll_bonus(character_id)
    welcome_message = "Scribe spell Menu: Type **STOP** at any time to go back to the player menu. \n" \
                      "It costs 50 universal reagent per level of spell to scribe. you have {}.\n" \
                      "The DC to copy a spell is 10 + spell level. you have +{} to the roll"\
        .format(reagent_quantity, ability_bonus)
    await command.message.author.send(welcome_message)

    spell_choice = await scribe_spell_spell_choice(self, command, character_id, reagent_quantity)
    if spell_choice == "exit" or spell_choice == "stop":
        return spell_choice

    confirm = await scribe_spell_confirm(self, command, discord_id, character_id, spell_choice, ability_bonus)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return "stop"


async def scribe_spell_spell_choice(self, command, character_id, reagent_quantity):
    option_list = Scripts.scribe_spell_list(character_id, reagent_quantity)
    option_question = "Which spell would you like to lend?"
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def scribe_spell_confirm(self, command, discord_id, character_id, spell, ability_bonus):
    spell_detail = spell.split(":")
    spell_level = spell_detail[0].replace("Level ", "").replace(" Spell", "")
    spell_name = spell_detail[1].replace(" From", "").lstrip()
    spell_origin = spell_detail[2].lstrip()
    question = "Do you want to try and scribe {} into your spellbook from {}? " \
               "\nIt will cost {} universal reagent and you must pass a DC {} Arcane roll"\
        .format(spell_name.replace("''", "'"), spell_origin, int(spell_level)*50, int(spell_level)+10)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Attempting to scribe...")
        await Scripts.scribe_spell_confirm(self, command, discord_id, character_id, spell_name,
                                           spell_origin, spell_level, ability_bonus)
    return "exit"
