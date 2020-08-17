import Character.Data.CharacterID as CharacterID
import Character.Data.DiscordID as DiscordID
import Character.Tables.Main_Characters
import Character.Data.Character
from typing import List


class CharacterFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, character_mapper):
        self._character_mapper = character_mapper

    def fetch(self, character_id: CharacterID.CharacterID) -> Character.Data.Character.Character:
        return self._character_mapper.fetch(character_id)

    def fetch_by_discord_id(self, discord_id: DiscordID.DiscordID) -> List[Character.Data.Character.Character]:
        return self._character_mapper.fetch_by_discord_id(discord_id)

    def update(self, character: Character.Data.Character.Character):
        return self._character_mapper.update(character)

    def insert(self, character: Character.Data.Character.Character):
        return self._character_mapper.insert(character)


character_facade = CharacterFacade(Character.Tables.Main_Characters.mapper)
