from Player_Menu.Character_Sheet_Menu import Scripts


async def main_menu(self, command, discord_id: int, character_name: str):
    while True:
        choice = await menu_options(self, command, character_name)
        if choice == "View inventory":
            await command.message.author.send(Scripts.inventory_list(character_name))
        elif choice == "Level up your character":
            while True:
                menu = await level_menu(self, command, discord_id, character_name)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif choice == "Pick your free crafting profession":
            while True:
                menu = await profession_menu(self, command, discord_id, character_name)
                if menu == "exit" or menu == "stop":
                    return menu
        elif "Pick your subclass for " in choice:
            while True:
                class_choice = choice.replace("Pick your subclass for ", "")
                menu = await subclass_menu(self, command, discord_id, character_name, class_choice)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif "View your " in choice:
            while True:
                class_choice = choice.replace("View your ", "").replace(" spells", "")
                menu = await view_spell_menu(self, command, character_name, class_choice)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif "Learn a new " in choice:
            while True:
                class_choice = choice.replace("Learn a new ", "").replace(" spell", "")
                menu = await learn_spell_menu(self, command, discord_id, character_name, class_choice)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif "Forget a " in choice:
            while True:
                class_choice = choice.replace("Forget a ", "").replace(" spell", "")
                menu = await forget_spell_menu(self, command, discord_id, character_name, class_choice)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif choice == "exit":
            return choice
        else:
            return


async def menu_options(self, command, character_name):
    option_list = Scripts.menu(character_name)
    details = Scripts.character_info(character_name)
    option_question = "Character Sheet Menu: " \
                      "Type **STOP** at any time to go back to the player menu \n" \
                      "{} \n" \
                      "What would you like to do?".format(details)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


'''''''''''''''''''''''''''''''''''''''''
###############Leveling##################
'''''''''''''''''''''''''''''''''''''''''


async def level_menu(self, command, discord_id, character_name):
    character_levels = Scripts.character_classes(character_name)
    welcome_message = "Level Menu: Type **STOP** at any time to go back to the player menu " \
                      "\n{} is currently a {}.".format(character_name, character_levels)
    await command.message.author.send(welcome_message)
    while True:
        class_choice = await level_class_choice(self, command, character_name)
        if class_choice == "exit" or class_choice == "stop":
            return class_choice
        confirm = await level_confirm(self, command, discord_id, character_name, class_choice)
        if confirm == "exit" or confirm == "stop":
            return confirm
        return


async def level_class_choice(self, command, character_name):
    option_list = Scripts.level_up_options(character_name)
    option_question = "Which class would you like to gain a level in?"
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def level_confirm(self, command, discord_id, character_name, class_choice):
    question = "Do you want {} to gain a level in {}?".format(character_name, class_choice)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("leveling...")
        log = "{} gained a level in {}".format(character_name, class_choice)
        await Scripts.level_up_confirm(self, character_name, class_choice, discord_id, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
###############Subclass##################
'''''''''''''''''''''''''''''''''''''''''


async def subclass_menu(self, command, discord_id, character_name, class_choice):
    character_levels = Scripts.character_classes(character_name)
    welcome_message = "Subclass Menu: Type **STOP** at any time to go back to the player menu." \
                      .format(character_name, character_levels)
    await command.message.author.send(welcome_message)
    while True:
        choice = await subclass_choice(self, command, class_choice)
        if choice == "exit" or choice == "stop":
            return choice
        confirm = await subclass_confirm(self, command, discord_id, character_name, class_choice, choice)
        if confirm == "exit" or confirm == "stop":
            return confirm
        return


async def subclass_choice(self, command, class_choice):
    option_list = Scripts.subclass_options(class_choice)
    option_question = "Which speciality do you wish to pick as a {}?".format(class_choice)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def subclass_confirm(self, command, discord_id, character_name, class_choice, subclass):
    question = "Do you want {} to specialise as a {} {}?".format(character_name, subclass, class_choice)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Specialising...")
        log = "{} specialised as a {} {}".format(character_name, subclass, class_choice)
        await Scripts.subclass_confirm(self, character_name, class_choice, subclass, discord_id, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
##############Profession#################
'''''''''''''''''''''''''''''''''''''''''


async def profession_menu(self, command, discord_id, character_name):
    welcome_message = "Profession Menu: Type **STOP** at any time to go back to the player menu " \
                      "\nPick your free crafting profession."
    await command.message.author.send(welcome_message)
    while True:
        profession_choice = await profession_step_1_profession_choice(self, command)
        if profession_choice == "exit" or profession_choice == "stop":
            return profession_choice
        confirm = await profession_step_2_confirm(self, command, discord_id, character_name, profession_choice)
        if confirm == "exit" or confirm == "stop":
            return confirm
        return


async def profession_step_1_profession_choice(self, command):
    option_list = Scripts.profession_list()
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
        await Scripts.give_profession(self, character_name, profession_name, discord_id, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
##############View Spells################
'''''''''''''''''''''''''''''''''''''''''


async def view_spell_menu(self, command, character_name: str, class_name: str):
    welcome_message = "View {} Spell Menu: Type **STOP** at any time to go back to the player menu." .format(class_name)
    await command.message.author.send(welcome_message)
    # if wizard get spell levels from spell books
    if class_name == 'Wizard':
        await command.message.author.send(Scripts.view_spells_all_book_spells(character_name))
        return "stop"
    elif Scripts.class_must_learn_spells(class_name):
        await command.message.author.send(Scripts.view_spells_list_all_spells(character_name, class_name))
        return "stop"
    else:
        while True:
            spell_level_choice = await view_spell_level_choice(self, command, character_name, class_name)
            if spell_level_choice == "exit" or spell_level_choice == "stop":
                return spell_level_choice
            spell_level = spell_level_choice.replace("Level ", "", ).replace(" Spells", "")
            await command.message.author.send(Scripts.view_spells_by_level(character_name, class_name, spell_level))
            return "stop"


async def view_spell_level_choice(self, command, character_name, class_choice):
    option_list = Scripts.spells_level_options(character_name, class_choice)
    option_question = "As a {}, you know all of your class spells, Which level of spell would you like to view?"\
        .format(class_choice)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


'''''''''''''''''''''''''''''''''''''''''
#############Learn Spells################
'''''''''''''''''''''''''''''''''''''''''


async def learn_spell_menu(self, command, discord_id, character_name: str, class_name: str):
    welcome_message = "Learn {} Spell Menu: Type **STOP** at any time to go back to the player menu.".format(class_name)
    await command.message.author.send(welcome_message)
    # pick spell level
    spell_level_choice = await learn_spell_level_choice(self, command, character_name, class_name)
    if spell_level_choice == "exit" or spell_level_choice == "stop":
        return spell_level_choice

    spell_choice = await learn_spell_choice(self, command, character_name, class_name, spell_level_choice)
    if spell_choice == "exit" or spell_choice == "stop":
        return spell_choice

    confirm = await learn_spell_confirm(self, command, discord_id, character_name, class_name, spell_choice)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return "stop"


async def learn_spell_level_choice(self, command, character_name, class_name):
    option_list = Scripts.spells_level_options(character_name, class_name)
    option_question = "What level of spell would you like to learn?".format(class_name)
    choice = await self.answer_from_list(command, option_question, option_list)
    result = choice.replace("Level ", "").replace(" Spells", "")
    return result


async def learn_spell_choice(self, command, character_name, class_name, spell_level: int):
    option_list = Scripts.learnable_spells_by_level(character_name, class_name, spell_level)
    option_question = "Which spell would you like to learn?".format(class_name)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def learn_spell_confirm(self, command, discord_id, character_name, class_name, spell_choice):
    if class_name == 'Wizard':
        question = "Do you want to add {} to your spell book?".format(spell_choice.replace("''", "'"))
        log = "{} added {} to their spell book from leveling up.".format(character_name,
                                                                         spell_choice)
    else:
        question = "Do you want to learn {} as a {}?".format(spell_choice.replace("''", "'"), class_name)
        log = "{} learnt {} as a {}.".format(character_name, spell_choice, class_name)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("learning spell...")
        await Scripts.learning_spell_confirm(self, discord_id, character_name, class_name, spell_choice, log)
        await command.author.send(log.replace("''", "'"))
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
#############Forget Spell################
'''''''''''''''''''''''''''''''''''''''''


async def forget_spell_menu(self, command, discord_id, character_name: str, class_name: str):
    welcome_message = "{} Learn Spell Menu: Type **STOP** at any time to go back to the player menu.".format(class_name)
    await command.message.author.send(welcome_message)
    # pick spell level

    spell_choice = await forget_spell_choice(self, command, character_name, class_name)
    if spell_choice == "exit" or spell_choice == "stop":
        return spell_choice

    confirm = await forget_spell_confirm(self, command, discord_id, character_name, class_name, spell_choice)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return "stop"


async def forget_spell_choice(self, command, character_name, class_name):
    option_list = Scripts.forget_spells_list(character_name, class_name)
    option_question = "Which spell would you like to forget?".format(class_name)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def forget_spell_confirm(self, command, discord_id, character_name, class_name, spell_choice):
    question = "Do you want to forget the {} spell {}?".format(class_name, spell_choice)
    log = "{} forgot {} as a {}.".format(character_name, spell_choice, class_name)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Forgetting spell...")
        await Scripts.learning_spell_confirm(self, discord_id, character_name, class_name, spell_choice, log)
        await command.author.send(log)
    return "stop"
