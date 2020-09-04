import Character.Tables.MainCharacterMapper as Mapper
from Character.Data.CharacterInfo import CharacterInfo
from typing import List


class CharacterInfoFacade:
    """
    Facade for fetching and saving a character
    """
    def __init__(self, mapper):
        self._mapper = mapper

    def update(self, value: CharacterInfo):
        return self._mapper.update(value)

    def insert(self, value: CharacterInfo):
        return self._mapper.insert(value)

    def delete(self, value: CharacterInfo):
        return self._mapper.delete(value)

    def fetch(self, character_id: str) -> CharacterInfo:
        """
        Fetches single CharacterInfo object by character_id key.
        :param character_id: Key to search for
        :return: CharacterInfo object
        """
        return self._mapper.fetch(value=character_id)[0]

    """
    Additional functions not defined in the 'base' facade
    """
    def fetch_keys(self) -> list:
        return self._mapper.fetch_keys()

    def fetch_by_discord_id(self, value: str) -> List[CharacterInfo]:
        return self._mapper.fetch_by_discord_id(value)

    def fetch_by_character_name(self, value: str) -> List[CharacterInfo]:
        return self._mapper.fetch(column=Mapper.mapper.table_info.name, value=value)


interface = CharacterInfoFacade(Mapper.mapper)
