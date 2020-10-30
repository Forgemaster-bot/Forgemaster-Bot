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

    def update(self, feat: CharacterFeat):
        return self._mapper.update(feat)

    def insert(self, feat: CharacterFeat):
        return self._mapper.insert(feat)

    def delete(self, feat: CharacterFeat):
        return self._mapper.delete(feat)


interface = CharacterFeatFacade(CharacterFeatMapper.mapper)
