import Character.Tables.SpellbookSpellMapper as SpellbookSpellMapper
from Character.Data.SpellbookSpell import SpellbookSpell
from typing import List


class SpellbookSpellFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, mapper):
        self._mapper = mapper

    def fetch(self, spellbook_id: str) -> List[SpellbookSpell]:
        return self._mapper.fetch(spellbook_id)

    def update(self, spellbook_spell: SpellbookSpell):
        return self._mapper.update(spellbook_spell)

    def insert(self, spellbook_spell: SpellbookSpell):
        return self._mapper.insert(spellbook_spell)

    def delete(self, spellbook_spell: SpellbookSpell):
        return self._mapper.delete(spellbook_spell)


interface = SpellbookSpellFacade(SpellbookSpellMapper.mapper)
