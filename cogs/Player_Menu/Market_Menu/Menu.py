from Player_Menu.Market_Menu import Scripts


async def main_menu(self, command, discord_id: int, character_id: str):
    while True:
        choice = await menu_options(self, command, character_id)
        if choice == "Buy items":
            while True:
                menu = await buy_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                if menu == "stop":
                    return
        elif choice == "Sell items":
            while True:
                menu = await sell_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                if menu == "stop":
                    return
        elif choice == "Stop selling an item":
            while True:
                menu = await stop_sell_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                if menu == "stop":
                    return
        elif choice == "Give an item to someone":
            while True:
                menu = await give_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                if menu == "stop":
                    return
        elif choice == "Give gold to someone":
            while True:
                menu = await pay_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                if menu == "stop":
                    return
        elif choice == "Recycle an item":
            while True:
                menu = await recycle_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                if menu == "stop":
                    return
        elif choice == "Share a spell from your spell book with someone":
            while True:
                menu = await share_spell_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                if menu == "stop":
                    return
        elif choice == "exit" or choice == "stop":
            return choice


async def menu_options(self, command, character_id):
    option_list = Scripts.menu(character_id)
    details = Scripts.character_info(character_id)
    option_question = "Character Sheet Menu: " \
                      "Type **STOP** at any time to go back to the player menu \n" \
                      "{} \n" \
                      "What would you like to do?".format(details)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


'''''''''''''''''''''''''''''''''''''''''
################Buying##################
'''''''''''''''''''''''''''''''''''''''''


async def buy_menu(self, command, discord_id, character_id: str):
    gold_limit = Scripts.buy_character_gold(character_id)
    if not Scripts.buy_can_afford_to_buy(gold_limit):
        await command.message.author.send("There is nothing on the market you can afford")
        return "stop"
    # what item type are they looking for?
    item_type = await buy_item_type_choice(self, command, gold_limit, character_id)
    if item_type == "exit" or item_type == "stop":
        return item_type
    # what item do they want?
    item_name = await buy_item_choice(self, command, gold_limit, item_type, character_id)
    if item_name == "exit" or item_name == "stop":
        return item_name
    # how many do they want to buy?
    quantity = await buy_quantity(self, command, character_id, item_name)
    if quantity == "exit" or quantity == "stop":
        return quantity
    confirm = await buy_confirm(self, command, discord_id, character_id, item_name, quantity)
    if confirm == "exit" or confirm == "stop":
        return confirm


async def buy_item_type_choice(self, command, gold, character_id):
    option_list = Scripts.buy_item_types(character_id, gold)
    option_question = "What type of item are you trying to buy?"
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def buy_item_choice(self, command, gold, item_type, character_id):
    option_list = Scripts.buy_item_list(character_id, gold, item_type)
    option_question = "which item are you trying to buy?"
    choice = await self.answer_from_list(command, option_question, option_list)
    choice_details = choice.split(":")
    return choice_details[0]


async def buy_quantity(self, command, character_id, item_name):
    character_gold = Scripts.buy_character_gold(character_id)
    trade_good = Scripts.buy_cheapest_item(item_name)
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


async def buy_confirm(self, command, discord_id, character_id, item_name, quantity: int):
    trade_good = Scripts.buy_cheapest_item(item_name)
    total_value = trade_good.Price * quantity
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want to buy {} {} for {}g each for a total of {}g? [Yes/No]" \
        .format(quantity, item_name, trade_good.Price, total_value)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Buying item...")
        log = "{} Bought {} {} for {}g".format(character_name, quantity, trade_good.Item, total_value)
        await Scripts.buy_confirm(self, discord_id, character_id, trade_good, quantity, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
################Selling##################
'''''''''''''''''''''''''''''''''''''''''


async def sell_menu(self, command, discord_id, character_id: str):
    item_name = await sell_item(self, command, character_id)
    if item_name == "exit" or item_name == "stop":
        return item_name
    quantity = await sell_quantity(self, command, character_id, item_name)
    if quantity == "exit" or quantity == "stop":
        return quantity
    price = await sell_price(self, command, item_name)
    if price == "exit" or price == "stop":
        return price
    confirm = await sell_confirm(self, command, discord_id, character_id, item_name, quantity, price)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return


async def sell_item(self, command, character_id):
    option_list = Scripts.sell_inventory(character_id)
    option_question = "What would you like to sell in the market?"
    choice_details = await self.answer_from_list(command, option_question, option_list)
    choice = choice_details.split(" (")
    return choice[0]


async def sell_quantity(self, command, character_id, item_name):
    item_details = Scripts.sell_character_item(character_id, item_name)
    maximum = item_details.Quantity
    if maximum == 1:
        choice = 1
    else:
        choice_question = "You own {} {}, how many would you like to put up for sale?".format(maximum, item_name)
        choice = await self.answer_with_int_number(command, choice_question, maximum)
    return choice


async def sell_price(self, command, item_name):
    choice_question = "How much do you want to sell each {} for? [Amount in gold]".format(item_name)
    choice = await self.answer_with_float_number(command, choice_question, 100000000000)
    return choice


async def sell_confirm(self, command, discord_id, character_id, item_name, quantity: int, price: float):
    total_value = price * quantity
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want to put {} {} up for trade at {}g each for a total of {}g? [Yes/No]" \
        .format(quantity, item_name, price, total_value)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("putting up for trade...")
        log = "{} put {} {} up for trade at {}g each".format(character_name, quantity, item_name, price)
        await Scripts.sell_confirm(self, discord_id, character_id, item_name, quantity, price, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
################Stop Sale################
'''''''''''''''''''''''''''''''''''''''''


async def stop_sell_menu(self, command, discord_id, character_id: str):
    item_name = await stop_sell_item(self, command, character_id)
    if item_name == "exit" or item_name == "stop":
        return item_name

    confirm = await stop_sell_confirm(self, command, discord_id, character_id, item_name)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return


async def stop_sell_item(self, command, character_id):
    option_list = Scripts.stop_sale_items(character_id)
    option_question = "What would you like to stop selling?"
    choice_details = await self.answer_from_list(command, option_question, option_list)
    choice = choice_details.split(" - ")
    return choice[0]


async def stop_sell_confirm(self, command, discord_id, character_id, item_name):
    question = "Do you want stop selling {}? [Yes/No]".format(item_name)
    character_name = Scripts.get_character_name(character_id)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Stopping sale...")
        log = "{} stopped selling {}".format(character_name, item_name)
        await Scripts.stop_sale_confirm(self, discord_id, character_id, item_name, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
################Gifting##################
'''''''''''''''''''''''''''''''''''''''''


async def give_menu(self, command, discord_id, character_id):
    # get character item is being sent to
    target_name = await give_target_name(self, command, character_id)
    if target_name == "exit" or target_name == "stop":
        return target_name
    # get the item they want to send
    item_name = await give_item_choice(self, command, character_id, target_name)
    if item_name == "exit" or item_name == "stop":
        return item_name
    # get the quantity
    quantity = await give_quantity_choice(self, command, character_id, item_name, target_name)
    if quantity == "exit" or quantity == "stop":
        return quantity
    # confirm the gift
    confirm = await give_confirm(self, command, discord_id, character_id, item_name, quantity, target_name)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return


async def give_target_name(self, command, character_id):
    choice_question = "Type the name of the character you want to give items to:"
    choice = await self.character_name_lookup(command, choice_question, character_id)
    return choice


async def give_item_choice(self, command, character_id, target):
    option_list = Scripts.give_character_inventory(character_id)
    option_question = "Please choose which item you want to give to {}:".format(target)
    choice = await self.answer_from_list(command, option_question, option_list)
    choice_details = choice.split(" (")
    item_name = choice_details[0]
    return item_name


async def give_quantity_choice(self, command, character_id, item_name, target_name):
    maximum = Scripts.give_quantity(character_id, item_name)
    if maximum == 1:
        choice = 1
    else:
        choice_question = "You own {} {}, how many do you want to give to {}? " .format(maximum, item_name,
                                                                                       target_name)
        choice = await self.answer_with_int_number(command, choice_question, maximum)
    return choice


async def give_confirm(self, command, discord_id, character_id, item_name, quantity: int, target_name):
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want to give {} {} {} from {}? [Yes/No]".format(target_name, quantity, item_name, character_name)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Giving...")
        log = "{} gave {} {} {}".format(character_name, target_name, quantity, item_name)
        await Scripts.give_confirm(self, discord_id, character_id, target_name, item_name, quantity, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
################Paying##################
'''''''''''''''''''''''''''''''''''''''''


async def pay_menu(self, command, discord_id, character_id):
    welcome_message = "Pay Menu: Type **STOP** at any time to go back to the player menu. \n" \
                      "You can pay other players directly for goods and services."
    await command.message.author.send(welcome_message)
    while True:
        # get character item is being sent to
        target_name = await pay_target_name(self, command, character_id)
        if target_name == "exit" or target_name == "stop":
            return target_name
        # get quantity
        quantity = await pay_quantity(self, command, character_id, target_name)
        if quantity == "exit" or quantity == "stop":
            return quantity
        reason = await pay_reason(self, command, target_name)
        if reason == "exit" or reason == "stop":
            return reason
        # confirm the transaction
        confirm = await pay_confirm(self, command, discord_id, character_id, quantity, target_name, reason)
        if confirm == "exit" or confirm == "stop":
            return confirm
        return


async def pay_target_name(self, command, character_id):
    choice_question = "Type the name of the character you want to pay:"
    choice = await self.character_name_lookup(command, choice_question, character_id)
    return choice


async def pay_quantity(self, command, character_id, target_name):
    maximum = Scripts.pay_character_gold(character_id)
    choice_question = "You currently have {}g, how much do you want to give to {}? [Amount in gold]" .format(maximum, target_name)
    choice = await self.answer_with_float_number(command, choice_question, maximum)
    return choice


async def pay_reason(self, command, target_name):
    question = "Why are you paying {}? [Respond to give reason]" .format(target_name)
    await command.author.send(question)
    choice = await self.answer_with_statement(command)
    return choice


async def pay_confirm(self, command, discord_id, character_id, quantity: float, target_name, reason):
    question = "Do you want to give {} {}g because: {}? [Yes/No]".format(target_name, quantity, reason)
    character_name = Scripts.get_character_name(character_id)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Paying...")
        log = "{} gave {} {}g because: {}".format(character_name, target_name, quantity, reason)
        await Scripts.pay_confirm(self, discord_id, character_id, target_name, quantity, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
################recycle##################
'''''''''''''''''''''''''''''''''''''''''


# recycle item
async def recycle_menu(self, command, discord_id, character_id):
    welcome_message = "Sell Menu: Type **STOP** at any time to go back to the player menu.\n" \
                      "You can sell mundane items to the town at their crafting value."
    await command.message.author.send(welcome_message)
    while True:
        # get the item they want to sell
        item_name = await scrap_item(self, command, character_id)
        if item_name == "exit" or item_name == "stop":
            return item_name
        # get the quantity
        quantity = await recycle_quantity(self, command, character_id, item_name)
        if quantity == "exit" or quantity == "stop":
            return quantity
        # confirm sale
        confirm = await recycle_confirm(self, command, discord_id, character_id, item_name, quantity)
        if confirm == "exit" or confirm == "stop":
            return confirm
        return


async def scrap_item(self, command, character_id,):
    option_list = Scripts.recycle_inventory(character_id)
    option_question = "Please choose which item you want to sell?"
    choice = await self.answer_from_list(command, option_question, option_list)
    choice_details = choice.split(" (")
    item_name = choice_details[0]
    return item_name


async def recycle_quantity(self, command, character_id, item_name):
    character_item = Scripts.recycle_character_item(character_id, item_name)
    maximum = character_item.Quantity

    item_details = Scripts.recycle_item_details(item_name)
    item_value = item_details.Value / 2
    if maximum == 1:
        choice = 1
    else:
        choice_question = "{} sell for {} each, you own {}, how many do you want to sell?"\
            .format(item_name, item_value, maximum, item_name)
        choice = await self.answer_with_int_number(command, choice_question, maximum)
    return choice


async def recycle_confirm(self, command, discord_id, character_id, item_name, quantity: int):
    item_details = Scripts.recycle_item_details(item_name)
    item_value = item_details.Value / 2
    total_value = item_value * quantity
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want to sell {} {} for {}g each for a total of {}g? [Yes/No]".format(quantity, item_name,
                                                                                   item_value, total_value)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Selling...")
        log = "{} recycled {} {} for {}g".format(character_name, quantity, item_name, total_value)
        await Scripts.recycle_confirm(self, discord_id, character_id, item_name, quantity, log)
        await command.author.send(log)
    return "stop"

'''''''''''''''''''''''''''''''''''''''''
#############Share Spell#################
'''''''''''''''''''''''''''''''''''''''''


async def share_spell_menu(self, command, discord_id, character_id):
    welcome_message = "Spell Share Menu: Type **STOP** at any time to go back to the player menu.\n" \
                      "You can give someone access to a spell in your spell book."
    await command.message.author.send(welcome_message)
    # get the target of the share
    target_name = await share_spell_target_name(self, command, character_id)
    if target_name == "exit" or target_name == "stop":
        return target_name
    # get the spell level
    spell_level = await share_spell_level_choice(self, command, character_id)
    if spell_level == "exit" or spell_level == "stop":
        return spell_level
    # get the spell
    spell = await share_spell_spell_choice(self, command, character_id, spell_level)
    if spell == "exit" or spell == "stop":
        return spell
    # confirm
    confirm = await share_spell_confirm(self, command, discord_id, character_id, target_name, spell)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return


async def share_spell_target_name(self, command, character_id):
    choice_question = "Type the name of the character you want to share a spell with."
    choice = await self.character_name_lookup(command, choice_question, character_id)
    return choice


async def share_spell_level_choice(self, command, character_id):
    option_list = Scripts.share_spell_level_options(character_id)
    option_question = "What level spell you want to lend?"
    choice = await self.answer_from_list(command, option_question, option_list)
    result = choice.replace("Level ", "").replace(" spell", "")
    return result


async def share_spell_spell_choice(self, command, character_id, spell_level: int):
    option_list = Scripts.share_spell_options(character_id, spell_level)
    option_question = "Which spell would you like to share?"
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def share_spell_confirm(self, command, discord_id, character_id, target_name, spell_name):
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want to create a scroll of {}?".format(spell_name.replace("''", "'"))
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("sharing spell...")
        log = "{} shared the spell {} with {}.".format(character_name, spell_name.replace("''", "'"), target_name)
        await Scripts.share_spell_confirm(self, discord_id, character_id, target_name, spell_name, log)
        await command.author.send(log)
    return "stop"
