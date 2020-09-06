import Character.Tables.CharacterSpellMapper as CharacterSpellMapper
from Character.Data.CharacterSpell import CharacterSpell
from typing import List


class CharacterSpellFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, mapper):
        self._mapper = mapper

    def fetch(self, character_id: str, origin: str) -> List[CharacterSpell]:
        return self._mapper.fetch_by_id_and_origin(character_id, origin)

    def fetch_by_id_and_origin(self, character_id: str, origin: str) -> List[CharacterSpell]:
        return self._mapper.fetch_by_id_and_origin(character_id, origin)

    def fetch_by_character_id(self, character_id: str):
        return self._mapper.fetch(character_id)

    def update(self, spell: CharacterSpell):
        return self._mapper.update(spell)

    def insert(self, spell: CharacterSpell):
        return self._mapper.insert(spell)

    def delete(self, spell: CharacterSpell):
        return self._mapper.delete(spell)


interface = CharacterSpellFacade(CharacterSpellMapper.mapper)
