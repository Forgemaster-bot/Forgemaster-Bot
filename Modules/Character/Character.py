import math
import Quick_Python
import Character.Data.LevelExperience as LevelExperience
import Character.CharacterInfoFacade as CharacterInfoFacade
import Character.CharacterClassFacade as CharacterClassFacade
import Character.CharacterFeatFacade as CharacterFeatFacade
import Character.CharacterSkillFacade as CharacterSkillFacade
import Character.CharacterItemFacade as CharacterItemFacade
from Character.Data.CharacterItem import CharacterItem
from Connections import RosterColumns


class Character:

    def __init__(self, character_id: str):
        self.info = CharacterInfoFacade.interface.fetch(character_id)
        self.classes = CharacterClassFacade.interface.fetch(character_id)
        self.feats = CharacterFeatFacade.interface.fetch(character_id)
        self.skills = CharacterSkillFacade.interface.fetch(character_id)
        self.items = {i.name: i for i in CharacterItemFacade.interface.fetch(character_id)}

    def refresh_info(self):
        self.info = CharacterInfoFacade.interface.fetch(self.info.character_id)

    def refresh_items(self):
        self.items = {i.name: i for i in CharacterItemFacade.interface.fetch(self.info.character_id)}

    def has_class(self, name: str):
        return any(c for c in self.classes if c.name.lower() == name.lower())

    def has_either_class(self, *args):
        names = [name.lower() for name in args]
        return any(c for c in self.classes if c.name in names)

    def has_subclass(self, sub_class: str):
        return any(c for c in self.classes if c.sub_class.lower() == sub_class.lower())

    def has_feat(self, name: str):
        return any(f for f in self.feats if f.name.lower() == name.lower())

    def has_skill(self, name: str):
        return any(s for s in self.skills if s.name.lower() == name.lower())

    def has_skill_proficiency(self, name: str):
        return any(s for s in self.skills if s.name.lower() == name.lower() and s.proficiency >= 0)

    def has_item(self, name: str):
        return True if (name in self.items) and (self.items[name].quantity > 0) else False

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
        return sum(c.level for c in self.classes)

    def get_xp(self):
        return self.info.xp

    def can_level_up(self):
        return LevelExperience.can_level_up(self.get_character_level(), self.get_xp())

    def get_gold(self):
        self.refresh_info()
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
        return Quick_Python.labelled_list("Classes", self.classes)

    def formatted_feats(self) -> str:
        return Quick_Python.labelled_list("Feats", self.feats)

    def formatted_skills(self) -> str:
        return Quick_Python.labelled_list("Skills", self.skills)

    def formatted_items(self) -> str:
        return Quick_Python.labelled_list("Items", list(self.items.values()))

    def formatted_character_info(self):
        info_list = [
            self.formatted_name(),
            self.formatted_stats(),
            self.formatted_xp(),
            self.formatted_classes(),
            self.formatted_feats(),
            self.formatted_skills(),
            self.formatted_gold(),
            self.formatted_items()
        ]
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
            RosterColumns.CLASS_1: self.classes[0] if 0 < len(self.classes) else None,
            RosterColumns.CLASS_2: self.classes[1] if 1 < len(self.classes) else None,
            RosterColumns.CLASS_3: self.classes[2] if 2 < len(self.classes) else None,
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
