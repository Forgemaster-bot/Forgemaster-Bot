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
                if menu == "exit" or menu == "stop":
                    return menu
        elif choice == "View spell book":
            await command.message.author.send("coming soon")
        elif choice == "exit" or choice == "stop":
            return choice


async def menu_options(self, command, character_name):
    option_list = Scripts.menu(character_name)
    details = Scripts.character_info(character_name)
    option_question = "Character Sheet Menu: " \
                      "Type **STOP** at any time to go back to the player menu \n" \
                      "{} \n" \
                      "What would you like to do?".format(details)
    choice = await self.answer_from_list(command, option_question, option_list)
    return choice


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
        await Scripts.level_up(self, character_name, class_choice, discord_id, log)
        await command.author.send(log)
    return "stop"


# Subclasses
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


# Pick free profession
async def profession_menu(self, command, discord_id, character_name):
    welcome_message = "Profession Menu: Type **STOP** at any time to go back to the player menu " \
                      "\nPick your free crafting profession."
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
