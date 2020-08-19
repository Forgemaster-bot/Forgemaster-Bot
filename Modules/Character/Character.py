import Character.CharacterInfoFacade as CharacterInfoFacade
import Character.CharacterClassFacade as CharacterClassFacade
import Character.CharacterFeatFacade as CharacterFeatFacade
import Character.CharacterSkillFacade as CharacterSkillFacade
import Character.CharacterItemFacade as CharacterItemFacade


class Character:
    owner_id = None
    info = None
    classes = None
    feats = None
    skills = None
    items = None

    def __init__(self, character_id: str):
        self.info = CharacterInfoFacade.interface.fetch(character_id)
        self.classes = CharacterClassFacade.interface.fetch(character_id)
        self.feats = CharacterFeatFacade.interface.fetch(character_id)
        self.skills = CharacterSkillFacade.interface.fetch(character_id)
        self.items = CharacterItemFacade.interface.fetch(character_id)

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
        return any(i for i in self.items if i.name == name)

    def has_item_quantity(self, name: str, quantity: int):
        return any(i for i in self.items if i.name == name and i.quantity >= quantity)

    def has_item_quantity_by_keyword(self, **kwargs):
        matches = {i.name: i.quantity for i in self.items if (i.name in kwargs) and (i.quantity >= kwargs[i.name])}
        return len(kwargs) == len(matches)

    def get_character_level(self):
        return sum(c.level for c in self.classes)

    def can_level_up(self):
        raise NotImplemented("XP info not implemented yet")
