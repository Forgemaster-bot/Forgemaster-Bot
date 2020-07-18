from Player_Menu.Character_Sheet_Menu import Scripts


async def main_menu(self, command, discord_id: int, character_id: str):
    while True:
        choice = await menu_options(self, command, character_id)
        if choice == "View inventory":
            await command.message.author.send(Scripts.inventory_list(character_id))
        elif choice == "Level up your character":
            while True:
                menu = await level_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif choice == "Pick your free crafting profession":
            while True:
                menu = await profession_menu(self, command, discord_id, character_id)
                if menu == "exit" or menu == "stop":
                    return menu
        elif "Pick your subclass for " in choice:
            while True:
                class_choice = choice.replace("Pick your subclass for ", "")
                menu = await subclass_menu(self, command, discord_id, character_id, class_choice)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif "View your " in choice:
            while True:
                class_choice = choice.replace("View your ", "").replace(" spells", "")
                menu = await view_spell_menu(self, command, character_id, class_choice)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif "Learn a new " in choice:
            while True:
                class_choice = choice.replace("Learn a new ", "").replace(" spell", "")

                menu = await learn_spell_menu(self, command, discord_id, character_id, class_choice)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif "Forget a " in choice:
            while True:
                class_choice = choice.replace("Forget a ", "").replace(" spell", "")
                menu = await forget_spell_menu(self, command, discord_id, character_id, class_choice)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif "Divine Soul affinity spell choice" in choice:
            while True:
                menu = await divine_soul_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif "Warlock Pack Boon choice" in choice:
            while True:
                menu = await warlock_pack_menu(self, command, discord_id, character_id)
                if menu == "exit":
                    return menu
                elif menu == "stop":
                    return
        elif choice == "exit" or choice == "stop":
            return choice
        else:
            return "stop"


async def menu_options(self, command, character_id):
    option_list = Scripts.menu(character_id)
    details = Scripts.character_info(character_id)
    option_question = "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n"\
                      "Character Sheet Menu: " \
                      "Type **STOP** at any time to go back to the player menu \n" \
                      "{} \n" \
                      "What would you like to do?".format(details)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


'''''''''''''''''''''''''''''''''''''''''
###############Leveling##################
'''''''''''''''''''''''''''''''''''''''''


async def level_menu(self, command, discord_id, character_id):
    character_levels = Scripts.character_classes(character_id)
    character_name = Scripts.get_character_name(character_id)
    welcome_message = "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n"\
                      "Level Menu: Type **STOP** at any time to go back to the player menu " \
                      "\n{} is currently a {}.".format(character_name, character_levels)
    await command.message.author.send(welcome_message)
    while True:
        class_choice = await level_class_choice(self, command, character_id)
        if class_choice == "exit" or class_choice == "stop":
            return class_choice
        confirm = await level_confirm(self, command, discord_id, character_id, class_choice)
        if confirm == "exit" or confirm == "stop":
            return confirm
        return


async def level_class_choice(self, command, character_id):
    option_list = Scripts.level_up_options(character_id)
    option_question = "Which class would you like to gain a level in?"
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def level_confirm(self, command, discord_id, character_id, class_choice):
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want {} to gain a level in {}? [Yes/No]".format(character_name, class_choice)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("leveling...")
        log = "{} gained a level in {}".format(character_name, class_choice)
        await Scripts.level_up_confirm(self, character_id, class_choice, discord_id, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
###############Subclass##################
'''''''''''''''''''''''''''''''''''''''''


async def subclass_menu(self, command, discord_id, character_id, class_choice):
    welcome_message = "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n"\
                      "Subclass Menu: Type **STOP** at any time to go back to the player menu."
    await command.message.author.send(welcome_message)
    while True:
        choice = await subclass_choice(self, command, class_choice)
        if choice == "exit" or choice == "stop":
            return choice
        confirm = await subclass_confirm(self, command, discord_id, character_id, class_choice, choice)
        if confirm == "exit" or confirm == "stop":
            return confirm
        return


async def subclass_choice(self, command, class_choice):
    option_list = Scripts.subclass_options(class_choice)
    option_question = "Which speciality do you wish to pick as a {}?".format(class_choice)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def subclass_confirm(self, command, discord_id, character_id, class_choice, subclass):
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want {} to specialise as a {} {}? [Yes/No]".format(character_name, subclass, class_choice)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Specialising...")
        log = "{} specialised as a {} {}".format(character_name, subclass, class_choice)
        await Scripts.subclass_confirm(self, character_id, class_choice, subclass, discord_id, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
##############Profession#################
'''''''''''''''''''''''''''''''''''''''''


async def profession_menu(self, command, discord_id, character_id):
    welcome_message = "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n"\
                      "Profession Menu: Type **STOP** at any time to go back to the player menu " \
                      "\nPick your free crafting profession."
    await command.message.author.send(welcome_message)
    while True:
        profession_choice = await profession_step_1_profession_choice(self, command)
        if profession_choice == "exit" or profession_choice == "stop":
            return profession_choice
        confirm = await profession_step_2_confirm(self, command, discord_id, character_id, profession_choice)
        if confirm == "exit" or confirm == "stop":
            return confirm
        return


async def profession_step_1_profession_choice(self, command):
    option_list = Scripts.profession_list()
    option_question = "Which profession would you like to gain have?"
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def profession_step_2_confirm(self, command, discord_id, character_id, profession_name):
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want {} to gain {} as a profession? [Yes/No]".format(character_name, profession_name)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Adding profession...")
        log = "{} gained {} as their free profession".format(character_name, profession_name)
        await Scripts.give_profession(self, character_id, profession_name, discord_id, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
##############View Spells################
'''''''''''''''''''''''''''''''''''''''''


async def view_spell_menu(self, command, character_id: str, class_name: str):
    welcome_message = "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n"\
                      "View {} Spell Menu: Type **STOP** at any time to go back to the player menu." .format(class_name)
    await command.message.author.send(welcome_message)
    # if wizard get spell levels from spell books
    if class_name == 'Wizard':
        await command.message.author.send(Scripts.view_spells_all_book_spells(character_id))
        return "stop"
    elif Scripts.class_must_learn_spells(class_name):
        await command.message.author.send(Scripts.view_spells_list_all_spells(character_id, class_name))
        return "stop"
    else:
        while True:
            spell_level_choice = await view_spell_level_choice(self, command, character_id, class_name)
            if spell_level_choice == "exit" or spell_level_choice == "stop":
                return spell_level_choice
            spell_level = spell_level_choice.replace("Level ", "", ).replace(" Spells", "")
            await command.message.author.send(Scripts.view_spells_by_level(character_id, class_name, spell_level))
            return "stop"


async def view_spell_level_choice(self, command, character_id, class_choice):
    option_list = Scripts.spells_level_options(character_id, class_choice)
    option_question = "As a {}, you know all of your class spells, Which level of spell would you like to view?"\
        .format(class_choice)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


'''''''''''''''''''''''''''''''''''''''''
#############Learn Spells################
'''''''''''''''''''''''''''''''''''''''''


async def learn_spell_menu(self, command, discord_id, character_id: str, class_name: str):
    welcome_message = "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n"\
                      "Learn {} Spell Menu: Type **STOP** at any time to go back to the player menu.".format(class_name)
    await command.message.author.send(welcome_message)
    # pick spell level
    spell_level_choice = await learn_spell_level_choice(self, command, character_id, class_name)
    if spell_level_choice == "exit" or spell_level_choice == "stop":
        return spell_level_choice

    spell_choice = await learn_spell_choice(self, command, character_id, class_name, spell_level_choice)
    if spell_choice == "exit" or spell_choice == "stop":
        return spell_choice

    confirm = await learn_spell_confirm(self, command, discord_id, character_id, class_name, spell_choice)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return "stop"


async def learn_spell_level_choice(self, command, character_id, class_name):
    option_list = Scripts.spells_level_options(character_id, class_name)
    option_question = "What level of spell would you like to learn?".format(class_name)
    choice = await self.answer_from_list(command, option_question, option_list)
    result = choice.replace("Level ", "").replace(" Spells", "")
    return result


async def learn_spell_choice(self, command, character_id, class_name, spell_level: int):
    option_list = Scripts.learnable_spells_by_level(character_id, class_name, spell_level)
    option_question = "Which spell would you like to learn?".format(class_name)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def learn_spell_confirm(self, command, discord_id, character_id, class_name, spell_choice):
    character_name = Scripts.get_character_name(character_id)
    if class_name == 'Wizard':
        question = "Do you want to add {} to your spell book? [Yes/No]".format(spell_choice.replace("''", "'"))
        log = "{} added {} to their spell book from leveling up.".format(character_name, spell_choice)
    else:
        question = "Do you want to learn {} as a {}? [Yes/No]".format(spell_choice.replace("''", "'"), class_name)
        log = "{} learnt {} as a {}.".format(character_name, spell_choice, class_name)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("learning spell...")
        await Scripts.learning_spell_confirm(self, discord_id, character_id, class_name, spell_choice, log)
        await command.author.send(log.replace("''", "'"))
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
#############Forget Spell################
'''''''''''''''''''''''''''''''''''''''''


async def forget_spell_menu(self, command, discord_id, character_id: str, class_name: str):
    welcome_message = "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n"\
                      "{} Learn Spell Menu: Type **STOP** at any time to go back to the player menu.".format(class_name)
    await command.message.author.send(welcome_message)
    # pick spell level

    spell_choice = await forget_spell_choice(self, command, character_id, class_name)
    if spell_choice == "exit" or spell_choice == "stop":
        return spell_choice

    confirm = await forget_spell_confirm(self, command, discord_id, character_id, class_name, spell_choice)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return "stop"


async def forget_spell_choice(self, command, character_id, class_name):
    option_list = Scripts.forget_spells_list(character_id, class_name)
    option_question = "Which spell would you like to forget?"
    choice = await self.answer_from_list(command, option_question, option_list)
    if choice == "exit" or choice == "stop":
        return choice
    result = choice.split(":")
    return result[1].lstrip()


async def forget_spell_confirm(self, command, discord_id, character_id, class_name, spell_choice):
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want to forget the {} spell {}? [Yes/No]".format(class_name, spell_choice.replace("''", "'"))
    log = "{} forgot {} as a {}.".format(character_name, spell_choice.replace("''", "'"), class_name)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("Forgetting spell...")
        await Scripts.forget_spell_confirm(self, discord_id, character_id, class_name, spell_choice, log)
        await command.author.send(log)
    return "stop"


'''''''''''''''''''''''''''''''''''''''''
###########Sub_Class Choices#############
'''''''''''''''''''''''''''''''''''''''''


async def divine_soul_menu(self, command, discord_id, character_id: str):
    welcome_message = "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n"\
                      "Divine Soul Spell Menu: Type **STOP** at any time to go back to the player menu."
    await command.message.author.send(welcome_message)
    # pick spell level

    spell_choice = await divine_soul_spell_choice(self, command)
    if spell_choice == "exit" or spell_choice == "stop":
        return spell_choice

    confirm = await divine_soul_confirm(self, command, discord_id, character_id, spell_choice)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return "stop"


async def divine_soul_spell_choice(self, command):
    option_list = ['Cure Wounds', 'Inflict Wounds', 'Bless', 'Bane', 'Protection from Evil and Good']
    option_question = "Which spell would you like to learn?"
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


async def divine_soul_confirm(self, command, discord_id, character_id, spell_choice):
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want to learn {} as your divine soul affinity spell? [Yes/No]".format(spell_choice)
    log = "{} learnt {} as a their divine soul affinity spell.".format(character_name, spell_choice)
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes":
        await command.author.send("learning spell...")
        await Scripts.divine_soul_confirm(self, discord_id, character_id, spell_choice, log)
        await command.author.send(log.replace("''", "'"))
    return "stop"


async def warlock_pack_menu(self, command, discord_id, character_id: str):
    welcome_message = "~~- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -~~\n"\
                      "Warlock Pack boon Menu: Type **STOP** at any time to go back to the player menu."
    await command.message.author.send(welcome_message)
    # pick spell level

    confirm = await warlock_pack_confirm(self, command, discord_id, character_id)
    if confirm == "exit" or confirm == "stop":
        return confirm
    return "stop"


async def warlock_pack_confirm(self, command, discord_id, character_id):
    character_name = Scripts.get_character_name(character_id)
    question = "Do you want to be a pack of the tome warlock with the book of ancient secrets invocation? [Yes/No]"
    await command.author.send(question)
    reply = await self.confirm(command)
    if reply == "Yes" or reply == 'No':
        if reply == 'Yes':
            log = "{} is a pack of the tome warlock with the book of ancient secrets invocation.".format(character_name)
            await command.author.send("creating book of shadows...")
        else:
            log = '{} is not a pack of the tome warlock, and wont have a book of secrets'.format(character_name)
            await command.author.send("working...")
        await Scripts.warlock_tome_confirm(self, discord_id, character_id, reply, log)
        await command.author.send(log.replace("''", "'"))
    return "stop"
