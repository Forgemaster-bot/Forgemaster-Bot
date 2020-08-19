import Character.Tables.CharacterFeatMapper as CharacterFeatMapper
from Character.Data.CharacterFeat import CharacterFeat
from typing import List


class CharacterFeatFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, mapper):
        self._mapper = mapper

    def fetch(self, character_id: str) -> List[CharacterFeat]:
        return self._mapper.fetch(character_id)

    def update(self, character: CharacterFeat):
        return self._mapper.update(character)

    def insert(self, character: CharacterFeat):
        return self._mapper.insert(character)


interface = CharacterFeatFacade(CharacterFeatMapper.mapper)
