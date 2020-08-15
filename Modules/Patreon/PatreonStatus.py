from enum import Enum
import discord
import Patreon.PatreonConfig


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
        if not Patreon.PatreonConfig.is_enabled():
            return False
        # Search through server roles for extra character role
        extra_character_role = Patreon.PatreonConfig.get_extra_character_role()
        role = discord.utils.find(lambda r: r.name == extra_character_role, ctx.message.guild.roles)
        # Return true if role found in author's roles
        return True if role in ctx.message.author.roles else False




