from enum import Enum
from Character.Data.CharacterID import CharacterID
from Character.Data.CharacterClass import CharacterClass
from Character.Tables.Queries import Queries
from typing import List
import Quick_Python


class CharacterClassMapper:
    """
    Character's class mapper
    """
    def __init__(self, queries, table_info):
        """
        Define dependencies
        :param queries:
        :param table_info:
        """
        self._queries = queries
        self._table_info = table_info

    def fetch(self, character_id: CharacterID) -> List[CharacterClass]:
        """
        Fetch CharacterClass objects from tables using character_id as key
        :param character_id: key for fetching data from tables
        :return: List of CharacterClass objects
        """
        table_dicts = self.queries.select(self._table_info, character_id.value)
        character_classes = []
        for row_dict in table_dicts:
            transformed_dict = Quick_Python.transform_dict_keys(row_dict, self._table_info.to_column_dict())
            character_classes.append(CharacterClass(**transformed_dict))
        print(self)

    def update(self, character_class: CharacterClass) -> None:
        """
        Updates row in table matching key
        :param character_class: CharacterClass object to update
        :return: None
        """
        data = character_class.to_dict()
        key_info = [self._table_info.character_id, self._table_info.class_name]
        where_info = {k: data.pop(k) for k in key_info}
        self._queries.update(self._table_info, data, where_info)

    def insert(self, character_class: CharacterClass) -> None:
        query_dict = Quick_Python.transform_dict_keys(character_class.to_dict(), self._table_info.to_dict())
        self._queries.insert(self._table_info, query_dict)


class Constants(str, Enum):
    """
    Storage for Link_Character_Class column/db labels and info
    """
    table = "Link_Character_Class"
    key = "Character_ID"
    # -------------------------- #
    character_id = key
    class_name = "Class"
    level = "Level"
    number = "Number"
    subclass = "Sub_Class"
    free_book_spells = "Free_Book_Spells"
    can_replace_spells = "Replace_Spell"
    has_class_choice = "Class_Choice"
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


mapper = CharacterClassMapper(Queries, Constants)
