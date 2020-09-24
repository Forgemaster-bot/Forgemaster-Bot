from Character.Data.SpellHolder import SpellHolder
from Character.CharacterSpellFacade import interface as spell_interface
from Character.SpellbookFacade import interface as spellbook_interface
from Character.LinkClassSpellFacade import interface as link_class_spell_interface
import Character.ClassRequirements as ClassRequirements
import cogs.utils.StandaloneQueries as StandaloneQueries


class CharacterClass:
    __slots__ = ["character_id", "name", "level", "number", "subclass",
                 "free_book_spells", "can_replace_spells", "has_class_choice",
                 "spell_holders", "class_info"]

    def __init__(self, character_id=None, name=None, level=None, number=None, subclass=None,
                 free_book_spells=None, can_replace_spells=None, has_class_choice=None):
        self.character_id = character_id
        self.name = name
        self.level = level
        self.number = number
        self.subclass = subclass
        self.free_book_spells = free_book_spells
        self.can_replace_spells = can_replace_spells
        self.has_class_choice = has_class_choice
        self.class_info = ClassRequirements.get_dnd_class_definition(self.name)
        self.spell_holders = None
        self.refresh()

    def to_dict(self) -> dict:
        """
        Helper function to convert this classes enumerated fields to a dictionary of key:value. Where:
            - key = Attribute **Name**
            - value = Attribute **Value**
        :return: [dict] dictionary of enumerated fields
        """
        return {s: getattr(self, s, None) for s in self.__slots__}

    def __str__(self):
        if self.subclass is None:
            return "{}: {}".format(self.name, self.level)
        else:
            return "{} {}: {}".format(self.subclass, self.name, self.level)

    def _get_spell_holder(self):
        if self.character_id and self.class_info:
            if self.class_info.has_spellbook():
                return {sb.name: sb for sb in spellbook_interface.fetch_by_character_id(self.character_id)}
            else:
                spell_holders = {}
                key = [self.character_id, self.name]
                spell_holders[self.name] = SpellHolder(name=self.name, interface=spell_interface, key=key)
                if self.subclass:
                    key = [self.character_id, self.subclass]
                    spell_holders[self.subclass] = SpellHolder(name=self.subclass, interface=spell_interface, key=key)
                return spell_holders

    def refresh(self):
        self.spell_holders = self._get_spell_holder()

    def subclass_is_picked(self):
        return False if self.subclass is None else True

    def subclass_not_picked(self):
        return not self.subclass_is_picked()

    def insert_spell(self, spell):
        if self.class_info.has_spellbook():
            core_spellbooks = [holder for holder in self.spell_holders.values() if holder.type == 'Core']
            holder = core_spellbooks[0]
        else:
            holder = self.spell_holders[spell.class_name]
        holder.insert_spell(character_id=self.character_id, name=spell.spell_name, origin=holder.name)

    def remove_spell(self, spell):
        spell_interface.delete(spell)
        self.refresh()

    def meet_subclass_requirement(self):
        return self.subclass_not_picked() and (self.level >= self.class_info.subclass_lvl)

    def get_num_spells(self):
        return sum(len(holder.spells) for holder in self.spell_holders.values())

    def can_learn_spell(self) -> bool:
        if self.class_info.is_spellcaster():
            if self.name == 'Wizard':
                return self.free_book_spells > 0
            else:
                return StandaloneQueries.max_spells_known_per_level(self) > self.get_num_spells()
        return False

    def filter_available_spells(self, spell_list):
        for holder in self.spell_holders.values():
            for spell in holder.spells:
                spell_list.pop(spell.name, None)
        return spell_list

    def available_class_spells(self):
        return link_class_spell_interface.fetch(self.name)

    def available_subclass_spells(self):
        spells = link_class_spell_interface.fetch(self.subclass)

        if self.subclass.startswith('School of Theurgy'):
            # Check if wizard 'School of Theurgy' subclass, and add cleric spells if domain is covered
            avail_domain_spells = self.filter_spell_list(spells)
            spells = link_class_spell_interface.fetch('Cleric') if not avail_domain_spells else spells

        # Select spell slot level
        return spells

    def get_spells(self):
        spells = []
        for holder in self.spell_holders.values():
            for spell in holder.spells:
                spells.append(spell)
        return spells

    def set_subclass(self, subclass_name):
        self.subclass = subclass_name
        self.has_class_choice = ClassRequirements.has_class_choice(self.name, self.subclass)

    @staticmethod
    def get_dnd_class(class_name):
        return ClassRequirements.get_dnd_class_definition(class_name)