import Character.Tables.CharacterClassMapper
from Character.Data.CharacterClass import CharacterClass
from typing import List


class CharacterClassFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, mapper):
        self._mapper = mapper

    def fetch(self, character_id: str) -> List:
        return self._mapper.fetch(character_id)

    def update(self, character: CharacterClass):
        return self._mapper.update(character)

    def insert(self, character: CharacterClass):
        return self._mapper.insert(character)

    def delete(self, character: CharacterClass):
        return self._mapper.delete(character)


interface = CharacterClassFacade(Character.Tables.CharacterClassMapper.mapper)
