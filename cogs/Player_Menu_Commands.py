from discord.ext import commands
import asyncio

import Quick_SQL
from Player_Menu import SQL_Lookup
from Player_Menu import SQL_Check
from Player_Menu import Scripts


class Player_Menu_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Menu
    @commands.command(name='Menu', help="Opens the player menu")
    async def player_menu(self, command):
        discord_id = command.message.author.id
        # welcome message
        welcome = "Welcome to the Lost World player menu, to navigate around the menu " \
                  "type the option number into chat. Type **EXIT** at any time to close the menu"
        await command.message.author.send(welcome)
        # character choice
        character_name = await self.character_choice(command, discord_id)
        if character_name.lower() == "exit" or character_name.lower() == "back":
            await command.message.author.send("Menu closed")
            return
        while True:
            menu_option = await self.menu_choice(command, character_name)
            if menu_option == "Craft items":
                while True:
                    menu = await self.craft_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Give items to other characters":
                while True:
                    menu = await self.give_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Level up your character":
                while True:
                    menu = await self.level_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Pay a character":
                while True:
                    menu = await self.pay_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Pick your free crafting profession":
                while True:
                    menu = await self.profession_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Sell an item to town":
                while True:
                    menu = await self.sell_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Trade at the marketplace":
                while True:
                    menu = await self.trade_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            elif menu_option == "Work for a character":
                while True:
                    menu = await self.work_menu(command, discord_id, character_name)
                    if menu == "exit":
                        menu_option = "exit"
                        break
                    if menu == "stop":
                        break
            if menu_option == "exit":
                break
        await command.message.author.send("Menu closed")

    # Roll Stats
    @commands.command(name='randchar', help='Roll character stats')
    async def dice_roll(self, command):
        Quick_SQL.log_command(command)
        discord_id = str(command.message.author.id)
        discord_name = str(command.message.author.display_name)

        if not SQL_Check.player_exists(discord_id):
            sync = Scripts.sync_player(discord_id, discord_name)
            if not sync[0]:
                await command.send(sync)
        if SQL_Check.player_stat_roll(discord_id):
            results = SQL_Lookup.player_stat_roll(discord_id)
            previous_rolls = [results.Roll_1, results.Roll_2, results.Roll_3,
                              results.Roll_4, results.Roll_5, results.Roll_6]
            response = Scripts.stitch_list_into_string(previous_rolls)
            response = "You already have a stat array : {}".format(response)
        else:
            response = Scripts.rand_char(discord_id)
        await command.send(response)

    # Menu commands
    async def character_choice(self, command, discord_id):

        option_list = SQL_Lookup.player_character_list(discord_id)
        if len(option_list) == 0:
            await command.message.author.send("You dont have any characters yet.")
            choice = "stop"
        elif len(option_list) == 1:
            choice = option_list[0]
        else:
            option_question = "Which character would you like to view the menu for?"
            choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def menu_choice(self, command, character_name):
        option_list = Scripts.main_menu_options(character_name)
        if len(option_list) == 0:
            await command.message.author.send("{} doesnt have any options available".format(character_name))
            choice = "stop"
        else:
            option_question = "Main Menu: Welcome {}, What would you like to do? Type **EXIT** to close the menu."\
                .format(character_name)
            choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    # Crafting
    async def craft_menu(self, command, discord_id, character_name):
        while True:
            gold_limit = Scripts.crafting_gold_limit(character_name)
            if gold_limit == 0:
                await command.message.author.send("you cannot craft any more this week")
                return "stop"
            await command.message.author.send("Craft Menu: Type **STOP** at any time to go back to the player menu")
            profession = await self.craft_step_1_profession_choice(command, character_name)
            if profession == "exit" or profession == "stop":
                return profession
            character_has_tools = Scripts.character_has_profession_tools(character_name, profession)
            if not character_has_tools[0]:
                await command.message.author.send(character_has_tools[1])
                return
            while True:
                await command.message.author.send(Scripts.crafting_welcome_message(character_name))
                craft_type_choice = await self.craft_step_2_type_choice(command, profession)
                if craft_type_choice == "Mundane item":
                    # get the type of item they want to craft
                    item_type = await self.craft_mundane_step_1_type_choice(command, profession, gold_limit)
                    if item_type == "exit" or item_type == "stop":
                        return item_type
                    # get the name of the item
                    item_name = await self.craft_mundane_step_2_item_choice(command, profession, gold_limit, item_type)
                    if item_name == "exit" or item_name == "stop":
                        return item_name
                    # get the quantity
                    quantity = await self.craft_mundane_step_3_quantity(command, gold_limit, item_name)
                    if quantity == "exit" or quantity == "stop":
                        return quantity
                    # confirm crafting
                    confirm = await self.craft_mundane_step_4_confirm(command, discord_id, character_name,
                                                                      item_name, quantity)
                    if confirm == "exit" or confirm == "stop":
                        return confirm
                    # check if they want to craft something else
                    repeat = await self.craft_mundane_step_5_repeat(command)
                    if repeat == "exit" or repeat == "stop":
                        return repeat
                    return
                elif craft_type_choice == "Consumable from a recipe":
                    # Number of effects
                    type_name = SQL_Lookup.profession_consumable_name(profession)
                    inventory_essence_list = SQL_Lookup.character_inventory_essence(character_name)
                    recipe_list = Scripts.craft_recipe_list(character_name, profession, inventory_essence_list)
                    effect_list = []

                    if profession.lower() == "cook":
                        minimum_gold = 25
                        message = "As a cook you can snack for 25g. These snacks will only have one effect"
                    else:
                        minimum_gold = 10
                        message = "as a {} you can create {} that have up to 5 effects, each effect costs 10g and " \
                                  "needs two essences to add.".format(profession, type_name)
                    if len(recipe_list) == 0:
                        await command.message.author.send("{} does not have the materials to craft any recipes that "
                                                          "they know for making a {}".format(character_name, type_name))
                        return "stop"
                    if gold_limit < minimum_gold:
                        await command.message.author.send("{} does not have enough gold or time to craft {}"
                                                          .format(character_name, type_name))
                        return "stop"

                    await command.message.author.send(message)

                    while True:
                        if len(recipe_list) == 0:
                            await command.message.author.send("{} doesnt have enough essences to add another effect"
                                                              .format(character_name))
                        if profession == "cook" and len(effect_list) == 1:
                            break
                        if len(effect_list) == 5:
                            await command.message.author.send("the {} have reached five effects".format(type_name))
                            break
                        if (len(effect_list) + 1) * 10 > gold_limit:
                            await command.message.author.send("{} cannot afford to add any more effects"
                                                              .format(character_name))
                            break
                        recipe = await self.craft_consumable_step_1_effects(command, type_name, effect_list,
                                                                            recipe_list, Scripts.stitch_list_into_string
                                                                            (inventory_essence_list))
                        if recipe == "exit" or recipe == "stop":
                            return recipe
                        if recipe == "craft":
                            break
                        else:
                            effect_list.append(recipe)
                            recipe_essence = SQL_Lookup.recipe_essence_list(profession, recipe)
                            inventory_essence_list = Scripts.craft_remove_essence_from_list(inventory_essence_list,
                                                                                            recipe_essence[0])
                            inventory_essence_list = Scripts.craft_remove_essence_from_list(inventory_essence_list,
                                                                                            recipe_essence[1])
                            recipe_list = Scripts.craft_recipe_list(character_name, profession, inventory_essence_list)
                    if len(effect_list) == 0:
                        await command.message.author.send("You cannot craft a {} without any effects".format(type_name))
                        break
                    craft = await self.craft_consumable_step_2_confirm(command, discord_id, character_name, profession,
                                                                       type_name, effect_list)
                    if craft == "exit" or craft == "stop":
                        break
                elif craft_type_choice == "Experiment with ingredients":
                    total_character_essence = SQL_Lookup.character_inventory_essence_count(character_name)
                    if total_character_essence < 2:
                        await command.message.author.send("{} does not have enough essences to experiment with"
                                                          .format(character_name))
                        return
                    if gold_limit < 20:
                        await command.message.author.send("{} does not have enough gold or time to experiment"
                                                          .format(character_name))
                        return
                    # get the first essence
                    essence_list = Scripts.craft_essence_list(character_name, profession)
                    essence_1 = await self.craft_experiment_step_1_first_essence(command, essence_list)
                    if essence_1 == "exit" or essence_1 == "stop":
                        return essence_1
                    # get the second essence
                    essence_list = Scripts.craft_possible_essence_combination_list(character_name, profession,
                                                                                   essence_1)
                    essence_2 = await self.craft_experiment_step_2_second_essence(command, essence_list)
                    if essence_2 == "exit" or essence_2 == "stop":
                        return essence_2
                    confirm = await self.craft_experiment_step_3_confirm(command, discord_id, character_name,
                                                                         profession, essence_1, essence_2,)
                    if confirm == "exit" or confirm == "stop":
                        return confirm
                    return
                elif craft_type_choice == "Look at recipe book":
                    recipe_list = SQL_Lookup.character_known_recipe_details(character_name, profession)
                    if len(recipe_list) == 0:
                        await command.message.author.send("{} doesnt know any recipes for {} yet"
                                                          .format(character_name, profession))
                    else:
                        recipe_list.insert(0, "{} knows the following {} recipes:".format(character_name, profession))
                        await command.message.author.send(Scripts.stitch_list_into_table(recipe_list))
                elif craft_type_choice == "exit" or craft_type_choice == "stop":
                        return craft_type_choice

    async def craft_step_1_profession_choice(self, command, character_name):
        # collect information about how much crafting can be done
        option_list = SQL_Lookup.character_profession_list(character_name)
        option_question = "Please enter the number of the profession to use."
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def craft_step_2_type_choice(self, command, skill):
        # find crafting types, choose if more than one
        option_list = SQL_Lookup.profession_craft_options(skill)
        option_question = "What sort of work do you want to do as a {}?".format(skill)
        if len(option_list) == 1:
            choice = option_list[0]
        else:
            choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def craft_mundane_step_1_type_choice(self, command, profession, gold_limit):
        option_list = SQL_Lookup.profession_item_type_list(profession, gold_limit)
        if len(option_list) == 0:
            await command.message.author.send("No options available")
            return "stop"
        option_question = "What type of item do you want to craft?".format(profession)
        if len(option_list) == 1:
            choice = option_list[0]
        else:
            choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def craft_mundane_step_2_item_choice(self, command, profession, gold_limit, item_type):
        option_list = SQL_Lookup.profession_item_list(profession, item_type, gold_limit)
        if len(option_list) == 0:
            await command.message.author.send("No options available")
            return "stop"
        option_question = "What item do you want to craft?"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def craft_mundane_step_3_quantity(self, command, gold_limit, item_name):
        item_craft_cost = SQL_Lookup.item_value(item_name)/2
        maximum = int(gold_limit / item_craft_cost)
        if item_craft_cost > 50 or maximum == 1:
            choice = 1
        else:
            quantity_question = "It costs {}g to make each {}, with your current supply of gold and time " \
                                "you can make up to {}. How many would you like to make?" \
                .format(item_craft_cost, item_name, maximum)
            choice = await self.answer_with_int_number(command, quantity_question, maximum)
        return choice

    async def craft_mundane_step_4_confirm(self, command, discord_id, character_name, item_name, quantity: int):
        item_craft_cost = SQL_Lookup.item_value(item_name) / 2
        total_cost = item_craft_cost * quantity
        await command.author.send("Do you want to craft {} {} for {}g? [yes/no]"
                                  .format(quantity, item_name, total_cost))
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("crafting..")
            log = "{} made {} {} for {}g".format(character_name, quantity, item_name, total_cost)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.craft_create_mundane_item(character_name, item_name, quantity)
            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
            return
        return "stop"

    async def craft_mundane_step_5_repeat(self, command):
        await command.author.send("Do you want to continue crafting? [yes/no]")
        choice = await self.confirm(command)
        if choice == "No":
            choice = "stop"
        return choice

    async def craft_consumable_step_1_effects(self, command, type_name, effect_list: list, recipe_list: list,
                                              inventory):
        cost = len(effect_list) * 10
        if len(effect_list) == 0:
            short_effect_list = "None"
            craft_message = "."
        else:
            short_effect_list = Scripts.stitch_list_into_string(Scripts.craft_merge_effects(effect_list))
            craft_message = " or type **Craft** to create the {}.".format(type_name)
        option_question = "Current effects : {}, at a cost of Cost : {}g. \n" \
                          "Essence available : {} \n" \
                          "Please enter the number for the effect you want{}"\
            .format(short_effect_list, cost, inventory, craft_message)
        choice = await self.answer_from_list_craft(command, option_question, recipe_list)
        choice_details = choice.split(" :")
        return choice_details[0]

    async def craft_consumable_step_2_confirm(self, command, discord_id, character_name, profession,
                                              type_name, effect_list):
        cleaned_effect_list = Scripts.stitch_list_into_string(Scripts.craft_merge_effects(effect_list))
        if profession == "cook":
            cost = 25
        else:
            cost = len(effect_list)*10
        await command.author.send("Do you want to craft a {} with: \n{} \nFor {}g? [yes/no]"
                                  .format(type_name, cleaned_effect_list, cost))
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("crafting..")
            log = "{} made a {} of {} for {}g".format(character_name, type_name,
                                                      cleaned_effect_list, cost)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.craft_create_consumable(character_name, type_name, profession,
                                            cleaned_effect_list, effect_list, cost)
            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
            return
        return "stop"

    async def craft_experiment_step_1_first_essence(self, command, option_list):
        option_question = "Please enter the number for the first essence you want to experiment with."
        choice = await self.answer_from_list(command, option_question, option_list)
        choice_details = choice.split(" (")
        return choice_details[0]

    async def craft_experiment_step_2_second_essence(self, command, essence_list):
        option_question = "Please enter the for the second essence to use."
        choice = await self.answer_from_list(command, option_question, essence_list)
        choice_details = choice.split(" (")
        return choice_details[0]

    async def craft_experiment_step_3_confirm(self, command, discord_id, character_name,
                                              profession, essence_1, essence_2):
        await command.author.send("Do you want to experiment using "
                                  "{} and {} as a {} for 20g? [yes/no]".format(essence_1, essence_2, profession))
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("crafting..")
            recipe_name = SQL_Lookup.recipe_by_essence(profession, essence_1, essence_2)
            if recipe_name == "":
                recipe_name = SQL_Lookup.recipe_by_essence(profession, essence_2, essence_1)

            log = "{} experimented with {} and {} as a {} and discovered {}".format(character_name, essence_1,
                                                                                    essence_2, profession, recipe_name)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.craft_create_experiment(character_name, profession, recipe_name, essence_1, essence_2)
            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
            return
        return "stop"

    async def give_menu(self, command, discord_id, character_name):
        welcome_message = "Gift Menu: Type **STOP** at any time to go back to the player menu."
        await command.message.author.send(welcome_message)
        while True:
            # get character item is being sent to
            target_name = await self.give_step_1_character_choice(command, character_name)
            if target_name == "exit" or target_name == "stop":
                return target_name

            # get the item they want to send
            item_name = await self.give_step_2_item_choice(command, character_name, target_name)
            if item_name == "exit" or item_name == "stop":
                return item_name

            # get the quantity
            quantity = await self.give_step_3_quantity_choice(command, character_name, item_name, target_name)
            if quantity == "exit" or quantity == "stop":
                return quantity

            # confirm the gift
            confirm = await self.give_step_4_confirm(command, discord_id, character_name,
                                                     item_name, quantity, target_name)
            if confirm == "exit" or confirm == "stop":
                return confirm
            return

    async def give_step_1_character_choice(self, command, character_name):
        choice_question = "Type the name of the character you want to give items to"
        choice = await self.character_name_lookup(command, choice_question, character_name)
        return choice

    async def give_step_2_item_choice(self, command, character_name, target):
        option_list = SQL_Lookup.character_inventory(character_name)
        option_question = "Please choose which item you want to give to {}".format(target)
        choice = await self.answer_from_list(command, option_question, option_list)
        choice_details = choice.split(" (")
        item_name = choice_details[0]
        return item_name

    async def give_step_3_quantity_choice(self, command, character_name, item_name, target_name):
        maximum = SQL_Lookup.character_item_quantity(character_name, item_name)
        if maximum == 1:
            choice = 1
        else:
            choice_question = "you own {} {}, how many do you want to give to {}?" .format(maximum, item_name,
                                                                                           target_name)
            choice = await self.answer_with_int_number(command, choice_question, maximum)
        return choice

    async def give_step_4_confirm(self, command, discord_id, character_name, item_name, quantity: int, target_name):
        question = "Do you want to give {} {} {} from {} inventory?".format(target_name, quantity,
                                                                            item_name, character_name)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Giving...")
            log = "{} gave {} {} {}".format(character_name, target_name, quantity, item_name)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.give_item(character_name, target_name, item_name, quantity)
            target_discord = self.bot.get_user(SQL_Lookup.character_owner(target_name))
            await Scripts.log_to_discord(self, log)
            await target_discord.send(log)
            await command.author.send(log)
        return "stop"

    # Leveling up

    async def level_menu(self, command, discord_id, character_name):
        character_levels = Scripts.stitch_list_into_string(SQL_Lookup.character_class_and_levels(character_name))
        welcome_message = "Level Menu: Type **STOP** at any time to go back to the player menu " \
                          "\n{} is currently a {}.".format(character_name, character_levels)
        await command.message.author.send(welcome_message)
        while True:
            class_choice = await self.level_step_1_class_choice(command, character_name)
            if class_choice == "exit" or class_choice == "stop":
                return class_choice
            confirm = await self.level_step_2_confirm(command, discord_id, character_name, class_choice)
            if confirm == "exit" or confirm == "stop":
                return confirm
            return

    async def level_step_1_class_choice(self, command, character_name):
        class_number = SQL_Lookup.character_count_classes(character_name)
        if class_number > 2:
            option_list = SQL_Lookup.character_class_list(character_name)
        else:
            option_list = SQL_Lookup.info_classes()
        option_question = "Which class would you like to gain a level in?"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def level_step_2_confirm(self, command, discord_id, character_name, class_choice):
        question = "Do you want {} to gain a level in {}?".format(character_name, class_choice)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("leveling...")
            log = "{} gained a level in {}".format(character_name, class_choice)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.level_up(character_name, class_choice)
            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
        return "stop"

    # Pay Character

    async def pay_menu(self, command, discord_id, character_name):
        welcome_message = "Pay Menu: Type **STOP** at any time to go back to the player menu. \n" \
                          "You can pay other players directly for goods and services."
        await command.message.author.send(welcome_message)
        while True:
            # get character item is being sent to
            target_name = await self.pay_step_1_character_choice(command, character_name)
            if target_name == "exit" or target_name == "stop":
                return target_name
            # get quantity
            quantity = await self.pay_step_2_quantity(command, character_name, target_name)
            if quantity == "exit" or quantity == "stop":
                return quantity
            reason = await self.pay_step_3_reason(command, target_name)
            if reason == "exit" or reason == "stop":
                return reason
            # confirm the transaction
            confirm = await self.pay_step_4_confirm(command, discord_id, character_name, quantity, target_name, reason)
            if confirm == "exit" or confirm == "stop":
                return confirm
            return

    async def pay_step_1_character_choice(self, command, character_name):
        choice_question = "Type the name of the character you want to pay."
        choice = await self.character_name_lookup(command, choice_question, character_name)
        return choice

    async def pay_step_2_quantity(self, command, character_name, target_name):
        maximum = SQL_Lookup.character_gold_total(character_name)
        if maximum == 1:
            choice = 1
        else:
            choice_question = "you have {}g, how much do you want to give {}?" .format(maximum, target_name)
            choice = await self.answer_with_float_number(command, choice_question, maximum)
        return choice

    async def pay_step_3_reason(self, command, target_name):
        question = "Why are you paying {}?" .format(target_name)
        await command.author.send(question)
        choice = await self.answer_with_statement(command)
        return choice

    async def pay_step_4_confirm(self, command, discord_id, character_name, quantity: float, target_name, reason):
        question = "Do you want to give {} {}g because: {}?".format(target_name, quantity, reason)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Paying...")
            log = "{} gave {} {}g because: {}".format(character_name, target_name, quantity, reason)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.give_gold(character_name, target_name, quantity)
            target_discord = self.bot.get_user(SQL_Lookup.character_owner(target_name))
            await Scripts.log_to_discord(self, log)
            await target_discord.send(log)
            await command.author.send(log)
        return "stop"

    # Pick free profession

    async def profession_menu(self, command, discord_id, character_name):
        character_levels = Scripts.stitch_list_into_string(SQL_Lookup.character_class_and_levels(character_name))
        welcome_message = "Profession Menu: Type **STOP** at any time to go back to the player menu " \
                          "\nPick your free crafting profession.".format(character_name, character_levels)
        await command.message.author.send(welcome_message)
        while True:
            profession_choice = await self.profession_step_1_profession_choice(command)
            if profession_choice == "exit" or profession_choice == "stop":
                return profession_choice
            confirm = await self.profession_step_2_confirm(command, discord_id, character_name, profession_choice)
            if confirm == "exit" or confirm == "stop":
                return confirm
            return

    async def profession_step_1_profession_choice(self, command):
        option_list = SQL_Lookup.info_skills()
        option_question = "Which profession would you like to gain have?"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def profession_step_2_confirm(self, command, discord_id, character_name, profession_name):
        question = "Do you want {} to gain {} as a profession?".format(character_name, profession_name)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("adding profession...")
            log = "{} gained {} as their free profession".format(character_name, profession_name)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.give_profession(character_name, profession_name)
            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
        return "stop"

    # Sell Item to town
    async def sell_menu(self, command, discord_id, character_name):
        welcome_message = "Sell Menu: Type **STOP** at any time to go back to the player menu.\n" \
                          "You can sell mundane items to the town at their crafting value."
        await command.message.author.send(welcome_message)
        while True:
            # get the item they want to sell
            item_name = await self.sell_step_1_item_choice(command, character_name)
            if item_name == "exit" or item_name == "stop":
                return item_name

            # get the quantity
            quantity = await self.sell_step_2_quantity_choice(command, character_name, item_name)
            if quantity == "exit" or quantity == "stop":
                return quantity

            # confirm sale
            confirm = await self.sell_step_3_confirm(command, discord_id, character_name, item_name, quantity)
            if confirm == "exit" or confirm == "stop":
                return confirm
            return

    async def sell_step_1_item_choice(self, command, character_name,):
        option_list = SQL_Lookup.character_sellable_inventory_list(character_name)
        option_question = "Please choose which item you want to sell?"
        choice = await self.answer_from_list(command, option_question, option_list)
        choice_details = choice.split(" (")
        item_name = choice_details[0]
        return item_name

    async def sell_step_2_quantity_choice(self, command, character_name, item_name):
        maximum = SQL_Lookup.character_item_quantity(character_name, item_name)
        item_value = SQL_Lookup.item_value(item_name)
        if maximum == 1:
            choice = 1
        else:
            choice_question = "{} sell for {} each, you own {}, how many do you want to sell?"\
                .format(item_name, item_value, maximum, item_name)
            choice = await self.answer_with_int_number(command, choice_question, maximum)
        return choice

    async def sell_step_3_confirm(self, command, discord_id, character_name, item_name, quantity: int):
        item_value = SQL_Lookup.item_value(item_name)
        total_value = item_value/2 * quantity
        question = "Do you want to sell {} {} for {}g each for a total of {}g?"\
            .format(quantity, item_name, item_value, total_value)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Selling...")
            log = "{} sold {} {} for {}g".format(character_name, quantity, item_name, total_value)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.sell_item_to_town(character_name, item_name, quantity)
            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
        return "stop"

    # Trade item in market
    async def trade_menu(self, command, discord_id, character_name):
        while True:
            welcome_message = "Trade Menu: Type **STOP** at any time to go back to the player menu \n" \
                              "You can buy and sell anything in your inventory to other members of town"
            await command.message.author.send(welcome_message)
            trade_type = await self.trade_step_1_choice(command, character_name)
            if trade_type == "exit" or trade_type == "stop":
                return trade_type
            elif trade_type == "Buy":
                gold_limit = SQL_Lookup.character_gold_total(character_name)
                if not SQL_Check.character_has_enough_gold_to_buy_trade(gold_limit):
                    await command.message.author.send("There is nothing on the market you can afford")
                    return "stop"
                # what item type are they looking for?
                item_type = await self.trade_buy_step_1_item_type_choice(command, gold_limit, character_name)
                if item_type == "exit" or item_type == "stop":
                    return item_type
                # what item do they want?
                item_name = await self.trade_buy_step_2_item_choice(command, gold_limit, item_type, character_name)
                if item_name == "exit" or item_name == "stop":
                    return item_name
                # how many do they want to buy?
                quantity = await self.trade_buy_step_3_quantity(command, character_name, item_name)
                if quantity == "exit" or quantity == "stop":
                    return quantity
                confirm = await self.trade_buy_step_4_confirm(command, discord_id, character_name, item_name, quantity)
                if confirm == "exit" or confirm == "stop":
                    return confirm
            elif trade_type == "Sell":
                item_name = await self.trade_sell_step_1_item(command, character_name)
                if item_name == "exit" or item_name == "stop":
                    return item_name
                quantity = await self.trade_sell_step_2_quantity(command, character_name, item_name)
                if quantity == "exit" or quantity == "stop":
                    return quantity
                price = await self.trade_sell_step_3_price(command, item_name)
                if price == "exit" or price == "stop":
                    return price
                confirm = await self.trade_sell_step_4_confirm(command, discord_id, character_name,
                                                               item_name, quantity, price)
                if confirm == "exit" or confirm == "stop":
                    return confirm
                return
            elif trade_type == "Stop trading":
                item_name = await self.trade_stop_step_1_item(command, character_name)
                if item_name == "exit" or item_name == "stop":
                    return item_name
                confirm = await self.trade_stop_step_2_confirm(command, discord_id, character_name, item_name)
                if confirm == "exit" or confirm == "stop":
                    return confirm
                return

    async def trade_step_1_choice(self, command, character_name):
        # collect information about how much crafting can be done
        option_list = Scripts.character_trade_options(character_name)
        option_question = "what would you like to do?"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def trade_buy_step_1_item_type_choice(self, command, gold, character_name):
        option_list = SQL_Lookup.trade_goods_types(character_name, gold)
        option_question = "What type of item are you trying to buy?"
        choice = await self.answer_from_list(command, option_question, option_list)
        return choice

    async def trade_buy_step_2_item_choice(self, command, gold, item_type, character_name):
        option_list = SQL_Lookup.trade_goods_items_by_type(character_name, gold, item_type)
        option_question = "which item are you trying to buy?"
        choice = await self.answer_from_list(command, option_question, option_list)
        choice_details = choice.split(":")
        return choice_details[0]

    async def trade_buy_step_3_quantity(self, command, character_name, item_name):
        character_gold = SQL_Lookup.character_gold_total(character_name)
        trade_good = SQL_Lookup.trade_item_cheapest_on_sale(item_name)
        if trade_good.Price == 0:
            maximum = trade_good.Quantity
        else:
            maximum = min([trade_good.Quantity, int(character_gold/trade_good.Price)])
        if maximum == 1:
            choice = 1
        else:
            choice_question = "There are {} {} for sale, they cost {}g each and you have {}g. " \
                              "How many would you like to buy?"\
                .format(trade_good.Quantity, trade_good.Item, trade_good.Price, character_gold)
            choice = await self.answer_with_int_number(command, choice_question, maximum)
        return choice

    async def trade_buy_step_4_confirm(self, command, discord_id, character_name, item_name, quantity: int):
        trade_good = SQL_Lookup.trade_item_cheapest_on_sale(item_name)
        total_value = trade_good.Price * quantity
        question = "Do you want to buy {} {} for {}g each for a total of {}g?" \
            .format(quantity, item_name, trade_good.Price, total_value)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Buying item...")
            log = "{} Bought {} {} for {}g".format(character_name, quantity, trade_good.Item, total_value)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.trade_buy(character_name, trade_good, quantity)

            target_discord = self.bot.get_user(SQL_Lookup.character_owner(trade_good.Character))
            await Scripts.log_to_discord(self, log)
            await target_discord.send(log)
            await command.author.send(log)
        return "stop"

    async def trade_sell_step_1_item(self, command, character_name):
        option_list = SQL_Lookup.character_inventory(character_name)
        option_question = "What would you like to sell in the market?"
        choice_details = await self.answer_from_list(command, option_question, option_list)
        choice = choice_details.split(" (")
        return choice[0]

    async def trade_sell_step_2_quantity(self, command, character_name, item_name):
        maximum = SQL_Lookup.character_item_quantity(character_name, item_name)
        if maximum == 1:
            choice = 1
        else:
            choice_question = "You own {} {}, how many would you like to put up for sale?".format(maximum, item_name)
            choice = await self.answer_with_int_number(command, choice_question, maximum)
        return choice

    async def trade_sell_step_3_price(self, command, item_name):
        choice_question = "how much do you want to sell each {} for?".format(item_name)
        choice = await self.answer_with_float_number(command, choice_question, 100000000000)
        return choice

    async def trade_sell_step_4_confirm(self, command, discord_id, character_name,
                                        item_name, quantity: int, price: float):
        total_value = price * quantity
        question = "Do you want to put {} {} up for trade at {}g each for a total of {}g?" \
            .format(quantity, item_name, price, total_value)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("putting up for trade...")
            log = "{} put {} {} up for trade at {}g each".format(character_name, quantity, item_name, price)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.trade_sell(character_name, item_name, quantity, price)

            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
        return "stop"

    async def trade_stop_step_1_item(self, command, character_name):
        option_list = SQL_Lookup.character_items_for_trade(character_name)
        option_question = "What would you like to stop selling?"
        choice_details = await self.answer_from_list(command, option_question, option_list)
        choice = choice_details.split(" - ")
        return choice[0]

    async def trade_stop_step_2_confirm(self, command, discord_id, character_name, item_name):
        question = "Do you want stop selling {}?".format(item_name)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("Stopping sale...")
            log = "{} stopped selling {}".format(character_name, item_name)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.trade_stop(character_name, item_name)

            await Scripts.log_to_discord(self, log)
            await command.author.send(log)
        return "stop"

    #  Work Menu
    async def work_menu(self, command, discord_id, character_name):
        welcome_message = "Work Menu: Type **STOP** at any time to go back to the player menu.\n" \
                          "You can give up crafting for the week to work for another character."
        await command.message.author.send(welcome_message)
        while True:
            # get target name
            target_name = await self.work_step_1_character_choice(command, character_name)
            if target_name == "exit" or target_name == "stop":
                return target_name
            if not SQL_Check.character_has_crafted_this_week(target_name):
                await command.message.author.send("{} has already started working this "
                                                  "week and cannot hire help".format(target_name))
                return "stop"
            # confirm the transaction
            confirm = await self.work_step_2_confirm(command, discord_id, character_name, target_name)
            if confirm == "exit" or confirm == "stop":
                return confirm
            return

    async def work_step_1_character_choice(self, command, character_name):
        choice_question = "Type the name of the character you want to pay"
        choice = await self.character_name_lookup(command, choice_question, character_name)
        return choice

    async def work_step_2_confirm(self, command, discord_id, character_name, target_name):
        question = "Do you want work for {} this week?".format(target_name)
        await command.author.send(question)
        reply = await self.confirm(command)
        if reply == "Yes":
            await command.author.send("working...")
            log = "{} is now working for {} this week".format(character_name, target_name)
            Quick_SQL.log_private_command(discord_id, log)
            Scripts.work(character_name, target_name)

            target_discord = self.bot.get_user(SQL_Lookup.character_owner(target_name))
            await Scripts.log_to_discord(self, log)
            await target_discord.send(log)
            await command.author.send(log)
        return "stop"

    # Answers methods
    async def answer_from_list(self, command, question, option_list):
        options = Scripts.question_list(option_list)
        maximum = len(option_list)
        await command.message.author.send("{}\n{}".format(question, options))

        # setup sub function to do checks the returned message is from the user in private messages

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return "exit"
            if msg.content.lower() == "exit":
                return "exit"
            if msg.content.lower() == "stop":
                return "stop"

            # check they picked an answer

            try:
                answer = int(msg.content)
                if answer < 1:
                    await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
                else:
                    option = option_list[answer - 1]
                    return option
            except IndexError:
                await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, please enter a number".format(msg.content))

    async def answer_from_list_craft(self, command, question, option_list):
        options = Scripts.question_list(option_list)
        maximum = len(option_list)
        await command.message.author.send("{}\n{}".format(question, options))

        # setup sub function to do checks the returned message is from the user in private messages

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return "exit"
            if msg.content.lower() == "exit":
                return "exit"
            if msg.content.lower() == "craft":
                return "craft"
            if msg.content.lower() == "stop":
                return "stop"

            # check they picked an answer

            try:
                answer = int(msg.content)
                if answer < 1:
                    await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
                else:
                    option = option_list[answer - 1]
                    return option
            except IndexError:
                await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, please enter a number".format(msg.content))

    async def answer_with_int_number(self, command, question, maximum):
        await command.message.author.send("{}".format(question))

        # setup sub function to do checks the returned message is from the user in private messages

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return "exit"
            if msg.content.lower() == "exit":
                return "exit"
            if msg.content.lower() == "stop":
                return "stop"
            # check they picked an answer
            try:
                answer = int(msg.content)
                if answer < 1:
                    await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
                elif answer <= maximum:
                    return answer
                else:
                    await command.message.author.send("Please enter a number between 1 and {}".format(maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, Please enter a number between 1 and {}"
                                                  .format(msg.content, maximum))

    async def answer_with_float_number(self, command, question, maximum):
        await command.message.author.send("{}".format(question))

        # setup sub function to do checks the returned message is from the user in private messages

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return "exit"
            if msg.content.lower() == "exit":
                return "exit"
            if msg.content.lower() == "stop":
                return "stop"
            # check they picked an answer
            try:
                answer = float(msg.content)
                if answer < 0:
                    await command.message.author.send("Please enter a number greater than 0".format(maximum))
                elif answer <= maximum:
                    return answer
                else:
                    await command.message.author.send("Please enter a number greater than 0".format(maximum))
            except ValueError:
                await command.message.author.send("{} is not a number, Please enter a number greater than 0"
                                                  .format(msg.content))

    async def answer_with_statement(self, command):
        # check author
        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        # send the user the message
        try:
            msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
        except asyncio.TimeoutError:
            return "exit"
        # check the response
        if msg.content.lower() == "exit":
            reply = "exit"
        elif msg.content.lower() == "stop":
            reply = "stop"
        else:
            reply = msg.content.lower()
        return reply

    async def confirm(self, command):
        # check author
        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        # send the user the message
        try:
            msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
        except asyncio.TimeoutError:
            return "exit"
        # check the response
        if msg.content.lower() == "exit":
            reply = "exit"
        elif msg.content.lower() == "stop":
            reply = "stop"
        elif msg.content.lower() == "yes":
            reply = "Yes"
        else:
            reply = "No"
        return reply

    async def character_name_lookup(self, command, question, character_name):
        await command.message.author.send(question)

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        while True:
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return "exit"
            if msg.content.lower() == "exit":
                return "exit"
            elif msg.content.lower() == "stop":
                return "stop"
            elif msg.content.lower() == character_name.lower():
                await command.message.author.send("You cannot give yourself an item")
            elif SQL_Check.character_exists(msg.content.lower()):
                return msg.content.lower()
            else:
                await command.message.author.send("{} is not a character, please "
                                                  "confirm the spelling and try again".format(msg.content.lower()))


def setup(bot):
    bot.add_cog(Player_Menu_Commands(bot))

