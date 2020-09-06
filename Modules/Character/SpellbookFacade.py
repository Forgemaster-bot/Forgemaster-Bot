import Character.Tables.SpellbookMapper as SpellbookMapper
from Character.Data.Spellbook import Spellbook
from typing import List


class SpellbookFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, mapper):
        self._mapper = mapper

    def fetch(self, spellbook_id: str) -> List[Spellbook]:
        return self._mapper.fetch(spellbook_id)

    def fetch_by_character_id(self, character_id: str) -> List[Spellbook]:
        return self._mapper.fetch_by_character_id(character_id)

    def update(self, spellbook: Spellbook):
        return self._mapper.update(spellbook)

    def insert(self, spellbook: Spellbook):
        return self._mapper.insert(spellbook)

    def delete(self, spellbook: Spellbook):
        return self._mapper.delete(spellbook)


interface = SpellbookFacade(SpellbookMapper.mapper)
