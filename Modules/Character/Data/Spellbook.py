from typing import List
from Character.Data.SpellbookSpell import SpellbookSpell
from Character.SpellbookSpellFacade import interface as spell_interface
from Character.Data.SpellHolder import SpellHolder
from cogs.utils import StandaloneQueries

class Spellbook(SpellHolder):
    __slots__ = ["spellbook_id", "character_id", "name", "type"]

    def __init__(self, spellbook_id=None, character_id=None, name=None, type=None):
        self.spellbook_id = spellbook_id
        self.character_id = character_id
        self.name = name
        self.type = type
        super().__init__(name=self.name, interface=spell_interface, key=[self.spellbook_id])

    def to_dict(self) -> dict:
        """
        Helper function to convert this classes enumerated fields to a dictionary of key:value. Where:
            - key = Attribute **Name**
            - value = Attribute **Value**
        :return: [dict] dictionary of enumerated fields
        """
        return {s: getattr(self, s, None) for s in self.__slots__}

    def __str__(self):
        return f"{self.name}"

    def refresh(self):
        self.spell_holder.refresh_spells()

    @staticmethod
    def get_suffix():
        return "Spell book"

    def insert_spell(self, name, **kwargs):
        spell_obj = SpellbookSpell(spellbook_id=self.spellbook_id, name=name, is_known=True)
        self.insert_spell_obj(spell_obj)
        StandaloneQueries.modify_free_spellbook_spells(self.character_id, kwargs['parent'], -1)
