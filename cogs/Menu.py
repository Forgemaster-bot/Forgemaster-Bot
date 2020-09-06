import logging
import asyncio
import itertools
from discord.ext import commands
from cogs.utils import textmenus
import Character.ClassRequirements as ClassRequirements
import cogs.utils.StandaloneQueries as Queries
import Character.CharacterInfoFacade as CharacterInfoFacade
import Character.LinkClassSpellFacade as LinkClassSpellFacade
from Character.CharacterClassFacade import interface as class_interface
from Character.Character import Character
import Connections
import Update_Google_Roster as Roster

log = logging.getLogger(__name__)
blank = '\u200b'


async def start_menu(ctx, menu, **kwargs):
    m = menu(**kwargs)
    channel = kwargs.pop('channel', None)
    await m.start(ctx, wait=True, channel=channel)

    if m.exception and isinstance(m.exception, textmenus.StopException):
        log.debug("Stop exception received")
        pass
    elif m.exception and isinstance(m.exception, textmenus.ExitException):
        log.debug("Exit exception received")
        raise m.exception
    elif m.exception and isinstance(m.exception, asyncio.TimeoutError):
        log.debug("Timeout exception received")
        raise m.exception
    elif not m.single_time:
        await start_menu(ctx, menu, **kwargs)
    return m


class Menu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.players_in_menu = {}

    class BaseMenu(textmenus.Menu):
        """
        Helper base instance for textmenus.Menu. Reuses common code for finalize and getter for title
        """

        def __init__(self, title=None, embed_info=None, stop_on_first=True, **kwargs):
            # Handle creating embed info if one wasn't passed
            embed_info = embed_info if embed_info else self.create_embed_info()
            super().__init__(embed_info=embed_info, stop_on_first=True, **kwargs)
            self.single_time = stop_on_first
            self.timed_out = False
            try:
                self.title
            except AttributeError:
                self.title = title

        def get_title(self):
            return self.title

        def finalize(self, timed_out):
            self.timed_out = timed_out

        def get_initial_message(self):
            return NotImplementedError

        def update_embed(self):
            return

        @staticmethod
        def create_embed_info():
            colour = 0xd0021b
            thumb_url = "https://cdn3.iconfinder.com/data/icons/fantasy-and-role-play-game-adventure-quest/" \
                        "512/Helmet.jpg-512.png"
            footer_text = None
            author = None
            fields = []
            return textmenus.EmbedInfo(thumb_url, author, colour, footer_text, fields)

    class BaseCharacterMenu(BaseMenu):
        """
        Subclass of BaseMenu which requires a character to be passed at initialization.
        This allows us to pass this info to other submenus.
        """

        def __init__(self, character=None, **kwargs):
            super().__init__(**kwargs)
            self.character = character
            self.update_embed()

    class ConfirmMenu(BaseMenu):
        title = "Confirm Choice"

        def __init__(self, message=None, **kwargs):
            super().__init__(**kwargs)
            self.message = message
            self.confirm = False

        def get_initial_message(self):
            return self.message

        @textmenus.submenu('Yes')
        async def confirm(self, payload):
            await self.ctx.channel.send("Confirming...")
            self.confirm = True

        @textmenus.submenu('No')
        async def reject(self, payload):
            await self.ctx.channel.send("Rejecting...")
            self.confirm = False

    class ForgetSpellSelectSpellMenu(BaseCharacterMenu):
        title = "Forget Spell Menu - Forget Spell"

        def get_initial_message(self):
            label = f"Level {self.spell_level} {self.character_class.name} spells"
            return f"Please select a spell from one of the {label} listed."

        def __init__(self, character_class, spell_level, **kwargs):
            super().__init__(**kwargs)
            self.character_class = character_class
            self.spell_level = spell_level
            for spell in self.character_class.get_spells():
                if spell.spell_info.level == self.spell_level:
                    self.submenu(label=spell.name)(self.make_spell_confirm(spell))

        async def on_confirm(self, spell):
            self.character_class.remove_spell(spell)
            self.character_class.can_replace_spells = False
            class_interface.update(self.character_class)
            msg = f"Successfully forgot the spell **{str(spell)}**'!"
            await Connections.log_to_discord(self, msg)
            await self.ctx.channel.send(msg)

        @staticmethod
        def make_spell_confirm(spell):
            async def spell_confirm(menu, payload):
                msg = f"Are you sure you want to learn the spell '{str(spell)}'?"
                m = await start_menu(menu.ctx, Menu.ConfirmMenu, message=msg)
                if m.confirm:
                    await menu.on_confirm(spell)

            return spell_confirm

    class ForgetSpellSelectLevelMenu(BaseCharacterMenu):
        title = "Forget Spell Menu - Select Spell Level"

        def get_initial_message(self):
            return f"Please select the level of {self.character_class.name} spells you would like to forget from."

        def __init__(self, character_class, **kwargs):
            super().__init__(**kwargs)
            self.character_class = character_class
            max_spell_level = Queries.class_max_spell_level(self.character_class)
            for level in range(1, max_spell_level + 1):
                self.submenu(label=f"Level {level} Spells")(self.make_select_spell_level(level, character_class))

        @staticmethod
        def make_select_spell_level(level, character_class):
            async def select_spell_level(menu, payload):
                await start_menu(menu.ctx, Menu.ForgetSpellSelectSpellMenu, character=menu.character,
                                 character_class=character_class, spell_level=level)

            return select_spell_level

    class ForgetSpellMenu(BaseCharacterMenu):
        title = "Forget Spell Menu"

        def get_initial_message(self):
            return f"Please choose a class you would like to forget a spell for."

        def __init__(self, character, spellcaster_classes, **kwargs):
            super().__init__(character, **kwargs)
            self.spellcaster_classes = spellcaster_classes

            for character_class in self.spellcaster_classes:
                if character_class.can_replace_spells:
                    add_to_submenu = self.submenu(character_class.name)
                    func = self.make_select_spell_level(character_class)
                    add_to_submenu(func)

        @staticmethod
        def make_select_spell_level(character_class):
            async def select_spell_level(menu, payload):
                await start_menu(menu.ctx, Menu.ForgetSpellSelectLevelMenu, character=menu.character,
                                 character_class=character_class)

            return select_spell_level

    class LearnSpellSelectSpellMenu(BaseCharacterMenu):
        title = "Learn Spell Menu - Select Spell"

        def get_initial_message(self):
            label = f"Level {self.spell_level} {self.character_class.name} spells"
            return f"Please select a spell from one of the {label} listed."

        def __init__(self, character_class, spell_level, **kwargs):
            super().__init__(**kwargs)
            self.character_class = character_class
            self.spell_level = spell_level
            available_spells = self.character_class.available_class_spells()[self.spell_level]
            if self.character_class.subclass is not None:
                subclass_spells = self.character_class.available_subclass_spells()
                available_spells = {**available_spells, **subclass_spells[spell_level]} \
                    if subclass_spells is not None else available_spells
            available_spells = self.character_class.filter_available_spells(available_spells)
            for name, spell in available_spells.items():
                self.submenu(label=name)(self.make_spell_confirm(spell))

        async def on_confirm(self, spell):
            self.character_class.insert_spell(spell.spell_name, spell.class_name)
            msg = f"{self.character.info.name} has successfully learned the spell **{spell.spell_name}**, " \
                  f"originating from '**{spell.class_name}**'!"
            await Connections.log_to_discord(self, msg)
            await self.ctx.channel.send(msg)
            Roster.update_character_in_roster(self.character)

        @staticmethod
        def make_spell_confirm(spell):
            async def spell_confirm(menu, payload):
                msg = f"Are you sure you want to learn the spell '{spell.spell_name}'?"
                m = await start_menu(menu.ctx, Menu.ConfirmMenu, message=msg)
                if m.confirm:
                    await menu.on_confirm(spell)

            return spell_confirm

    class LearnSpellSelectLevelMenu(BaseCharacterMenu):
        title = "Learn Spell Menu - Select Spell Level"

        def get_initial_message(self):
            return f"Please select the level of {self.character_class.name} spells you would like to learn from."

        def __init__(self, character_class, **kwargs):
            super().__init__(**kwargs)
            self.character_class = character_class
            max_spell_level = Queries.class_max_spell_level(self.character_class)
            for level in range(1, max_spell_level + 1):
                self.submenu(label=f"Level {level} Spells")(self.make_select_spell_level(level, character_class))

        @staticmethod
        def make_select_spell_level(level, character_class):
            async def select_spell_level(menu, payload):
                await start_menu(menu.ctx, Menu.LearnSpellSelectSpellMenu, character=menu.character,
                                 character_class=character_class, spell_level=level)

            return select_spell_level

    class LearnSpellMenu(BaseCharacterMenu):
        title = "Learn Spell Menu"

        def get_initial_message(self):
            return f"Please choose a class you would like to learn a spell for."

        def __init__(self, character, classes_with_spells, **kwargs):
            super().__init__(character, **kwargs)
            self.classes_with_spells = classes_with_spells

            for character_class in self.classes_with_spells:
                if character_class.can_learn_spell():
                    add_to_submenu = self.submenu(character_class.name)
                    func = self.make_select_spell_level(character_class)
                    add_to_submenu(func)

        @staticmethod
        def make_select_spell_level(character_class):
            async def select_spell_level(menu, payload):
                await start_menu(menu.ctx, Menu.LearnSpellSelectLevelMenu, character=menu.character,
                                 character_class=character_class)

            return select_spell_level

    class ViewSpellPreparedMenu(BaseCharacterMenu):
        title = "View Possible Prepared Spells"

        def get_initial_message(self):
            return f"Your possible spells to prepare as a {self.class_name}:"

        def __init__(self, class_name, **kwargs):
            self.class_name = class_name
            super().__init__(**kwargs)

        def update_embed(self):
            max_spell_level = Queries.class_max_spell_level(self.character.classes[self.class_name])
            class_spells = LinkClassSpellFacade.interface.fetch(self.class_name)
            embed_fields = []
            for level in range(1, max_spell_level + 1):
                if level in class_spells:
                    spells = ", ".join(spell.spell_name for spell in class_spells[level].values())
                    embed_fields.append(textmenus.EmbedInfo.Field(f"Level {level}", spells, inline=False))
            if not embed_fields:
                embed_fields.append(textmenus.EmbedInfo.Field("None", blank, inline=False))
            embed_fields.extend(self.embed_info.fields)
            self.embed_info.fields = embed_fields

    class ViewSpellKnownMenu(BaseCharacterMenu):
        title = "View Known Spells"

        def get_initial_message(self):
            return f"Your current spells for '{str(self.character_class)}':"

        def __init__(self, character_class, **kwargs):
            self.character_class = character_class
            super().__init__(**kwargs)

        def update_embed(self):
            embed_fields = []
            spells = []
            for holder in self.character_class.spell_holders.values():
                spells.extend(holder.spells)
            for k, g in itertools.groupby(spells, lambda spell: spell.spell_info.level):
                field = textmenus.EmbedInfo.Field(f"Level {k}", ", ".join(spell.name for spell in g), inline=False)
                embed_fields.append(field)
            if not embed_fields:
                embed_fields.append(textmenus.EmbedInfo.Field("None", blank, inline=False))
            embed_fields.extend(self.embed_info.fields)
            self.embed_info.fields = embed_fields

    class ViewSpellMenu(BaseCharacterMenu):
        title = "View Spells Menu"

        def get_initial_message(self):
            return f"Please choose the class you would like to view spells for."

        def __init__(self, character, spellcaster_classes, **kwargs):
            super().__init__(character, **kwargs)
            self.spellcaster_classes = spellcaster_classes

            for character_class in self.spellcaster_classes:
                name = character_class.class_info.name

                if character_class.class_info.are_spells_memorized():
                    add_to_submenu = self.submenu(name)
                    func = self.make_display_character_class_spells(character_class)
                elif character_class.class_info.are_spells_prepared():
                    add_to_submenu = self.submenu(name)
                    func = self.make_display_prepared_spells(name)
                elif character_class.class_info.has_spellbook():
                    add_to_submenu = self.submenu(name, skip_if=self._skip_display_spellbook_spells)
                    func = self.make_display_character_class_spells(character_class)
                add_to_submenu(func)

        @staticmethod
        def make_display_character_class_spells(character_class):
            async def display_character_class_spells(menu, payload):
                await start_menu(menu.ctx, Menu.ViewSpellKnownMenu, character=menu.character,
                                 character_class=character_class)
            return display_character_class_spells

        @staticmethod
        def make_display_prepared_spells(class_name):
            async def display_class_spells(menu, payload):
                await start_menu(menu.ctx, Menu.ViewSpellPreparedMenu, character=menu.character, class_name=class_name)

            return display_class_spells

        def _skip_display_spellbook_spells(self):
            try:
                return not self.character.has_core_spellbook()
            except AttributeError:
                return True

    class SubclassChoiceMenu(BaseCharacterMenu):
        title = "Pick a Subclass"

        def get_initial_message(self):
            return f"This menu displays the possible subclasses you can select."

        def __init__(self, class_name, **kwargs):
            super().__init__(**kwargs)
            self.class_name = class_name
            self.subclass_choice = None
            options = Queries.select_possible_subclasses(self.class_name)
            for subclass in options:
                add_to_submenu = self.submenu(subclass)
                func = self.make_subclass_confirm(subclass)
                add_to_submenu(func)

        async def on_confirm(self, subclass_name):
            self.character.set_subclass(self.class_name, subclass_name)
            msg = f"**{self.character.info.name}** has selected **{subclass_name}** as their {self.class_name} subclass."
            await Connections.log_to_discord(self, msg)
            await self.ctx.channel.send(msg)
            Roster.update_character_in_roster(self.character)

        @staticmethod
        def make_subclass_confirm(subclass_name):
            async def subclass_confirm(menu, payload):
                msg = f"Are you sure you want to select the subclass '{subclass_name}'?"
                m = await start_menu(menu.ctx, Menu.ConfirmMenu, message=msg)
                if m.confirm:
                    await menu.on_confirm(subclass_name)

            return subclass_confirm

    class SubclassMenu(BaseCharacterMenu):
        title = "Subclass Menu"

        def get_initial_message(self):
            return f"Please choose the class you would like to choose a subclass for."

        def __init__(self, character, **kwargs):
            super().__init__(character, **kwargs)
            available_subclass_choices = ClassRequirements.classes_available_for_subclass(self.character)
            for class_name in available_subclass_choices:
                add_to_submenu = self.submenu(class_name)
                func = self.make_class_choice(class_name)
                add_to_submenu(func)

        @staticmethod
        def make_class_choice(class_name):
            async def class_choice(menu, payload):
                await start_menu(menu.ctx, Menu.SubclassChoiceMenu, character=menu.character, class_name=class_name)

            return class_choice

    class LevelUpMenu(BaseCharacterMenu):
        """
        Level Up menu which allows players to select a class to level up in.
        """
        title = "Level Up Menu"

        def get_initial_message(self):
            return f"Congratulations on leveling up. You may apply this level to any of the available classes below. " \
                   f"**Note:** Classes may not be listed due to ability score requirements."

        def __init__(self, character, **kwargs):
            super().__init__(character, **kwargs)
            available_classes = ClassRequirements.classes_available_for_levelup(self.character)
            for name in available_classes:
                add_to_submenu = self.submenu(name)
                func = self.make_level_up_choice(name)
                add_to_submenu(func)

        async def on_confirm(self, class_name):
            self.character.level_up(class_name)
            msg = f"**{self.character.info.name}** has gained a level in **{class_name}**."
            await Connections.log_to_discord(self, msg)
            await self.ctx.channel.send(msg)
            Roster.update_character_in_roster(self.character)

        @staticmethod
        def make_level_up_choice(class_name):
            async def level_up_confirm(menu, payload):
                msg = f"Are you sure you want to gain a level in '{class_name}'?"
                m = await start_menu(menu.ctx, Menu.ConfirmMenu, message=msg)
                if m.confirm:
                    await menu.on_confirm(class_name)

            return level_up_confirm

    class CharacterSheetMenu(BaseCharacterMenu):
        """
        Character Sheet menu which allows players to manage their character.
        """
        title = "Character Sheet"

        def __init__(self, character: Character, **kwargs):
            super().__init__(character, **kwargs)
            self.character.refresh()
            self.spellcaster_classes = ClassRequirements.all_spellcaster_classes(self.character)
            self.classes_with_spells = [c for c in self.spellcaster_classes if c.can_learn_spell()]

        def get_initial_message(self):
            return f"**{self.character.info.name}**, welcome to your character sheet. " \
                   f"This menu displays a summary of info for your character and allows you to manage your character."

        def update_embed(self):
            feats = self.character.feat_list_as_str()
            skills = self.character.skills_list_as_str()
            items = self.character.item_list_as_str().replace('*', '')
            info_fields = [
                textmenus.EmbedInfo.Field("Name", self.character.info.name, inline=True),
                textmenus.EmbedInfo.Field("XP", self.character.get_xp(), inline=True),
                # textmenus.EmbedInfo.Field("Can Level", self.character.can_level_up(), inline=True),
                textmenus.EmbedInfo.Field("Gold", self.character.get_gold(), inline=True)
            ]
            class_fields = [textmenus.EmbedInfo.Field("Class", c, inline=True) for c in self.character.classes.values()]
            list_fields = [
                textmenus.EmbedInfo.Field("Feats", "None" if not feats else feats, inline=True),
                textmenus.EmbedInfo.Field("Skills", "None" if not skills else skills, inline=True),
                textmenus.EmbedInfo.Field("Stats", self.character.info.formatted_stats()),
                textmenus.EmbedInfo.Field("Items", "None" if not items else items, inline=True)
            ]
            """
            Build the new embed_fields and set them
            """
            embed_fields = []
            embed_fields.extend(info_fields)
            embed_fields.extend(class_fields)
            embed_fields.extend(list_fields)
            embed_fields.extend(self.embed_info.fields)
            self.embed_info.fields = embed_fields

        def _skip_level_up_menu(self):
            """
            Used to determine if the level_up_menu should be displayed or not
            :return: bool - True to skip
            """
            try:
                return not self.character.can_level_up()
            except AttributeError:
                return True

        @textmenus.submenu('Level up your character', skip_if=_skip_level_up_menu)
        async def level_up_menu(self, payload):
            """
            Displays a LevelUpMenu to the user if they are able to level up
            :param payload: message received which caused this option to be selected
            :return: None
            """
            m = await start_menu(self.ctx, Menu.LevelUpMenu, character=self.character)

        def _skip_pick_subclass_menu(self):
            """
            Used to determine if subclass_menu should be displayed or not. Checks if the user has any classes
            which they have not currently picked a subclass for.
            :return:
            """
            try:
                available = any(ClassRequirements.classes_available_for_subclass(self.character))
                return not available
            except AttributeError:
                return True

        @textmenus.submenu('Pick available subclass', skip_if=_skip_pick_subclass_menu)
        async def pick_subclass_menu(self, payload):
            """
            Displays a SubclassMenu to the user if they are able to select a subclass
            :param payload: message received which caused this option to be selected
            :return: None
            """
            await start_menu(self.ctx, Menu.SubclassMenu, character=self.character)

        def _skip_view_spells_menu(self):
            try:
                return not any(self.spellcaster_classes)
            except AttributeError:
                return True

        @textmenus.submenu('View your spells', skip_if=_skip_view_spells_menu)
        async def view_spells_menu(self, payload):
            await start_menu(self.ctx, Menu.ViewSpellMenu, character=self.character,
                             spellcaster_classes=self.spellcaster_classes)

        def _skip_learn_spell_menu(self):
            try:

                return not any(self.classes_with_spells)
            except AttributeError:
                return True

        @textmenus.submenu('Learn a spell', skip_if=_skip_learn_spell_menu)
        async def learn_spell_menu(self, payload):
            await start_menu(self.ctx, Menu.LearnSpellMenu, character=self.character,
                             classes_with_spells=self.classes_with_spells)

        def _skip_forget_spell_menu(self):
            try:
                return not any(c.can_replace_spells for c in self.character.classes.values())
            except AttributeError:
                return True

        @textmenus.submenu('Forget a spell', skip_if=_skip_forget_spell_menu)
        async def forget_spell_menu(self, payload):
            await start_menu(self.ctx, Menu.ForgetSpellMenu, character=self.character,
                             spellcaster_classes=self.spellcaster_classes)

    class WorkshopMenu(BaseCharacterMenu):
        """
        Workshop menu which allows players to craft items or give labor to other players.
        """
        title = "Workshop"

        def get_initial_message(self):
            return "Welcome to the workshop."

        @textmenus.submenu('Create a mundane item')
        async def craft_mundane(self, payload):
            await self.ctx.channel.send("Your mundane recipes would be listed here.")

        @textmenus.submenu('Create a consumable item')
        async def craft_consumable(self, payload):
            await self.ctx.channel.send("Your consumable recipes would be listed here.")

    class MarketMenu(BaseCharacterMenu):
        """
        Market menu which allows players to buy and sell items with other players.
        """
        title = "Market"

        def get_initial_message(self):
            return "Welcome to the market."

        @textmenus.submenu('Buy items from the market')
        async def buy_item_menu(self, payload):
            await self.ctx.channel.send("This would list the menu for buying items from the market")

        @textmenus.submenu('Sell items on the market')
        async def sell_item_menu(self, payload):
            await self.ctx.channel.send("This would list the menu for selling items on the market")

    class MainMenu(BaseCharacterMenu):
        """
        Main Menu which definition which is presented when the `menu` command is invoked.

        Available submenus:
            CharacterSheetMenu
            WorkshopMenu
            MarketMenu
        """
        title = "Main Menu"

        def get_initial_message(self):
            return f"Welcome, **{self.character.info.name}**. What can the Forgemaster do for you?"

        def update_embed(self):
            guide = "Navigation Guide"
            guide_text = "I will provide you a list of available options. " \
                         "Please select an option you'd like me to perform by inputting the identifier (before `:`). " \
                         "**Note:** You may select one of the listed alternate options at anytime."
            guide_field = textmenus.EmbedInfo.Field(guide, guide_text)
            embed_fields = [guide_field]
            embed_fields.extend(self.embed_info.fields)
            self.embed_info.fields = embed_fields

        @textmenus.submenu('Character Sheet')
        async def character_sheet(self, payload):
            await start_menu(self.ctx, Menu.CharacterSheetMenu, character=self.character, stop_on_first=False)

        @textmenus.submenu('Workshop')
        async def workshop(self, payload):
            await start_menu(self.ctx, Menu.WorkshopMenu, character=self.character, stop_on_first=False)

        @textmenus.submenu('Market')
        async def market(self, payload):
            await start_menu(self.ctx, Menu.MarketMenu, character=self.character, stop_on_first=False)

    class CharacterChoiceMenu(BaseMenu):
        title = "Character Choice"
        character_info = None

        def get_initial_message(self):
            return "Welcome to the character select menu. Please select one of the characters below."

        def __init__(self, info_list=[], **kwargs):
            """
            Add a 'dynamic' submenu for each possible character and present menu to user.
            Accomplished by decorating a menu function to set that menu's character_info when selected.
            """
            super().__init__(**kwargs)
            for info in info_list:
                add_to_submenu = self.submenu(info.name)
                func = self.gen_set_character_info(info)
                add_to_submenu(func)

        @staticmethod
        def gen_set_character_info(character_info):
            async def set_character_info(menu, payload):
                log.debug("CharacterChoiceMenu::set_character_info")
                menu.character_info = character_info
                await menu.ctx.channel.send(f"You selected {menu.character_info.name}")

            return set_character_info

    @staticmethod
    async def select_character(ctx):
        """
        Fetches info for discord user. Returns id if available or will prompt user to select one from multiple.
        :param ctx: context
        :return: character_id
        """
        info_list = CharacterInfoFacade.interface.fetch_by_discord_id(ctx.message.author.id)
        if len(info_list) == 0:
            """No characters exist for the caller"""
            return None
        elif len(info_list) == 1:
            """Shortcut to return the only available character."""
            return info_list[0].character_id
        else:
            m = await start_menu(ctx, Menu.CharacterChoiceMenu, info_list=info_list)
            return m.character_info.character_id if m.character_info else None

    @commands.group(name='menu', invoke_without_command=True, brief='Opens the main menu')
    async def menu(self, ctx):
        player_opened_menu = False
        reason = None
        try:
            """
            Handle a player trying to access the menu twice
            """
            if ctx.message.author.id in self.players_in_menu:
                await ctx.message.author.send("You are already accessing the menu.")
                return
            else:
                player_opened_menu = True
                self.players_in_menu[ctx.message.author.id] = None

            """
            Select character before accessing other menus
            """
            character_id = await self.select_character(ctx)
            if character_id is None:
                error_message = "You do not have a character which can access the menu." \
                                "You will need to roll your stats and talk with a Mod to create your character." \
                                "The 'randchar' command will randomly roll your characters stats. " \
                                "Once this is done, a Mod can use the 'Create' command to create your character."
                await ctx.channel.send(error_message)
                return
            """
            Create menu and start querying the user
            """
            m = await start_menu(ctx, Menu.MainMenu, character=Character(character_id), stop_on_first=False)
        except textmenus.StopException:
            reason = "'stop' received"
        except textmenus.ExitException:
            reason = "'exit' received"
        except asyncio.TimeoutError:
            reason = "Timeout occurred"
        finally:
            await ctx.channel.send(f"{reason}. Closing menu.")
            """
            Remove player from list when they leave
            """
            if player_opened_menu:
                self.players_in_menu.pop(ctx.message.author.id)


def setup(bot):
    bot.add_cog(Menu(bot))
