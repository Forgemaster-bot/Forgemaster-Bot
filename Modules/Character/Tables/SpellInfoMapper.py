from enum import Enum
from Character.Data.SpellInfo import SpellInfo
from Character.Tables.Queries import Queries
from Character.Tables.TableMapper import TableMapper


class SpellInfoMapper(TableMapper):
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


class Constants(str, Enum):
    """
    Storage for Info_Spells column/db labels and info
        Fields = Name, Level, School, Ritual, Source, Consumable_Cost
        Items per key = Multiple
    """
    table = "Info_Spells"
    key = "Name"
    # -------------------------- #
    name = key
    level = "Level"
    school = "School"
    ritual = "Ritual"
    source = "Source"
    consumable_cost = "Consumable_Cost"
    # -------------------------- #
    update_keys = [key]

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


mapper = SpellInfoMapper(Queries, Constants, SpellInfo)
