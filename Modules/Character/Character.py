import Character.CharacterInfoFacade as CharacterInfoFacade
import Character.CharacterClassFacade as CharacterClassFacade
import Character.CharacterFeatFacade as CharacterFeatFacade
import Character.CharacterSkillFacade as CharacterSkillFacade
import Character.CharacterItemFacade as CharacterItemFacade
from Character.Data.CharacterItem import CharacterItem


class Character:

    def __init__(self, character_id: str):
        self.info = CharacterInfoFacade.interface.fetch(character_id)
        self.classes = CharacterClassFacade.interface.fetch(character_id)
        self.feats = CharacterFeatFacade.interface.fetch(character_id)
        self.skills = CharacterSkillFacade.interface.fetch(character_id)
        # self.items = CharacterItemFacade.interface.fetch(character_id)
        self.items = {i.name: i for i in CharacterItemFacade.interface.fetch(character_id)}

    def has_class(self, name: str):
        return any(c for c in self.classes if c.name == name)

    def has_subclass(self, sub_class: str):
        return any(c for c in self.classes if c.sub_class == sub_class)

    def has_feat(self, name: str):
        return any(f for f in self.feats if f.name == name)

    def has_skill(self, name: str):
        return any(s for s in self.skills if s.name == name)

    def has_skill_proficiency(self, name: str):
        return any(s for s in self.skills if s.name == name and s.proficiency >= 0)

    def has_item(self, name: str):
        return True if name in self.items else False

    def has_item_quantity(self, name: str, quantity: int):
        return True if (name in self.items) and (self.items[name].quantity >= quantity) else False

    def has_item_quantity_by_keyword(self, **kwargs):
        # Check gold
        if "Gold" in kwargs:
            if self.get_gold() < kwargs.pop("Gold"):
                return False
        # Check remaining items
        matches = {k: v for k, v in kwargs.items() if (k in self.items) and (self.items[k].quantity >= v)}
        return len(kwargs) == len(matches)

    def get_character_level(self):
        return sum(c.level for c in self.classes)

    def can_level_up(self):
        raise NotImplemented("XP info not implemented yet")

    def get_gold(self):
        return self.info.gold

    def set_item_amount(self, name: str, amount: int):
        if amount < 0:
            raise ValueError("set_item_amount does not support negative amounts")
        elif amount == 0:
            return self.remove_item(name)

        if name in self.items:
            item = self.items[name]
            item.quantity += amount
            CharacterItemFacade.interface.update(item)
        else:
            item = CharacterItem(character_id=self.info.character_id, name=name, quantity=amount)
            self.items[name] = item
            CharacterItemFacade.interface.insert(item)

    def modify_item_amount(self, name: str, amount):
        if name == "Gold":
            new_quantity = self.info.gold + amount
            if new_quantity >= 0:
                self.info.gold += amount
                CharacterInfoFacade.interface.update(self.info)
            else:
                raise RuntimeError("modify_item_amount cannot remove gold due to lack of quantity. {} > {}"
                                   .format(amount, self.info.gold))
        elif name in self.items:
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
