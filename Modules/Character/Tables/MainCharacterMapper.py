from enum import Enum
from Character.Data.CharacterID import CharacterID
from Character.Data.DiscordID import DiscordID
from Character.Data.Character import Character
from Character.Tables.Queries import Queries
from typing import List


class MainCharacterMapper:
    """
    Character info storage
    """
    def __init__(self, queries, table_info):
        """
        Define dependencies
        """
        self._queries = queries
        self._table_info = table_info

    def transform_query_dict(self, query_dict: dict) -> dict:
        """
        Transform dictionary containing keys of Main_Character columns to Character attribute names
        :param query_dict: dictionary containing key:value where key is column name from Main_Character
        :return: dict containing new keys relating to Character attributes
        """
        column_attribute_dict = self._table_info.to_column_dict()
        character_dict = dict((column_attribute_dict[k], v) for k, v in query_dict.items())
        return character_dict

    def transform_character_dict(self, character_dict: dict) -> dict:
        """
        Transform dictionary containing keys of Character attribute names to Main_Character columns
        :param character_dict: dictionary containing key:value where key is column name from Main_Character
        :return: dict containing new keys relating to Character attributes
        """
        column_attribute_dict = self._table_info.to_dict()
        character_dict = dict((column_attribute_dict[k], v) for k, v in character_dict.items())
        return character_dict

    def fetch(self, character_id: CharacterID) -> Character:
        """
        Fetch Character from tables using character_id as key
        :param character_id: key for fetching data from tables
        :return: Character object
        """
        query_dict = self._queries.select_by_key(self._table_info, character_id.value)
        character = Character(**self.transform_query_dict(query_dict))
        return character

    def fetch_by_discord_id(self, discord_id: DiscordID) -> List[Character]:
        data = self._queries.select(self._table_info, self._table_info.discord_id, discord_id.value)
        characters = []
        for query_dict in data:
            characters.append(Character(**self.transform_query_dict(query_dict)))
        return characters

    def update(self, character: Character) -> None:
        data = character.to_dict()
        where_key = self._table_info.key
        where_value = data.pop(where_key)
        self._queries.update_by_key(self._table_info, data, where_value)

    def insert(self, character: Character) -> None:
        self._queries.insert(self._table_info, self.transform_character_dict(character.to_dict()))


class Constants(str, Enum):
    """Storage for Main_Character column/db labels and info"""
    table = "Main_Characters"
    key = "ID"
    # -------------------------- #
    character_id = key
    discord_id = "Discord_ID"
    name = "Character_Name"
    race = "Race"
    background = "Background"
    xp = "XP"
    str = "Strength"
    dex = "Dexterity"
    con = "Constitution"
    int = "Intelligence"
    wis = "Wisdom"
    cha = "Charisma"
    gold = "Gold"
    roll_id = "Roll_ID"
    # -------------------------- #

    @staticmethod
    def to_dict() -> dict:
        """
        Helper function to convert this classes enumerated fields to a dictionary of key:value. Where:
            - key = Attribute **Name**
            - value = Attribute **Value**
        :return: [dict] dictionary of enumerated fields
        """
        return {k: v for k, v in Constants.__members__.items()}

    @staticmethod
    def to_column_dict() -> dict:
        """
        Helper function to convert this classes enumerated fields to a dictionary of key:value. Where:
            - key = Attribute **Value**
            - value = Attribute **Name**
        :return: [dict] dictionary of enumerated fields
        """
        return {v: k for k, v in Constants.__members__.items()}

    @staticmethod
    def format(query: str) -> str:
        """
        Helper function which returns passed string formatted with Constants enumerated values replaced.
        :param query: string with *only* fields from this class
        :return: [str] formatted string
        """
        return query.format(**Constants.to_dict())


mapper = MainCharacterMapper(Queries, Constants)
