import Character.Data.CharacterID as CharacterID
import Character.Tables.CharacterClassMapper
import Character.Data.CharacterClass
from typing import List


class CharacterClassFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, mapper):
        self._mapper = mapper

    def fetch(self, character_id: CharacterID.CharacterID) -> Character.Data.CharacterClass.CharacterClass:
        return self._mapper.fetch(character_id)

    def update(self, character: Character.Data.CharacterClass.CharacterClass):
        return self._mapper.update(character)

    def insert(self, character: Character.Data.CharacterClass.CharacterClass):
        return self._mapper.insert(character)


interface = CharacterClassFacade(Character.Tables.CharacterClassMapper.mapper)
