import config
import logging
from Character.Data.CharacterInfo import CharacterInfo
log = logging.getLogger(__name__)


max_number_of_classes = 3

class DndClass:
    def __init__(self, name, stat_req, subclass_lvl=3, prepare_spells=False,
                 spells_memorized=False, has_spellbook=False):
        self.ability_score_requirement = 13
        self.name = name
        self.stats_required = stat_req
        self.subclass_lvl = subclass_lvl
        self.prepare_spells = prepare_spells
        self.spells_memorized = spells_memorized
        self._has_spellbook = has_spellbook

    def meet_ability_score_requirement(self, character_info: CharacterInfo):
        results = []
        for stat in self.stats_required:
            # TODO: Handle 'stat1' or 'stat2' requirements for blood hunter
            stat_value = getattr(character_info, stat)
            results.append(stat_value >= self.ability_score_requirement)
        return all(results)

    def are_spells_memorized(self):
        return self.spells_memorized

    def are_spells_prepared(self):
        return self.prepare_spells

    def has_spellbook(self):
        return self._has_spellbook

    def is_spellcaster(self):
        return self.are_spells_prepared() or self.are_spells_memorized() or self.has_spellbook()


# Class,Sub_Class_Level,All_Spells_known
# -----,---------------,----------------
# Artificer,3,1
# Barbarian,3,0
# Bard,3,0
# Blood Hunter,3,0
# Cleric,1,1
# Druid,2,1
# Fighter,3,0
# Monk,3,0
# Paladin,3,1
# Ranger,3,0
# Rogue,3,0
# Sorcerer,1,0
# Warlock,1,0
# Wizard,2,0
# classes_which_learn_spells =
# ['Bard', 'Blood Hunter', 'Fighter', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock']

class_definitions = {
    DndClass("Artificer", stat_req=['int'], prepare_spells=True),
    DndClass("Barbarian", stat_req=['str']),
    DndClass("Bard", stat_req=['cha'], spells_memorized=True),
    DndClass("Cleric", stat_req=['wis'], subclass_lvl=1, prepare_spells=True),
    DndClass("Druid", stat_req=['wis'], subclass_lvl=2, prepare_spells=True),
    DndClass("Fighter", stat_req=['str', 'dex'], spells_memorized=True),
    DndClass("Monk", stat_req=['dex', 'wis']),
    DndClass("Paladin", stat_req=['str', 'cha'], prepare_spells=True),
    DndClass("Ranger", stat_req=['dex', 'wis'], spells_memorized=True),
    DndClass("Rogue", stat_req=['dex'], spells_memorized=True),
    DndClass("Sorcerer", stat_req=['cha'], subclass_lvl=1, spells_memorized=True),
    DndClass("Warlock", stat_req=['cha'], subclass_lvl=1, spells_memorized=True),
    DndClass("Wizard", stat_req=['int'], subclass_lvl=2, has_spellbook=True)
}


class_lookup = {c.name: c for c in class_definitions if c.name in config.available_classes}

def get_dnd_class_definition(class_name: str) -> DndClass:
    return class_lookup[class_name]

def classes_available_for_levelup(character):
    """
    Returns set of classes available for leveling. Will only return current classes if at max count.
    Otherwise, it will return a set of current classes and classes which character meets requirements.
    """
    if len(character.classes) >= max_number_of_classes:
        return character.classes.keys()
    class_set = {c for c in character.classes.keys()}
    class_set.update({k for k, v in class_lookup.items() if v.meet_ability_score_requirement(character.info)})
    return sorted(class_set)

def classes_available_for_subclass(character):
    return [k for k, v in character.classes.items() if v.meet_subclass_requirement()]

def all_spellcaster_classes(character):
    return [v for k, v in character.classes.items() if v.class_info.is_spellcaster()]
