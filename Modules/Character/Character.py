import math
import logging
from typing import Dict

import Quick_Python
import Character.Data.LevelExperience as LevelExperience
import Character.CharacterInfoFacade as CharacterInfoFacade
from Character.CharacterClassFacade import interface as CharacterClassInterface
import Character.CharacterFeatFacade as CharacterFeatFacade
import Character.CharacterSkillFacade as CharacterSkillFacade
import Character.CharacterItemFacade as CharacterItemFacade
import Character.SpellbookFacade as SpellbookFacade
import Character.SkillInfoFacade as SkillInfoFacade
from Character.Data.CharacterItem import CharacterItem
from Character.Data.CharacterClass import CharacterClass
from Character.Data.CharacterSkill import CharacterSkill
from Character.Data.Spellbook import Spellbook
from Character.Data.SkillInfo import SkillInfo
from Connections import RosterColumns, log_to_discord
import config

from cogs.utils import StandaloneQueries
# import Update_Google_Roster as Roster

log = logging.getLogger(__name__)

class Character:

    def __init__(self, character_id: str):
        self.info = CharacterInfoFacade.interface.fetch(character_id)
        self.classes: Dict[str, CharacterClass] = {c.name: c for c in CharacterClassInterface.fetch(character_id)}
        self.feats = CharacterFeatFacade.interface.fetch(character_id)
        self.skills = CharacterSkillFacade.interface.fetch(character_id)
        self.items = {i.name: i for i in CharacterItemFacade.interface.fetch(character_id)}
        self.core_spellbook_check()

    def refresh_info(self):
        self.info = CharacterInfoFacade.interface.fetch(self.info.character_id)

    def refresh_items(self):
        self.items = {i.name: i for i in CharacterItemFacade.interface.fetch(self.info.character_id)}

    def has_class(self, name: str):
        return any(c for c in self.classes.values() if c.name.lower() == name.lower())

    def has_either_class(self, *args):
        names = [name.lower() for name in args]
        return any(k for k in self.classes.keys() if k.lower() in names)

    def has_subclass(self, sub_class: str):
        return any(c for c in self.classes.values() if c.subclass.lower() == sub_class.lower())

    def can_pick_subclass(self):
        return any(c.subclass_not_picked() for c in self.classes.values())

    def has_subclass_choice(self, sub_class: str):
        for character_class in self.classes.values():
            if character_class.subclass and character_class.subclass.lower() == sub_class.lower():
                return False if character_class.has_class_choice is None else character_class.has_class_choice
        return False

    def has_feat(self, name: str):
        return any(f for f in self.feats if f.name.lower() == name.lower())

    def has_skill(self, name: str):
        return any(s for s in self.skills if s.name.lower() == name.lower())

    def has_skill_proficiency(self, name: str):
        return any(s for s in self.skills if s.name.lower() == name.lower() and s.proficiency >= 0)

    def has_item(self, name: str):
        # if lower:
        if any([key for key, value in self.items.items() if key.lower() == name.lower() and value.quantity > 0]):
            return True
        return False
        # return True if (name in self.items) and (self.items[name].quantity > 0) else False

    def has_item_quantity(self, name: str, quantity: int):
        return True if (name in self.items) and (self.items[name].quantity >= quantity) else False

    def has_level(self, level: int):
        return True if (self.get_character_level() >= level) else False

    def has_item_quantity_by_keyword(self, **kwargs):
        # Check gold
        if "Gold" in kwargs:
            self.refresh_info()
            if self.get_gold() < kwargs.pop("Gold"):
                return False
        # Check remaining items
        self.refresh_items()
        matches = {k: v for k, v in kwargs.items() if (k in self.items) and (self.items[k].quantity >= v)}
        return len(kwargs) == len(matches)

    def get_character_level(self):
        return sum(c.level for c in self.classes.values())

    def get_xp(self):
        return self.info.xp

    def can_level_up(self):
        character_level = self.get_character_level()
        xp = self.get_xp()
        can_level = LevelExperience.can_level_up(self.get_character_level(), self.get_xp())
        log.debug(f"level: {character_level}; xp: {xp}; can_level: {can_level}")
        return can_level

    def get_gold(self):
        return self.info.gold

    def set_item_amount(self, name: str, amount: int):
        if amount < 0:
            raise ValueError("set_item_amount does not support negative amounts")
        elif amount == 0:
            return self.remove_item(name)

        if name in self.items:
            item = self.items[name]
            item.quantity = amount
            CharacterItemFacade.interface.update(item)
        else:
            item = CharacterItem(character_id=self.info.character_id, name=name, quantity=amount)
            self.items[name] = item
            CharacterItemFacade.interface.insert(item)

    def modify_item_amount(self, name: str, amount):
        if name == "Gold":
            self.refresh_info()
            new_quantity = self.info.gold + amount
            if new_quantity >= 0:
                self.info.gold += amount
                CharacterInfoFacade.interface.update(self.info)
                return
            else:
                raise RuntimeError("modify_item_amount cannot remove gold due to lack of quantity. {} > {}"
                                   .format(amount, self.info.gold))

        self.refresh_items()
        if name in self.items:
            # update existing quantity if item already exists
            item = self.items[name]
            new_quantity = item.quantity + amount
            if new_quantity > 0:
                # update counts
                item.quantity += amount
                CharacterItemFacade.interface.update(item)
            elif new_quantity == 0:
                # remove item
                self.remove_item(name)
            else:
                # error: don't have enough
                raise RuntimeError("modify_item_amount cannot remove[{}] more than available[{}]"
                                   .format(amount, item.quantity))
        elif amount > 0:
            # insert item
            item = CharacterItem(character_id=self.info.character_id, name=name, quantity=amount)
            self.items[name] = item
            CharacterItemFacade.interface.insert(item)
        else:
            # cannot add item with zero or less than zero count
            raise RuntimeError("Cannot add negative or zero amount if character does not have item {}".format(name))

    def remove_item_amount(self, name: str, amount: int):
        if amount < 0:
            raise ValueError("Cannot remove negative amount: {}:{}".format(name, amount))
        self.modify_item_amount(name, amount*(-1))

    def remove_item(self, name: str):
        if name in self.items:
            item = self.items.pop(name)
            CharacterItemFacade.interface.delete(item)

    def refresh(self):
        self.__init__(self.info.character_id)

    def formatted_name(self) -> str:
        return Quick_Python.labelled_str("Name", self.info.formatted_name())

    def formatted_stats(self) -> str:
        return Quick_Python.labelled_str("Stats", self.info.formatted_stats())

    def formatted_gold(self) -> str:
        return Quick_Python.labelled_str("Gold", self.info.formatted_gold())

    def formatted_xp(self) -> str:
        return Quick_Python.labelled_str("XP", self.info.formatted_xp())

    def formatted_classes(self) -> str:
        return Quick_Python.labelled_list("Classes", list(self.classes.keys()))

    def formatted_feats(self) -> str:
        return Quick_Python.labelled_list("Feats", self.feats)

    def formatted_skills(self) -> str:
        return Quick_Python.labelled_list("Skills", self.skills)

    def formatted_items(self) -> str:
        return Quick_Python.labelled_list("Items", list(self.items.values()))

    def get_formatted_character_info_list(self):
        return [
            self.formatted_name(),
            self.formatted_xp(),
            self.formatted_gold(),
            self.formatted_stats(),
            self.formatted_classes(),
            self.formatted_feats(),
            self.formatted_skills(),
            self.formatted_items()
        ]

    def formatted_character_info(self):
        info_list = self.get_formatted_character_info_list()
        return "\n".join(info_list)

    def item_list_as_str(self):
        return Quick_Python.list_to_string(list(self.items.values()))

    def item_list_as_roster_str(self):
        return Quick_Python.list_to_string([item.roster_str() for item in self.items.values()])

    def feat_list_as_str(self):
        return Quick_Python.list_to_string(self.feats)

    def skills_list_as_str(self):
        return Quick_Python.list_to_string(self.skills)

    def get_roster_data(self):
        # list = [None] * (RosterColumns.END-1)
        roster_dict = {
            RosterColumns.DISCORD_NAME: Quick_Python.lookup_player_name_by_id(self.info.discord_id),
            RosterColumns.CHARACTER_NAME: self.info.name,
            RosterColumns.RACE: self.info.race,
            RosterColumns.BACKGROUND: self.info.background,
            RosterColumns.CLASS_1: list(self.classes.values())[0] if 0 < len(self.classes) else None,
            RosterColumns.CLASS_2: list(self.classes.values())[1] if 1 < len(self.classes) else None,
            RosterColumns.CLASS_3: list(self.classes.values())[2] if 2 < len(self.classes) else None,
            RosterColumns.EXPERIENCE: self.info.xp,
            RosterColumns.LEVEL: self.get_character_level(),
            RosterColumns.LEVELUP: self.can_level_up(),
            RosterColumns.STR: self.info.str,
            RosterColumns.DEX: self.info.dex,
            RosterColumns.CON: self.info.con,
            RosterColumns.INT: self.info.int,
            RosterColumns.WIS: self.info.wis,
            RosterColumns.CHA: self.info.cha,
            RosterColumns.GOLD: self.info.gold,
            RosterColumns.FEATS: self.feat_list_as_str(),
            RosterColumns.SKILLS: self.skills_list_as_str(),
            RosterColumns.ITEMS: self.item_list_as_roster_str()
        }
        return roster_dict

    def get_proficiency_bonus(self):
        return math.ciel(self.get_character_level() * (1 / 4)) + 1

    def get_skills_dict(self):
        return {s.name: s for s in self.skills}

    def get_class_dict(self):
        return self.classes

    async def level_up(self, class_name, cog=None, channel=None):
        classes = self.get_class_dict()

        if class_name in classes.keys():
            is_first_level = False
            class_obj = classes[class_name]
            class_obj.level += 1
            class_obj.can_replace_spells = class_obj.class_info.are_spells_memorized()
        else:
            # get_dnd_class
            is_first_level = True
            class_obj = CharacterClass()
            class_obj.character_id = self.info.character_id
            class_obj.name = class_name
            class_obj.level = 1
            class_obj.number = max([c.number for c in self.classes.values()]) + 1
            class_obj.can_replace_spells = CharacterClass.get_dnd_class(class_name).are_spells_memorized()
            class_obj.free_book_spells = 0

        if class_name == 'Wizard':
            additional_slots = 6 if is_first_level else 2
            class_obj.free_book_spells += additional_slots
            # TODO: Spell book

        if is_first_level:
            self.classes[class_obj.name] = class_obj
            CharacterClassInterface.insert(class_obj)
        else:
            CharacterClassInterface.update(class_obj)
        self.refresh()
        """
        Check if player unlocks a new character
        """
        try:
            additional_character_level = config.additional_character_level
            additional_character_num = config.additional_character_num
            current_level = self.get_character_level()
            if current_level == additional_character_level:
                log.info(f"{self.name} leveled up to {current_level} and unlocked an additional character.")
                StandaloneQueries.update_player_character_total(self.info.discord_id, additional_character_num)
                if cog and channel:
                    msg = f"{self.info.name} has unlocked a new character slot for reaching level {current_level}!"
                    await log_to_discord(cog, msg)
                    await channel.send(msg)
        except KeyError:
            log.info(f"{self.name} leveled up, but skipping character total check as keys are not in bot config file.")
            pass

    def set_subclass(self, class_name, subclass_name):
        self.classes[class_name].set_subclass(subclass_name)
        CharacterClassInterface.update(self.classes[class_name])

    # def has_spellbook(self):
    #     return False if not self.spellbook else True
    #
    # def get_spellbooks(self):
    #     return self.spellbooks

    def get_spellbook_name(self):
        return f"{self.info.name} {Spellbook.get_suffix()}"

    def get_core_spellbook(self):
        return self.classes['Wizard'].spell_holders[self.get_spellbook_name()]

    def has_core_spellbook(self):
        try:
            return self.get_core_spellbook() is not None
        except KeyError as err:
            return False

    def insert_core_spellbook(self):
        book = Spellbook(character_id=self.info.character_id, name=self.get_spellbook_name(), type='Core')
        SpellbookFacade.interface.insert(book)
        self.refresh()

    def core_spellbook_check(self):
        if 'Wizard' in self.classes:
            if not self.has_core_spellbook():
                self.insert_core_spellbook()

    # TODO: Book of Shadows
    # def get_tome_spellbook(self):
    # def has_tome_spellbook(self):
    # def insert_tome_spellbook(self):

    def insert_spellbook(self, book_type: str):
        book = Spellbook(character_id=self.info.character_id, name=self.get_spellbook_name(), type=book_type)
        SpellbookFacade.interface.insert(book)
        self.refresh()

    @staticmethod
    def filter_spell_list(spell_list, spells_holder):
        """
        Spellholder can be classes or spellbooks for example
        :param spell_list:
        :param spells_holder:
        :return:
        """
        if isinstance(spells_holder, dict):
            for holder in spells_holder.values():
                for spell in holder.spells:
                    spell_list.pop(spell.name, None)
        elif isinstance(spells_holder, list):
            for holder in spells_holder:
                for spell in holder.spells:
                    spell_list.pop(spell.name, None)
        else:
            for spell in spells_holder.spells:
                spell_list.pop(spell.name, None)
        return spell_list

    async def forget_spell(self, character_class, spell, cog=None, channel=None):
        if isinstance(character_class, str):
            character_class = self.classes[character_class]
        character_class.remove_spell(spell)
        character_class.can_replace_spells = False
        CharacterClassInterface.update(character_class)
        if cog and channel:
            msg = f"{self.info.name} has successfully forgot the spell **{str(spell)}**'!"
            await log_to_discord(cog, msg)
            await channel.send(msg)

    async def learn_spell(self, character_class: CharacterClass, spell, cog=None, channel=None):
        if isinstance(character_class, str):
            character_class = self.classes[character_class]
        character_class.insert_spell(spell)
        if cog and channel:
            msg = f"{self.info.name} has successfully learned the spell **{spell.spell_name}**, " \
                  f"originating from '**{spell.class_name}**'!"
            await log_to_discord(cog, msg)
            await channel.send(msg)

    async def learn_skill(self, skill: SkillInfo, has_proficiency: bool = False):
        if skill.name not in self.get_skills_dict():
            character_skill = CharacterSkill(character_id=self.id, name=skill.name, proficiency=has_proficiency)
            CharacterSkillFacade.interface.insert(character_skill)
            self.refresh()

    def update_class_choice(self, character_class: CharacterClass, is_used: bool):
        if isinstance(character_class, str):
            character_class = self.classes[character_class]
        character_class.has_class_choice = is_used
        CharacterClassInterface.update(character_class)

    @property
    def id(self):
        return self.info.character_id

    @property
    def name(self):
        return self.info.name
