from enum import Enum
from Character.Data.Spellbook import Spellbook
from Character.Tables.Queries import Queries
from Character.Tables.TableMapper import TableMapper
from typing import List

class SpellbookMapper(TableMapper):
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

    def fetch_by_character_id(self, character_id: str) -> List[Spellbook]:
        return self.fetch(column=self._table_info.character_id, value=character_id)


class Constants(str, Enum):
    """
    Storage for Main_Spell_Book column/db labels and info
    ID,Owner_ID,Name,Type
    """
    table = "Main_Spell_Book"
    key = "ID"
    # -------------------------- #
    spellbook_id = key
    character_id = "Owner_ID"
    name = "Name"
    type = "Type"
    # -------------------------- #
    update_keys = [key, character_id]

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


mapper = SpellbookMapper(Queries, Constants, Spellbook)
