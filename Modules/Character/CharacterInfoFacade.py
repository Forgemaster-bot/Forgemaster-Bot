import Character.Tables.MainCharacterMapper
from Character.Data.CharacterInfo import CharacterInfo
from typing import List


class CharacterInfoFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, character_mapper):
        self._character_mapper = character_mapper

    def fetch(self, character_id: str) -> CharacterInfo:
        return self._character_mapper.fetch(character_id)[0]

    def fetch_by_discord_id(self, discord_id: str) -> List[CharacterInfo]:
        return self._character_mapper.fetch_by_discord_id(discord_id)

    def update(self, character: CharacterInfo):
        return self._character_mapper.update(character)

    def insert(self, character: CharacterInfo):
        return self._character_mapper.insert(character)


interface = CharacterInfoFacade(Character.Tables.MainCharacterMapper.mapper)
