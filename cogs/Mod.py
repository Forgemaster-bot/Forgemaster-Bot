from datetime import datetime
from operator import itemgetter
from typing import List, Tuple
import logging
from textwrap import dedent

from discord.ext import commands
import Connections
import Quick_Python
from Character.CharacterInfoFacade import interface as character_info_interface
from Character.LinkClassSpellFacade import interface as link_class_spell_interface
from Character.Character import Character
import cogs.utils.menu as menu_helper
import Update_Google_Roster as Roster

log = logging.getLogger(__name__)
MAX_MESSAGE_SIZE = 2000

class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dms_logging_tickets = {}

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


    @commands.command(name='add_spell', help='.add_spell <character_name>, <origin>, <spell>')
    @commands.has_any_role('DMs', 'Mods', 'Forge Smiths')
    def add_spell(self, ctx, *, args):
        # Parse arguments passed and handle error cases
        try:
            name, dndclass, spell = args.split(',')
        except ValueError as err:
            log.error(f"add_spell - '{ctx.author}' - Invalid argument format passed for args '{args}'")
            await ctx.send(f"ERROR: Invalid argument format passed. Should be: <character_name>, <origin>, <spell>")
            return
        except Exception as err:
            log.error(f"add_spell - '{ctx.author}' - Unknown exception thrown for args '{args}'")
            await ctx.send(f"ERROR: Unknown exception thrown - {str(err)}")
            return

        log.info(f"add_spell - '{ctx.author}' is adding spell '{spell}' with origin '{dndclass}' to '{name}''")

        # Fetch character info. Check that the info is valid and only one character was returned.
        character_info = character_info_interface.fetch_by_character_name(name)
        if character_info is None:
            log.error(f"add_spell - '{ctx.author}' - No character with the name '{name}' found.")
            await ctx.send(f"ERROR: No character with the name '{name}' found.")
            return
        if len(character_info) > 1:
            log.error(f"add_spell - '{ctx.author}' - Multiple characters with the name '{name}' found.")
            await ctx.send(f"ERROR: Multiple characters with the name '{name}' found.")
            return

        # Make Character object from the character info
        character = Character(character_info[0].character_id)

        # Verify dndclass is valid
        if not (character.has_class(dndclass) or character.has_subclass(dndclass)):
            log.error(f"add_spell - '{ctx.author}' - Character does not have matching class or subclass '{dndclass}'")
            await ctx.send(f"ERROR: Character does not have matching class or subclass with name '{dndclass}'")
            return

        # Verify a matching spell is found for dndclass
        dndclass_spells = link_class_spell_interface.fetch(dndclass)
        matching_spells = [s for s in dndclass_spells.values() if s.spell_name == spell]
        if not any(matching_spells):
            log.error(f"add_spell - '{ctx.author}' - No matching spells for '{spell}' and class/subclass '{dndclass}'")
            await ctx.send(f"ERROR: No matching spells named '{spell}' for class/subclass '{dndclass}'")
            return

        # Confirm the choice.
        msg = f"Would you like to confirm: '{name}' should learn the spell '{spell}' with an origin of '{dndclass}'?"
        m = await menu_helper.start_menu(ctx, menu_helper.ConfirmMenu, message=msg, should_dm=False)
        if not m.confirm:
            log.info(f"add_spell - '{ctx.author}' - Cancelled adding '{spell}' to '{name}'")
            await ctx.send(f"Cancelling the request.")
            return

        # Add the spell
        character.learn_spell(dndclass, matching_spells[0], cog=self, channel=ctx)
        log.info(f"add_spell - '{ctx.author}' - Done ading '{spell}' to '{name}'")



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
        dm_opened_menu = False
        try:
            """
            Check if a DM is currently trying to submit a ticket
            """
            if ctx.message.author.id in self.dms_logging_tickets:
                log.error(f"ticket - '{ctx.author}' is already logging a ticket. Cancelling.")
                channel = await menu_helper.get_channel(ctx)
                await channel.send("You are already logging a ticket. Cancelling.")
                return
            else:
                dm_opened_menu = True
                self.dms_logging_tickets[ctx.message.author.id] = None
                log.info(f"ticket - '{ctx.author}' inserted into dms_logging_tickets")

            name, _, item_string = args.partition('/')
            characters = character_info_interface.fetch_by_character_name(name)

            """
            Handle logging a ticket
            """
            # Check for valid character names
            if len(characters) != 1:
                log.error(f"ticket - Found multiple characters for name '{name}'")
                await ctx.send(f"ERROR: {'Multiple' if len(characters) else 'No'} characters found matching '{name}'")
                return

            # Select first *and only* character in the list
            character = Character(characters[0].character_id)
            log.info(f"ticket - '{ctx.author}' is logging exit ticket for '{character.name}'")

            # Parse item_string into a dictionary of name:quantity pairs
            try:
                items = self.parse_ticket_items(item_string)
            except ValueError as err:
                await ctx.send(f"ERROR: {str(err)}")
                return
            except Exception as err:
                await ctx.send(f"ERROR: Unknown exception thrown - {str(err)}")
                return

            # Check that user has enough for any negative values
            # TODO: Remove if we figure out a way to handle cursors and can rollback changes.
            for name, quantity in items.items():
                # Continue if value is positive
                if quantity >= 0:
                    continue

                # Handle checking for a negative quantity
                quantity = quantity * -1
                error_string = f"ERROR: Cannot remove **{quantity} x {name}** as '{character.name}'"
                # Handle gold and xp different since they aren't 'items'
                if name.lower() == 'gold' or name.lower() == 'xp':
                    if not character.has_item_quantity_by_keyword(**{name: quantity}):
                        amount = character.gold if name.lower() == 'gold' else character.xp
                        await ctx.send(f"{error_string} only has ***{amount}*** x **{name}**")
                        return
                else:
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
                log.info(f"ticket - '{ctx.author}' rejected the following changes: {items}")
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

        finally:
            """
            Handle removing dm from list if they opened it
            """
            if dm_opened_menu:
                self.dms_logging_tickets.pop(ctx.message.author.id)


def setup(bot):
    bot.add_cog(Mod(bot))
