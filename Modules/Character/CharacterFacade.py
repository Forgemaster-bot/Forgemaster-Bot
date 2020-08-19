import Character.Data.CharacterID as CharacterID
import Character.Data.DiscordID as DiscordID
import Character.Tables.MainCharacterMapper
import Character.Data.Character
from typing import List


class CharacterFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, character_mapper):
        self._character_mapper = character_mapper

    def fetch(self, character_id: str) -> Character.Data.Character.Character:
        return self._character_mapper.fetch(character_id)[0]

    def fetch_by_discord_id(self, discord_id: str) -> List[Character.Data.Character.Character]:
        return self._character_mapper.fetch_by_discord_id(discord_id)

    def update(self, character: Character.Data.Character.Character):
        return self._character_mapper.update(character)

    def insert(self, character: Character.Data.Character.Character):
        return self._character_mapper.insert(character)


interface = CharacterFacade(Character.Tables.MainCharacterMapper.mapper)
