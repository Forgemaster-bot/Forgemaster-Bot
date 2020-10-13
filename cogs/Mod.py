from datetime import datetime
from operator import itemgetter
from typing import List, Tuple

from discord.ext import commands
import Connections
import Quick_Python

MAX_MESSAGE_SIZE = 2000

class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='history_like', help='Args = string to search for')
    @commands.has_any_role('DMs', 'Mods', 'Forge Smiths')
    async def history_like(self, ctx, *, to_find):
        """Read all commands like 'to_find' then outputs them into messages sorted by time"""
        command_history: List[Tuple[datetime, int, str]] = []
        with Connections.sql_db_connection() as cursor:
            query = "SELECT * FROM Command_Logs WHERE [Command] LIKE ?"
            args = [f"%{to_find}%"]
            Quick_Python.log_transaction(query, args)
            cursor.execute(query, args)
            for row in cursor:
                command_history.append((row.DateTime, row.User_ID, row.Command))

        await ctx.send(f"{len(command_history)} messages found. Outputting in sorted order:")
        command_history.sort(key=itemgetter(0))
        message = ""
        for time, discord_id, command in command_history:
            output = f"{time} - <@{discord_id}> - {command}\n"
            # Send accumulated messages and reset if we hit the character limit
            if len(output) + len(message) > MAX_MESSAGE_SIZE:
                await ctx.send(message)
                message = ""
            message = f"{message}{output}"

        if len(message): await ctx.send(message) #  Handle sending left over items
        await ctx.send(f"Completed.")

def setup(bot):
    bot.add_cog(Mod(bot))
