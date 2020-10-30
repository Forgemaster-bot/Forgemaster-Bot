import logging
import asyncio
import itertools
import textwrap
from typing import Callable, Awaitable, List
import discord
from discord.ext import commands
import Exceptions
from cogs.utils import textmenus
from cogs.utils import StandaloneQueries
from cogs.utils.menu import start_menu, BaseMenu, BaseCharacterMenu, ConfirmMenu, ListMenu
from cogs.utils import menu as menu_helper
from cogs.utils import workshop
import Character.ClassRequirements as ClassRequirements
import Character.CharacterInfoFacade as CharacterInfoFacade
import Character.LinkClassSpellFacade as LinkClassSpellFacade
from Character.SkillInfoFacade import interface as skill_info_interface
from Character.Data.CharacterInfo import CharacterInfo
from Character.Data.LinkClassSpell import LinkClassSpell
from Character.Character import Character
import Connections
import Update_Google_Roster as Roster

from cogs.old_menus.Workshop_Menu import Menu as OldWorkshopMenu
from cogs.old_menus.Market_Menu import Menu as OldMarketMenu

log = logging.getLogger(__name__)
blank = '\u200b'

class Menu(commands.Cog):

    should_dm = True

    def __init__(self, bot):
        self.bot = bot
        self.players_in_menu = {}

    class FreeProfessionConfirmMenu(ConfirmMenu, BaseCharacterMenu):
        title = "Free Profession Menu - Confirm Choice"

        def __init__(self, skill, **kwargs):
            message = f"Are you sure you want to learn the job '{skill.name}'?"
            super().__init__(message=message, **kwargs)
            self.skill = skill

        async def on_confirm(self, payload):
            await super().on_confirm(payload)
            self.character.learn_skill(self.skill)
            msg = f"{self.character.name} has used their free profession slot to become a '**{self.skill.name}**'"
            await Connections.log_to_discord(self, msg)
            await self.channel.send(msg)
            Roster.update_character_in_roster(self.character)

    class FreeProfessionMenu(BaseCharacterMenu):
        """
        FreeProfessionMenu menu which allows players to select a job if they don't have one.
        """
        title = "Free Profession Menu"

        def get_initial_message(self):
            return f"Each character in this world has some way to make a living. " \
                   f"Since you do not have a job, you are allowed to select one of the following. " \
                   f"This will allow you to craft goods which can be used by yourself or other characters."

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            for job_name, skill_obj in skill_info_interface.fetch_jobs().items():
                self.submenu(label=job_name)(self.make_job_choice(skill_obj))

        @staticmethod
        def make_job_choice(skill_obj):
            async def job_confirm(menu, _):
                await start_menu(menu.ctx, Menu.FreeProfessionConfirmMenu, character=menu.character,
                                 skill=skill_obj)
            return job_confirm

    class ForgetSpellConfirmMenu(ConfirmMenu, BaseCharacterMenu):
        title = "Forget Spell Menu - Confirm Choice"

        def __init__(self, spell, character_class, **kwargs):
            message = f"Are you sure you want to forget the spell '{str(spell)}'?"
            super().__init__(message=message, **kwargs)
            self.spell = spell
            self.character_class = character_class

        async def on_confirm(self, payload):
            await ConfirmMenu.on_confirm(self, payload)
            await self.character.forget_spell(self.character_class, self.spell, cog=self, channel=self.channel)

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

        @staticmethod
        def make_spell_confirm(spell):
            async def spell_confirm(menu, _):
                await start_menu(menu.ctx, Menu.ForgetSpellConfirmMenu, character=menu.character,
                                 character_class=menu.character_class, spell=spell)
            return spell_confirm

    class ForgetSpellSelectLevelMenu(BaseCharacterMenu):
        title = "Forget Spell Menu - Select Spell Level"

        def get_initial_message(self):
            return f"Please select the level of {self.character_class.name} spells you would like to forget from."

        def __init__(self, character_class, **kwargs):
            super().__init__(**kwargs)
            self.character_class = character_class
            for level in range(1, StandaloneQueries.class_max_spell_level(self.character_class) + 1):
                self.submenu(label=f"Level {level} Spells")(self.make_select_spell_level(level, self.character_class))

        @staticmethod
        def make_select_spell_level(level, character_class):
            async def select_spell_level(menu, _):
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
            async def select_spell_level(menu, _):
                await start_menu(menu.ctx, Menu.ForgetSpellSelectLevelMenu, character=menu.character,
                                 character_class=character_class)
            return select_spell_level

    class LearnSpellConfirmMenu(ConfirmMenu, BaseCharacterMenu):
        title = "Learn Spell Menu - Confirm Choice"

        def __init__(self, spell, character_class, **kwargs):
            message = f"Are you sure you want to learn the spell '{str(spell)}'?"
            super().__init__(message=message, **kwargs)
            self.spell = spell
            self.character_class = character_class

        async def on_confirm(self, payload):
            await ConfirmMenu.on_confirm(self, payload)
            await self.character.learn_spell(self.character_class, self.spell, cog=self, channel=self.channel)

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
                if subclass_spells is not None:
                    available_spells = {**available_spells, **subclass_spells[spell_level]}

            available_spells = self.character_class.filter_available_spells(available_spells)
            for name, spell in available_spells.items():
                self.submenu(label=name)(self.make_spell_confirm(spell))

        @staticmethod
        def make_spell_confirm(spell):
            async def spell_confirm(menu, _):
                await start_menu(menu.ctx, Menu.LearnSpellConfirmMenu, character=menu.character,
                                 character_class=menu.character_class, spell=spell)
            return spell_confirm

    class LearnSpellSelectLevelMenu(BaseCharacterMenu):
        title = "Learn Spell Menu - Select Spell Level"

        def get_initial_message(self):
            return f"Please select the level of {self.character_class.name} spells you would like to learn from."

        def __init__(self, character_class, **kwargs):
            super().__init__(**kwargs)
            self.character_class = character_class
            max_spell_level = StandaloneQueries.class_max_spell_level(self.character_class)
            for level in range(1, max_spell_level + 1):
                self.submenu(label=f"Level {level} Spells")(self.make_select_spell_level(level, character_class))

        @staticmethod
        def make_select_spell_level(level, character_class):
            async def select_spell_level(menu, _):
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
            async def select_spell_level(menu, _):
                await start_menu(menu.ctx, Menu.LearnSpellSelectLevelMenu, character=menu.character,
                                 character_class=character_class)

            return select_spell_level

    class DivineSoulMenu(BaseCharacterMenu):
        title = "Divine Soul Affinity - Select Spell"

        def get_initial_message(self):
            label = f"**'Divine Soul'**"
            return f"Please select a spell from one of the {label} listed."

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.character_class = 'Sorcerer'
            available_spells = ['Cure Wounds', 'Inflict Wounds', 'Bless', 'Bane', 'Protection from Good and Evil']
            for name in available_spells:
                spell = LinkClassSpell('Divine Soul', name)
                self.submenu(label=name)(self.make_spell_confirm(spell))

        @staticmethod
        def make_spell_confirm(spell):
            async def spell_confirm(menu, _):
                await start_menu(menu.ctx, Menu.DivineSoulMenu.DivineSoulConfirmMenu, character=menu.character,
                                 character_class=menu.character_class, spell=spell)
            return spell_confirm

        class DivineSoulConfirmMenu(ConfirmMenu, BaseCharacterMenu):
            title = "Divine Soul Affinity - Confirm Choice"

            def __init__(self, spell, character_class, **kwargs):
                message = f"Are you sure you want to select the spell '{str(spell)}' as your Divine Soul Affinity?"
                super().__init__(message=message, **kwargs)
                self.spell = spell
                self.character_class = character_class

            async def on_confirm(self, payload):
                await ConfirmMenu.on_confirm(self, payload)
                await self.character.learn_spell(self.character_class, self.spell)
                self.character.update_class_choice(self.character_class, False)
                msg = f"{self.character.name} used their divine soul affinity to learn **{str(self.spell)}**'!"
                await Connections.log_to_discord(self, msg)
                await self.channel.send(msg)

    class ViewSpellPreparedMenu(BaseCharacterMenu):
        title = "View Possible Prepared Spells"

        def get_initial_message(self):
            return f"Your possible spells to prepare as a {self.class_name}:"

        def __init__(self, class_name, **kwargs):
            self.class_name = class_name
            super().__init__(**kwargs)

        def update_embed(self):
            max_spell_level = StandaloneQueries.class_max_spell_level(self.character.classes[self.class_name])
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
                    # Add submenu which displays memorized spells
                    self.submenu(label=name)(self.make_display_character_class_spells(character_class))
                elif character_class.class_info.are_spells_prepared():
                    # Add submenu which displays all possible prepared spells
                    self.submenu(label=name)(self.make_display_prepared_spells(name))
                elif character_class.class_info.has_spellbook():
                    # Add submenu which displays class spells if they have the right spellbook
                    func = self.make_display_character_class_spells(character_class)
                    self.submenu(name, skip_if=self._skip_display_spellbook_spells)(func)

        @staticmethod
        def make_display_character_class_spells(character_class):
            async def display_character_class_spells(menu, _):
                await start_menu(menu.ctx, Menu.ViewSpellKnownMenu, character=menu.character,
                                 character_class=character_class)
            return display_character_class_spells

        @staticmethod
        def make_display_prepared_spells(class_name):
            async def display_class_spells(menu, _):
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
            options = StandaloneQueries.select_possible_subclasses(self.class_name)
            for subclass in options:
                add_to_submenu = self.submenu(subclass)
                func = self.make_subclass_confirm(subclass)
                add_to_submenu(func)

        async def on_confirm(self, subclass_name):
            self.character.set_subclass(self.class_name, subclass_name)
            msg = f"**{self.character.info.name}** has selected **{subclass_name}** as their {self.class_name} subclass"
            await Connections.log_to_discord(self, msg)
            await self.channel.send(msg)
            Roster.update_character_in_roster(self.character)

        @staticmethod
        def make_subclass_confirm(subclass_name):
            async def subclass_confirm(menu, _):
                msg = f"Are you sure you want to select the subclass '{subclass_name}'?"
                m = await start_menu(menu.ctx, ConfirmMenu, message=msg)
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
            async def class_choice(menu, _):
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
                self.submenu(label=name)(self.make_level_up_choice(name))

        async def on_confirm(self, class_name):
            await self.character.level_up(class_name, cog=self, channel=self.channel)
            msg = f"**{self.character.info.name}** has gained a level in **{class_name}**."
            await Connections.log_to_discord(self, msg)
            await self.channel.send(msg)
            Roster.update_character_in_roster(self.character)

        @staticmethod
        def make_level_up_choice(class_name):
            async def level_up_confirm(menu, _):
                msg = f"Are you sure you want to gain a level in '{class_name}'?"
                m = await start_menu(menu.ctx, ConfirmMenu, message=msg)
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
                textmenus.EmbedInfo.Field("Gold", f"{self.character.get_gold():.2f}", inline=True)
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
        async def level_up_menu(self, _):
            """
            Displays a LevelUpMenu to the user if they are able to level up
            :param _: message received which caused this option to be selected
            :return: None
            """
            await start_menu(self.ctx, Menu.LevelUpMenu, character=self.character)

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
        async def pick_subclass_menu(self, _):
            """
            Displays a SubclassMenu to the user if they are able to select a subclass
            :param _: message received which caused this option to be selected
            :return: None
            """
            await start_menu(self.ctx, Menu.SubclassMenu, character=self.character)

        def _skip_view_spells_menu(self):
            try:
                return not any(self.spellcaster_classes)
            except AttributeError:
                return True

        @textmenus.submenu('View your spells', skip_if=_skip_view_spells_menu)
        async def view_spells_menu(self, _):
            await start_menu(self.ctx, Menu.ViewSpellMenu, character=self.character,
                             spellcaster_classes=self.spellcaster_classes)

        def _skip_learn_spell_menu(self):
            try:

                return not any(self.classes_with_spells)
            except AttributeError:
                return True

        @textmenus.submenu('Learn a spell', skip_if=_skip_learn_spell_menu)
        async def learn_spell_menu(self, _):
            await start_menu(self.ctx, Menu.LearnSpellMenu, character=self.character,
                             classes_with_spells=self.classes_with_spells)

        def _skip_forget_spell_menu(self):
            try:
                return not any(c.can_replace_spells for c in self.character.classes.values())
            except AttributeError:
                return True

        @textmenus.submenu('Forget a spell', skip_if=_skip_forget_spell_menu)
        async def forget_spell_menu(self, _):
            await start_menu(self.ctx, Menu.ForgetSpellMenu, character=self.character,
                             spellcaster_classes=self.spellcaster_classes)

        def _skip_free_profession(self):
            try:
                skills = self.character.skills
                jobs = [skill for skill in skills if skill.name in skill_info_interface.fetch_jobs()]
                return len(jobs) > 0
            except AttributeError:
                return True

        @textmenus.submenu("Pick a free profession", skip_if=_skip_free_profession)
        async def pick_free_profession(self, _):
            await start_menu(self.ctx, Menu.FreeProfessionMenu, character=self.character)

        def _skip_divine_soul_choice(self):
            try:
                available = self.character.has_subclass_choice('Divine Soul')
                log.debug(f"_skip_divine_soul_choice available = {available}")
                return not available
            except AttributeError:
                log.debug(f"_skip_divine_soul_choice available = attribute error")
                return True

        @textmenus.submenu("Pick your Divine Soul Affinity", skip_if=_skip_divine_soul_choice)
        async def divine_soul_choice(self, _):
            await start_menu(self.ctx, Menu.DivineSoulMenu, character=self.character)

    class WorkshopMenu(BaseCharacterMenu):
        """
        Workshop menu which allows players to craft items or give labor to other players.
        """
        title = "Workshop"

        def get_initial_message(self):
            return textwrap.dedent("""\
            Welcome to the workshop. In this menu, you can perform various tasks related to crafting or making things  
            for your character. When crafting mundane items, you may spend up to a weekly crafting limit in gold to 
            produce items. This weekly limit acts as the amount of 'labor' you can expend in a week.\n
            **Note**: This limit resets Sunday night at midnight EST/EDT.
            """)

        def update_embed(self):
            jobs = [skill for skill in self.character.skills if skill.name in skill_info_interface.fetch_jobs()]
            jobs_str = "None" if not jobs else ", ".join(job.name for job in jobs)
            crafting_limit_row = StandaloneQueries.fetch_crafting_limit_row(self.character.id)
            # limit = StandaloneQueries.calculate_crafting_limit(crafting_limit_row, self.character.get_gold())
            limit = crafting_limit_row.Crafting_Value
            """
            Build fields list for the embed sent for this menu
            """
            embed_fields = [
                textmenus.EmbedInfo.Field("Name", self.character.info.name, inline=True),
                textmenus.EmbedInfo.Field("Gold", f"{self.character.get_gold():.2f}", inline=True),
                textmenus.EmbedInfo.Field("Workers", crafting_limit_row.Labour_Points, inline=True),
                textmenus.EmbedInfo.Field("Professions", jobs_str, inline=True),
                textmenus.EmbedInfo.Field("Current Weekly Limit", f"{limit:.2f}", inline=True)
            ]
            """
            Extend with any built in fields and set embed's fields to the newly built list
            """
            embed_fields.extend(self.embed_info.fields)
            self.embed_info.fields = embed_fields

        def __init__(self, character: Character, **kwargs):
            super().__init__(character, **kwargs)
            self.character.refresh()
            StandaloneQueries.fetch_crafting_limit_row(self.character.id)

        def _skip_crafting(self):
            """
            Used to determine if the crafting menus should be displayed or not
            :return: bool - True to skip
            """
            try:
                limit = StandaloneQueries.crafting_limit(self.character.info.character_id, self.character.get_gold())
                jobs = [skill for skill in self.character.skills if skill.name in skill_info_interface.fetch_jobs()]
                available = (limit and any(jobs))
                log.info(f"_skip_crafting: Should skip crafting menu = '{not available}'")
                return not available
            except AttributeError:
                return True

        @textmenus.submenu("Create a mundane item", skip_if=_skip_crafting)
        async def craft_mundane(self, _):
            await workshop.mundane_crafting_menu(self.ctx, self.character)

        @textmenus.submenu("Experiment with Thaumstyn")
        async def craft_thaumstyn(self, _):
            await workshop.open_file_based_recipe_menu(self.ctx, 'thaumstyn', self.character)

        def _skip_craft_scroll(self):
            try:
                limit = StandaloneQueries.crafting_limit(self.character.info.character_id, self.character.get_gold())
                has_spellcaster_class = any(ClassRequirements.all_spellcaster_classes(self.character))
                available = (limit and has_spellcaster_class)
                return not available
            except AttributeError:
                return True

        @textmenus.submenu("Create a scroll")
        async def craft_scroll(self, _):
            await self.channel.send("New menu system not implemented for this menu yet. Displaying old one...")
            await OldWorkshopMenu.new_craft_scroll_menu(self.ctx, self.character)

        @textmenus.submenu("Work for someone this week")
        async def assign_labor(self, _):
            await self.channel.send("New menu system not implemented for this menu yet. Displaying old one...")
            await OldWorkshopMenu.work_menu(self.ctx.cog, self.ctx, self.ctx.author.id,
                                            self.character.info.character_id)

        def _skip_scribe(self):
            try:
                return not self.character.has_core_spellbook()
            except AttributeError:
                return True

        @textmenus.submenu("Scribe a spell into your spell book", skip_if=_skip_scribe)
        async def scribe_spell(self, payload):
            await self.channel.send("New menu system not implemented for this menu yet. Displaying old one...")
            payload_context = await self.bot.get_context(payload)
            await OldWorkshopMenu.scribe_spell_menu(self.ctx.cog, payload_context, self.ctx.author.id,
                                                    self.character.info.character_id)

    class MarketMenu(BaseCharacterMenu):
        """
        Market menu which allows players to buy and sell items with other players.
        """
        title = "Market"

        def get_initial_message(self):
            return "Welcome to the market."

        def update_embed(self):
            item_rows = StandaloneQueries.get_items_without_listed_auctions(self.character.id)
            items_str = ", ".join(f"{item.Quantity}x[**{item.Item}**]" for item in item_rows) if item_rows else "None"
            """
            Build fields list for the embed sent for this menu
            """
            embed_fields = [
                textmenus.EmbedInfo.Field("Name", self.character.name, inline=True),
                textmenus.EmbedInfo.Field("Gold", f"{self.character.get_gold():.2f}", inline=True),
                textmenus.EmbedInfo.Field("Inventory", items_str, inline=False)
            ]
            """
            Extend with any built in fields and set embed's fields to the newly built list
            """
            embed_fields.extend(self.embed_info.fields)
            self.embed_info.fields = embed_fields

        @textmenus.submenu('Buy items from the market')
        async def buy_item_menu(self, payload):
            await self.channel.send("New menu system not implemented for this menu yet. Displaying old one...")
            payload_context = await self.bot.get_context(payload)
            await OldMarketMenu.buy_menu(self.ctx.cog, payload_context, self.ctx.author.id, self.character.id)

        @textmenus.submenu('Sell items on the market')
        async def sell_item_menu(self, payload):
            await self.channel.send("New menu system not implemented for this menu yet. Displaying old one...")
            payload_context = await self.bot.get_context(payload)
            await OldMarketMenu.sell_menu(self.ctx.cog, payload_context, self.ctx.author.id, self.character.id)

        @textmenus.submenu('Stop selling an item')
        async def stop_sell_item_menu(self, payload):
            await self.channel.send("New menu system not implemented for this menu yet. Displaying old one...")
            payload_context = await self.bot.get_context(payload)
            await OldMarketMenu.stop_sell_menu(self.ctx.cog, payload_context, self.ctx.author.id, self.character.id)

        @textmenus.submenu('Give an item to another player')
        async def give_item_menu(self, payload):
            await self.channel.send("New menu system not implemented for this menu yet. Displaying old one...")
            payload_context = await self.bot.get_context(payload)
            await OldMarketMenu.give_menu(self.ctx.cog, payload_context, self.ctx.author.id, self.character.id)

        @textmenus.submenu('Give gold to another player')
        async def give_gold_menu(self, payload):
            await self.channel.send("New menu system not implemented for this menu yet. Displaying old one...")
            payload_context = await self.bot.get_context(payload)
            await OldMarketMenu.pay_menu(self.ctx.cog, payload_context, self.ctx.author.id, self.character.id)

        @textmenus.submenu('Recycle an item')
        async def recycle_menu(self, payload):
            await self.channel.send("New menu system not implemented for this menu yet. Displaying old one...")
            payload_context = await self.bot.get_context(payload)
            await OldMarketMenu.recycle_menu(self.ctx.cog, payload_context, self.ctx.author.id, self.character.id)

        def _skip_share_spellbook_spell(self):
            try:
                return not self.character.has_core_spellbook()
            except AttributeError:
                return True

        @textmenus.submenu('Share a spellbook spell with another player', skip_if=_skip_share_spellbook_spell)
        async def share_spell_menu(self, payload):
            await self.channel.send("New menu system not implemented for this menu yet. Displaying old one...")
            payload_context = await self.bot.get_context(payload)
            await OldMarketMenu.share_spell_menu(self.ctx.cog, payload_context, self.ctx.author.id, self.character.id)

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
        async def character_sheet(self, _):
            await start_menu(self.ctx, Menu.CharacterSheetMenu, character=self.character, stop_on_first=False)

        @textmenus.submenu('Workshop')
        async def workshop(self, _):
            await start_menu(self.ctx, Menu.WorkshopMenu, character=self.character, stop_on_first=False)

        @textmenus.submenu('Market')
        async def market(self, _):
            await start_menu(self.ctx, Menu.MarketMenu, character=self.character, stop_on_first=False)

    class CharacterChoiceMenu(BaseMenu):
        title = "Character Choice"
        character_info: CharacterInfo = None

        def get_initial_message(self):
            return "Welcome to the character select menu. Please select one of the characters below."

        def __init__(self, available_characters: List[CharacterInfo] = None, **kwargs):
            """
            Add a 'dynamic' submenu for each possible character and present menu to user.
            Accomplished by decorating a menu function to set that menu's character_info when selected.
            """
            super().__init__(**kwargs)
            if available_characters is None:
                available_characters = []
            for character_info in available_characters:
                self.submenu(label=character_info.name)(self.gen_set_character_info(character_info))

        @staticmethod
        def gen_set_character_info(character_info: CharacterInfo) -> \
                Callable[['Menu.CharacterChoiceMenu', discord.Message], Awaitable[None]]:
            """
            Creates a decorated closure function which sets the menu's selected character to the one passed
            :param character_info: character information to set when selected
            :return:
            """
            async def set_character_info(menu: Menu.CharacterChoiceMenu, _: discord.Message) -> None:
                log.debug("CharacterChoiceMenu::set_character_info")
                menu.character_info = character_info
                await menu.channel.send(f"You selected {menu.character_info.name}")
            return set_character_info

    @staticmethod
    async def select_character(ctx, author: discord.Member = None, channel: discord.abc.Messageable = None):
        """
        Fetches info for discord user. Returns id if available or will prompt user to select one from multiple.
        :param ctx: context of the command which called this
        :param author: discord.abc.User to fetch name of
        :param channel: channel to send response message
        :return: character_id
        """
        info_list = CharacterInfoFacade.interface.fetch_by_discord_id(author.id if author else ctx.message.author.id)
        if len(info_list) == 0:
            """No characters exist for the caller"""
            return None
        elif len(info_list) == 1:
            """Shortcut to return the only available character."""
            return info_list[0].character_id
        else:
            m = await start_menu(ctx, Menu.CharacterChoiceMenu, available_characters=info_list, channel=channel,
                                 author=author)
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
                channel = await menu_helper.get_channel(ctx)
                await channel.send("You are already accessing the menu.")
                return
            else:
                player_opened_menu = True
                self.players_in_menu[ctx.message.author.id] = None

            """
            Select character before accessing other menus
            """
            character_id = await self.select_character(ctx)
            if character_id is None:
                error_message = "You do not have a character which can access the menu. " \
                                "You will need to roll your stats and talk with a Mod to create your character. " \
                                "The 'randchar' command will randomly roll your characters stats. " \
                                "Once this is done, a Mod can use the 'Create' command to create your character."
                channel = await menu_helper.get_channel(ctx)
                await channel.send(error_message)
                return
            """
            Create menu and start querying the user
            """
            await start_menu(ctx, Menu.MainMenu, character=Character(character_id), stop_on_first=False)
        except textmenus.StopException:
            reason = "'stop' received"
        except textmenus.ExitException:
            reason = "'exit' received"
        except asyncio.TimeoutError:
            reason = "Timeout occurred"
        finally:
            channel = await menu_helper.get_channel(ctx)
            await channel.send(f"{reason}. Closing menu.")
            """
            Remove player from list when they leave
            """
            if player_opened_menu:
                self.players_in_menu.pop(ctx.message.author.id)

    """
    Define methods needed for 'old' menus.
    """
    @staticmethod
    async def confirm(ctx):
        m = await start_menu(ctx, ConfirmMenu, message="Would you like to confirm your choice?")
        return "Yes" if m.confirm else "No"

    @staticmethod
    async def answer_from_list(ctx, question, option_list):
        if len(option_list) == 0:
            channel = await menu_helper.get_channel(ctx)
            await channel.send("No options available. Stopping. "
                               "[This could be due to not knowing a spell, meeting the minimum crafting limit, etc.]")
            raise Exceptions.StopException
        choices = dict(message=question, choices=option_list, title='Select From List', should_raise_stop=True)
        m = await start_menu(ctx, ListMenu, **choices)
        return m.choice

    async def answer_with_int_number(self, ctx, question, maximum):
        member = ctx.message.author
        channel = await menu_helper.get_channel(ctx)
        await member.send(f"{question}")

        # setup sub function to do checks the returned message is from the user in private messages
        def wait_for_reply(message: discord.Message):
            if member.id != message.author.id or channel.id != message.channel.id:
                return False
            return True

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=wait_for_reply)
            except asyncio.TimeoutError:
                await channel.send(f"Timed out, aborting...")
                raise Exceptions.ExitException
            if msg.content.lower() == "exit":
                await channel.send(f"Exit received. Exiting...")
                raise Exceptions.ExitException
            if msg.content.lower() == "stop":
                await channel.send(f"Stop received. Stopping...")
                raise Exceptions.StopException
            # check they picked an answer
            try:
                answer = int(msg.content)
                if answer < 1: await member.send(f"Please enter a number between 1 and {maximum}")
                elif answer <= maximum: return answer
                else: await member.send(f"Please enter a number between 1 and {maximum}")
            except ValueError:
                await member.send(f"{msg.content} is not a number, Please enter a number between 1 and {maximum}")

    async def answer_with_float_number(self, ctx, question, maximum):
        member = ctx.message.author
        channel = await menu_helper.get_channel(ctx)
        await member.send(f"{question}")

        # setup sub function to do checks the returned message is from the user in private messages
        def wait_for_reply(message: discord.Message):
            return False if member.id != message.author.id and channel.id != message.channel.id else True

        while True:
            # run the check until 60 seconds has elapsed or player types EXIT
            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=wait_for_reply)
            except asyncio.TimeoutError:
                await channel.send(f"Timed out, aborting...")
                raise Exceptions.ExitException
            if msg.content.lower() == "exit":
                await channel.send(f"Exit received. Exiting...")
                raise Exceptions.ExitException
            if msg.content.lower() == "stop":
                await channel.send(f"Stop received. Stopping...")
                raise Exceptions.StopException
            # check they picked an answer
            try:
                answer = float(msg.content)
                if answer < 0: await member.send(f"Please enter a number between 0 and {maximum}")
                elif answer <= maximum: return answer
                else: await member.send(f"Please enter a number between 1 and {maximum}")
            except ValueError:
                await member.send(f"{msg.content} is not a number, Please enter a number between 1 and {maximum}")

    async def answer_with_statement(self, ctx):
        member = ctx.message.author
        channel = await menu_helper.get_channel(ctx)

        # check author
        def wait_for_reply(message: discord.Message):
            return False if member.id != message.author.id and channel.id != message.channel.id else True

        # send the user the message
        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=wait_for_reply)
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

    async def character_name_lookup(self, command, question, character_id):
        await command.message.author.send(question)

        def check_reply(user_response):
            return user_response.author == command.author and user_response.channel.type[1] == 1

        character_info = CharacterInfoFacade.interface.fetch(character_id)
        while True:
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check_reply)
            except asyncio.TimeoutError:
                return "exit"

            if msg.content.lower() == "exit":
                return "exit"
            elif msg.content.lower() == "stop":
                return "stop"
            elif msg.content.lower() == character_info.name.lower():
                await command.message.author.send("You cannot give yourself an item")
            elif CharacterInfoFacade.interface.fetch_by_character_name(msg.content.lower()) is not None:
                return msg.content.lower()
            else:
                await command.message.author.send("{} is not a character, please "
                                                  "confirm the spelling and try again".format(msg.content.lower()))

def setup(bot):
    bot.add_cog(Menu(bot))
