from datetime import datetime
from operator import itemgetter
from typing import List, Tuple
import logging
from textwrap import dedent

from discord.ext import commands
import Connections
import Quick_Python
from Character.CharacterInfoFacade import interface as character_info_interface
from Character.Character import Character
import cogs.utils.menu as menu_helper
import Update_Google_Roster as Roster

log = logging.getLogger(__name__)
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

    @staticmethod
    def parse_ticket_items(item_string):
        items = {}
        for item in item_string.split(','):
            name, _, quantity = item.partition(':')
            try:
                quantity = int(quantity or 1)
            except ValueError:
                log.info(f"Failed to parse quantity for item '{item}'")
                raise ValueError(f"Failed to parse quantity for item '{item}'. Please verify and try again.")
            items[name.strip()] = quantity
        return items

    @commands.command(name='ticket', brief='Exit ticket command.',
                      help=dedent("""\
                      Command which will handle adding gold, xp, and items to a character after a session.
                      Usage: .ticket *<character_name>*/*<item>*:*<amount>*,*<item>*:*<amount>*...
                      Example: `.ticket Name/Gold:-100, XP:300, Blue Dust:10 
                      """),
                      )
    @commands.has_any_role('DMs', 'Mods', 'Admins')
    async def ticket(self, ctx, *, args):
        name, _, item_string = args.partition('/')
        characters = character_info_interface.fetch_by_character_name(name)

        # Check for valid character names
        if len(characters) != 1:
            await ctx.send(f"ERROR: {'Multiple' if len(characters) else 'No'} character names found matching '{name}'")
            return

        # Select first *and only* character in the list
        character = Character(characters[0].character_id)
        log.info(f"'{ctx.author}' is logging exit ticket for '{character.name}'")

        # Parse item_string into a dictionary of name:quantity pairs
        try:
            items = self.parse_ticket_items(item_string)
        except ValueError as err:
            await ctx.send(f"ERROR: {str(err)}")
            return

        # Check that user has enough for any negative values
        # TODO: Remove if we figure out a way to handle cursors and can rollback changes.
        for name, quantity in items.items():
            if quantity < 0:
                quantity = quantity * -1
                error_string = f"ERROR: Cannot remove **{quantity} x {name}** as '{character.name}'"
                if not character.has_item(name):
                    await ctx.send(f"{error_string} has none.")
                    return
                if not character.has_item_quantity(name, quantity):
                    await ctx.send(f"{error_string} only has ***{character.items[name].quantity}*** x **{name}**")
                    return

        # Ask user to confirm the choices
        input_choices = "\n".join([f"\t**{quantity}** x **{name}**" for name, quantity in items.items()])
        msg = f"Would you like to confirm the following changes for '{character.name}'?\n{input_choices}"

        m = await menu_helper.start_menu(ctx, menu_helper.ConfirmMenu, message=msg, should_dm=False)
        if not m.confirm:
            log.info(f"'{ctx.author}' rejected the following changes: {items}")
            await ctx.send(f"Cancelled making exit ticket for '{character.name}'")
            return

        # Perform item changes
        for name, quantity in items.items():
            character.modify_item_amount(name, quantity)

        # Log changes to roster, info channel, and user
        msg = f"**'{ctx.author}'** did the following item changes to '{character.name}':\n{input_choices}"
        await Connections.log_to_discord(self, msg)
        Roster.update_character_in_roster(character)
        await ctx.send(f"Exit ticket logged successfully for '{character.name}'")


def setup(bot):
    bot.add_cog(Mod(bot))
