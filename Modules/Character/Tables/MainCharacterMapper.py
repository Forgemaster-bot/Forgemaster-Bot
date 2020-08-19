from enum import Enum
from Character.Data.CharacterID import CharacterID
from Character.Data.DiscordID import DiscordID
from Character.Data.CharacterInfo import CharacterInfo
from Character.Tables.Queries import Queries
from Character.Tables.TableMapper import TableMapper
from typing import List
from Quick_Python import transform_dict_keys


class MainCharacterMapper(TableMapper):
    """
    CharacterInfo info storage
    """
    def __init__(self, queries, table_info, storage_type):
        """
        Define dependency injection objects
        :param queries:
        :param table_info:
        :param storage_type:
        """
        super().__init__(queries, table_info, storage_type)

    def fetch_by_discord_id(self, discord_id: str) -> List[CharacterInfo]:
        return self.fetch(column=self._table_info.discord_id, value=discord_id)


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
    update_keys = [character_id]

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


mapper = MainCharacterMapper(Queries, Constants, CharacterInfo)
