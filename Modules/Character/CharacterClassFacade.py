import Character.Tables.CharacterClassMapper
from typing import List


class CharacterClassFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, mapper):
        self._mapper = mapper

    def fetch(self, character_id: str) -> List:
        return self._mapper.fetch(character_id)

    def update(self, character_class):
        return self._mapper.update(character_class)

    def insert(self, character_class):
        return self._mapper.insert(character_class)

    def delete(self, character_class):
        return self._mapper.delete(character_class)


interface = CharacterClassFacade(Character.Tables.CharacterClassMapper.mapper)
