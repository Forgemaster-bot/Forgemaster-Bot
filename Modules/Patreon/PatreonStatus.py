from enum import Enum
import Quick_Python


class Constants(str, Enum):
    """Storage for location of Patreon Status within database."""
    table = "Info_Discord"
    column = "Patreon"
    key = "ID"

    @staticmethod
    def to_dict() -> dict:
        """
        Helper function to convert this classes enumerated fields to a dictionary
        :return: [dict] dictionary of enumerated fields
        """
        return {k: v for k, v in Constants.__members__.items()}

    @staticmethod
    def format(query: str) -> str:
        """
        Helper function which returns passed string formatted with Constants enumerated values replaced.
        :param query: string with *only* fields from this class
        :return: [str] formatted string
        """
        return query.format(**Constants.to_dict())


class PatreonStatus:
    """
    Container of static methods for handling Patreon Status
    """
    @staticmethod
    def update(discord_id: str, is_patreon: bool) -> None:
        """
        Update patreon status of a discord member to enable/disable features for them.
        :param discord_id: Unique ID of the discord user.
        :param is_patreon: boolean value for value to set in database
        :return: None
        """
        query = """\
                UPDATE [{table}]
                SET [{column}] = ?
                WHERE ID = ?
                """
        query = Constants.format(query)
        args = [is_patreon, discord_id]  # status_column = <is_patreon>; ID = <discord_id>
        Quick_Python.run_query_commit(query, args)

    @staticmethod
    def select(discord_id: str) -> bool:
        """
        Select patreon status of a discord member.
        :param discord_id: Unique ID of discord user.
        :return: boolean value of patreon status
        """
        query = """\
                SELECT [{column}]
                FROM [{table}]
                WHERE [{key}] = ?
                """
        args = [discord_id]
        result = Quick_Python.run_query(Constants.format(query), args).fetchone()
        return None if result is None else result[0]


    """
    Alias static method above from sql operation names to standard getter/setter 
    """
    set = update
    get = select


