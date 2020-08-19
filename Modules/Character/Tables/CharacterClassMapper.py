from enum import Enum
from Character.Data.CharacterClass import CharacterClass
from Character.Tables.Queries import Queries
from Character.Tables.TableMapper import TableMapper


class CharacterClassMapper(TableMapper):
    """
    Character's class mapper
    """
    def __init__(self, queries, table_info, storage_type):
        """
        Define dependency injection objects
        :param queries:
        :param table_info:
        :param storage_type:
        """
        super().__init__(queries, table_info, storage_type)


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
    update_keys = [character_id, class_name]

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


mapper = CharacterClassMapper(Queries, Constants, CharacterClass)
