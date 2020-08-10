from enum import Enum
import discord


class Constants(str, Enum):
    """Storage for location of Patreon Status within database."""
    role = "Patreon"

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
    Storage for methods related to getting PatreonStatus
    """
    @staticmethod
    def get(ctx: discord.ext.commands.Context) -> bool:
        """
        Returns weather context passed has patreon status/role
        :param ctx: Discord context from command
        :return: True is patreon, false otherwise
        """
        # Find patreon role from server of the context
        role = discord.utils.find(lambda r: r.name == Constants.role, ctx.message.server.roles)
        # Return true if role found in author's roles
        return True if role in ctx.message.author.roles else False




