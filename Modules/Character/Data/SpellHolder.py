
from Character.Data.CharacterSpell import CharacterSpell

class SpellHolder:
    def __init__(self, name, interface, key):
        self.name = name
        self.interface = interface
        self.key = key
        self.spells = None
        self.refresh_spells()

    def refresh_spells(self):
        self.spells = sorted(self.interface.fetch(*self.key), key=lambda spell: spell.spell_info.level)

    def insert_spell_obj(self, spell_obj):
        matching_spells = [s for s in self.spells if spell_obj.name == s.name]
        if any(matching_spells):
            raise RuntimeError(f"Can't insert already known spell {spell_obj.name} into {self.name}")
        self.interface.insert(spell_obj)
        self.refresh_spells()

    def insert_spell(self, character_id, name, origin, **kwargs):
        spell_obj = CharacterSpell(character_id=character_id, name=name, origin=origin)
        self.insert_spell_obj(spell_obj)
