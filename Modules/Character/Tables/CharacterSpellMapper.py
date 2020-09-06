from enum import Enum
from Character.Data.CharacterSpell import CharacterSpell
from Character.Tables.Queries import Queries
from Character.Tables.TableMapper import TableMapper
from typing import List

class CharacterSpellMapper(TableMapper):
    """
    CharacterInfo's skill mapper
    """
    def __init__(self, queries, table_info, storage_type):
        """
        Define dependency injection objects
        :param queries:
        :param table_info:
        :param storage_type:
        """
        super().__init__(queries, table_info, storage_type)

    def fetch_by_id_and_origin(self, character_id: str, origin: str) -> List[CharacterSpell]:
        return self.fetch(character_id, where_and_pairs=[(self._table_info.origin, origin)])


class Constants(str, Enum):
    """
    Storage for Main_Spell_Book column/db labels and info
        Fields = Spell_Book_ID,Spell,Known
        Items per key = Multiple
    """
    table = "Link_Character_Spells"
    key = "Character_ID"
    # -------------------------- #
    character_id = key
    name = "Spell"
    origin = "Origin"
    # -------------------------- #
    update_keys = [key, name]

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


mapper = CharacterSpellMapper(Queries, Constants, CharacterSpell)
