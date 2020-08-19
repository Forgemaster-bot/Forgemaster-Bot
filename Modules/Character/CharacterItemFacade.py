import Character.Tables.CharacterItemMapper as CharacterItemMapper
from Character.Data.CharacterItem import CharacterItem
from typing import List


class CharacterItemFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, mapper):
        self._mapper = mapper

    def fetch(self, character_id: str) -> List[CharacterItem]:
        return self._mapper.fetch(character_id)

    def update(self, character: CharacterItem):
        return self._mapper.update(character)

    def insert(self, character: CharacterItem):
        return self._mapper.insert(character)


interface = CharacterItemFacade(CharacterItemMapper.mapper)
