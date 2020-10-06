from discord.ext import commands
from discord.ext import menus
from discord.ext import tasks
import asyncio
import uuid
import datetime
import logging
import discord
import itertools
import calendar
import pytz
from typing import List, Optional

# Own modules
import Quick_Python
from Crafting.Utils import query_user
from Character.Tables.Queries import Queries
from Character.CharacterInfoFacade import interface as character_info_interface
from cogs.utils import menu
from cogs.utils import member_utils
from cogs.utils import StandaloneQueries
from cogs.utils import time
from cogs.Menu import Menu
from Modules import Connections

log = logging.getLogger(__name__)


def get_current_time(tz=pytz.timezone('GMT')):
    return datetime.datetime.now(tz=tz)


async def get_cog(bot, channel, cog_name):
    menu_cog = bot.get_cog(cog_name)
    if menu_cog is None:
        if channel is not None:
            msg = f"{cog_name} cog is missing. Contact developer or admin"
            await channel.send(msg)
        raise RuntimeError(f"{cog_name} cog is missing")
    return menu_cog


def execute_single_nondata_query(query: str, args: list) -> bool:
    try:
        with Connections.sql_db_connection() as cursor:
            Quick_Python.log_transaction(query, args)
            cursor.execute(query, args)
            return True
    except Exception as err:
        log.exception(err)
        return False


def execute_single_data_query(query: str, args: list) -> Optional[dict]:
    try:
        with Connections.sql_db_connection() as cursor:
            Quick_Python.log_transaction(query, args)
            cursor.execute(query, args)
            row = cursor.fetchone()
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
    except Exception as err:
        log.exception(err)
        return None


async def fetch_link(ctx, message_id):
    try:
        if message_id is None:
            return "None"
        msg = await ctx.fetch_message(message_id)
        return msg.jump_url
    except discord.NotFound:
        return "None"


class Column:
    python_type = None
    sql_type = None

    def __init__(self, name, primary=False, size=None, null=False):
        self.name = name
        self.primary = primary
        self.size = size
        self.null = null

    @property
    def primary(self) -> bool:
        return self._primary

    @primary.setter
    def primary(self, value: bool) -> None:
        self._primary = value

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value) -> None:
        self._size = value
        self._size_str = '' if value is None else f"({str(value)})"

    @property
    def size_str(self) -> str:
        return self._size_str

    @property
    def null(self) -> str:
        return self._null

    @null.setter
    def null(self, value: bool) -> None:
        self._null = 'NULL' if value else 'NOT NULL'


class UniqueIdColumn(Column):
    python_type = uuid.UUID
    sql_type = 'uniqueidentifier'


class DatetimeColumn(Column):
    python_type = datetime.datetime
    sql_type = 'datetime2'


class BoolColumn(Column):
    python_type = bool
    sql_type = 'bit'


class IntColumn(Column):
    python_type = int
    sql_type = 'BIGINT'


class FloatColumn(Column):
    python_type = float
    sql_type = 'float'

    def __init__(self, name, size='53', **kwargs):
        super().__init__(name, size=size, **kwargs)


class StringColumn(Column):
    python_type = str
    sql_type = 'nvarchar'

    def __init__(self, name, size='50', **kwargs):
        super().__init__(name, size=size, **kwargs)


class BaseTable:
    table: str = ''
    key: str = ''
    columns: List[Column] = []
    default_order_by: Optional[str] = None

    class Row:
        def __init__(self, **kwargs):
            pass

        def to_dict(self):
            return {k: v for k, v in vars(self).items() if not k.startswith('__') and not callable(v)}

    @classmethod
    def exists(cls) -> bool:
        """
        Returns true if successfully able to compare cls.columns with columns in cls.table
        :return: bool
        """
        try:
            return all(column.name in Quick_Python.get_column_names_and_types(cls.table).keys()
                       for column in cls.columns)
        except Exception as err:
            log.exception(err)
            return False

    @classmethod
    def create(cls) -> bool:
        try:
            with Connections.sql_db_connection() as cursor:
                query = f"CREATE TABLE {cls.table} ( {cls.get_schema_string()} )"
                Quick_Python.log_transaction(query)
                cursor.execute(query)
            return True
        except Exception as err:
            log.exception(err)
            return False

    @classmethod
    def delete_all(cls) -> bool:
        try:
            with Connections.sql_db_connection() as cursor:
                query = f"DELETE FROM [{cls.table}]"
                Quick_Python.log_transaction(query)
                cursor.execute(query)
                return True
        except Exception as err:
            log.exception(err)
            return False

    @classmethod
    def get_schema_string(cls):
        labels = []
        primary_keys = []
        for col in cls.columns:
            labels.append(f"[{col.name}] [{col.sql_type}]{col.size_str} {col.null}")
            if col.primary:
                primary_keys.append(col)
        if len(primary_keys):
            keys = ", ".join(f"[{col.name}]" for col in primary_keys)
            labels.append(f"PRIMARY KEY ({keys})")
        return "\n".join(f"{label}," for label in labels)

    @classmethod
    def to_dict(cls):
        data = {c.name: c.name for c in cls.columns}
        data['table'] = cls.table
        return data

    @classmethod
    def setup(cls) -> None:
        if not cls.exists():
            cls.create()

    @classmethod
    def select_all(cls) -> List[Optional[Row]]:
        return [cls.Row(**row) for row in Queries.select(cls, cls.key, '*', order_by_column=cls.default_order_by)]

    @classmethod
    def insert_row(cls, row: Row):
        inserted_data = Queries.insert(cls, row.to_dict())
        return None if inserted_data is None else cls.Row(**inserted_data)

    @classmethod
    def select_key(cls, key) -> Optional[Row]:
        query = f"SELECT * FROM [{cls.table}] WHERE [auction_id] = ?"
        args = [key]
        data = execute_single_data_query(query, args)
        return cls.Row(**data) if data is not None else None


class AuctionTable(BaseTable):
    table: str = 'Auction'
    key: str = 'auction_id'
    columns: List[Column] = [UniqueIdColumn('auction_id', primary=True),
                             DatetimeColumn('start'), DatetimeColumn('end'),
                             BoolColumn('auto_award'), BoolColumn('open'),
                             StringColumn('item', size='max'), StringColumn('winner', size='max', null=True),
                             IntColumn('message_id', null=True), IntColumn('channel_id', null=True)]
    default_order_by = 'start'

    class Row(BaseTable.Row):
        def __init__(self, item, auto_award, start, open=True, message_id=None, channel_id=None,
                     auction_id=None, end=None, winner=None):
            self.auction_id: uuid.UUID = auction_id
            self.item: str = item
            self.start: datetime.datetime = start
            self.end: datetime.datetime = end
            self.auto_award: bool = auto_award
            self.winner: str = winner
            self.message_id: int = message_id
            self.channel_id: int = channel_id
            self.open: bool = open

        def __str__(self):
            closed = not self.open
            labels = [f"'**{self.item}**'"]
            if closed: labels.append(f"Lasted '*{str(self.end - self.start)}*'")
            if self.winner is not None: labels.append(f"'*{self.winner}*' won the auction")
            labels.append(f"Started on '{self.start.strftime('%c %Z')}'")
            if closed or self.end: labels.append(f"{'Ended' if closed else 'Ends'} on '{self.end.strftime('%c %Z')}'")
            data = " - ".join(labels)
            return f'~~{data}~~' if closed else data

        async def fetch_message(self, ctx: commands.Context) -> Optional[discord.Message]:
            if self.message_id is None:
                return None
            try:
                return await ctx.fetch_message(self.message_id)
            except discord.NotFound:
                return None

        async def query_to_update_time(self, ctx, end):
            log.info(f"auction_start - {ctx.author.display_name} - end date != row end date: {end} != {self.end}")
            channel = await menu.get_channel(ctx)
            await channel.send(f"Would you like to update the auction end time to: {str(end)}?")
            choices = {'Yes': True, 'No': False}
            choice = await query_user(ctx, choices)
            if choices[choice]:
                self.end = end
                AuctionTable.update_end(auction_id=self.auction_id, end=end, open=True)

    @classmethod
    def select_open(cls, item: str = None) -> List[Optional[Row]]:
        with Connections.sql_db_connection() as cursor:
            if item is not None:
                query = f"SELECT * FROM [Auction] WHERE([open] = 'TRUE') AND [item] = ? ORDER BY [start] DESC"
                args = [item]
            else:
                query = f"SELECT * FROM [Auction] WHERE ([open] = 'TRUE') ORDER BY [start] DESC"
                args = []
            Quick_Python.log_transaction(query, args)
            cursor.execute(query, args)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [cls.Row(**dict(zip(columns, row))) for row in rows]

    @classmethod
    def insert(cls, item: str, message_id: int, channel_id: int, auto_award: bool = False):
        new_row = cls.Row(item=item, auto_award=auto_award, start=get_current_time(),
                          message_id=message_id, channel_id=channel_id)
        return cls.insert_row(new_row)

    @classmethod
    def update_message(cls, auction_id: uuid.UUID, channel_id: int, message_id: int) -> bool:
        query = f"UPDATE Auction SET [channel_id] = ?, [message_id] = ? WHERE [auction_id] = ?"
        args = [channel_id, message_id, auction_id]
        return execute_single_nondata_query(query, args)

    @classmethod
    def update_end(cls, auction_id: uuid.UUID, end: datetime.datetime = None, open=False,
                   tz=datetime.timezone.utc) -> bool:
        if end is None:
            end = get_current_time(tz=tz)
        query = f"UPDATE Auction SET [end] = ?, [open] = ? WHERE [auction_id] = ?"
        args = [end, open, auction_id]
        return execute_single_nondata_query(query, args)

    @classmethod
    def make_auction(cls, item: str, end: datetime.datetime) -> Row:
        if end is None:
            raise AttributeError("Cannot start a brand new auction without an end time specified. Aborting...")
        row = cls.Row(item, auto_award=False, start=get_current_time(), end=end)
        row = cls.insert_row(row)
        return row


class BidTable(BaseTable):
    table: str = 'AuctionBids'
    key: str = 'auction_id'
    columns: List[Column] = [UniqueIdColumn('auction_id', primary=True), UniqueIdColumn('character_id', primary=True),
                             DatetimeColumn('time'), FloatColumn('bid')]
    default_order_by = 'time'

    class Row(BaseTable.Row):

        def __init__(self, auction_id: uuid.UUID, character_id: uuid.UUID, time: datetime.datetime, bid: float):
            self.auction_id: uuid.UUID = auction_id
            self.character_id: uuid.UUID = character_id
            self.time: datetime.datetime = time
            self.bid: float = bid

        def __str__(self):
            return "\n".join([
                f"**Bid** = {self.bid}",
                f"**Character_ID** = {self.character_id}",
                f"**Time** = {self.time.strftime('%c %Z')}",
                f"**Auction_ID** = {self.auction_id}"
            ])

    @classmethod
    def get_bid(cls, auction_id: uuid.UUID, character_id: uuid.UUID) -> bool:
        with Connections.sql_db_connection() as cursor:
            query = f"SELECT bid FROM [{cls.table}] WHERE [auction_id] = ? AND [character_id] = ?"
            args = [auction_id, character_id]
            Quick_Python.log_transaction(query, args)
            cursor.execute(query, args)
            return cursor.fetchval()

    @classmethod
    def update_bid(cls, auction_id: uuid.UUID, character_id: uuid.UUID, bid: float, tz=datetime.timezone.utc) -> bool:
        query = f"UPDATE [{cls.table}] SET [bid] = ?, [time] = ? WHERE [auction_id] = ? AND [character_id] = ?"
        args = [bid, get_current_time(tz=tz), auction_id, character_id]
        return execute_single_nondata_query(query, args)

    @classmethod
    def get_auction_bids(cls, auction_id: uuid.UUID) -> List[Optional[Row]]:
        with Connections.sql_db_connection() as cursor:
            query = f"SELECT * FROM [{cls.table}] WHERE [auction_id] = ? ORDER BY [bid] DESC"
            args = [auction_id]
            Quick_Python.log_transaction(query, args)
            cursor.execute(query, args)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [cls.Row(**dict(zip(columns, row))) for row in rows]


class Auction(commands.Cog):
    should_run_tasks = True

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.gmttz = pytz.timezone('GMT')
        self.tz = pytz.timezone('US/Eastern')
        if self.should_run_tasks:
            self.update_auctions.start()

    def cog_unload(self):
        self.update_auctions.cancel()

    @staticmethod
    async def query_for_auction(auctions: List[AuctionTable.Row], ctx, msg) -> Optional[AuctionTable.Row]:
        channel = await menu.get_channel(ctx)
        await channel.send(msg)
        choices = {}
        for a in auctions:
            link = await fetch_link(ctx, a.message_id)
            choices[f"{str(a)} - {link}"] = a
        log.info(f"query_for_auction - {ctx.author.name} - Querying user for choice")
        choice = await query_user(ctx, choices)
        log.info(f"query_for_auction - {ctx.author.name} - Chose {str(choice)}")
        return choices[choice]

    @commands.group(name='auction', description='Group command')
    @commands.check_any(commands.has_any_role('Admins', 'Mods', 'DMs'), commands.is_owner())
    async def auction(self, ctx: commands.Context):
        AuctionTable.setup()
        BidTable.setup()
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='Auction Help', colour=0xFFEF00)
            embed.set_thumbnail(url=menu.thumb_url)
            cmds = sorted([cmd for cmd in ctx.command.walk_commands()], key=lambda cmd: cmd.name)
            embed.description = "\n".join(f"**{cmd.name}** - {cmd.description}" for cmd in cmds)
            await ctx.send(embed=embed)

    @classmethod
    async def select_matching_auction(cls, ctx, auctions: List[AuctionTable.Row]) -> Optional[AuctionTable.Row]:
        user = ctx.author
        channel = await menu.get_channel(ctx)
        await channel.send("Open auction found which matches the item you provided. "
                           "Would you like to create a new auction? ('No' will give you list of open auctions.)")
        choices = {'Yes': True, 'No': False}
        choice = await query_user(ctx, choices)
        create_new = choices[choice]
        if not create_new:
            log.info(f"auction_start - {user.display_name} - Chose to listen to old message.")
            msg = f"Which of the following would you me to begin listening for reactions?"
            row = await cls.query_for_auction(auctions, ctx, msg)
            log.info(f"auction_start - {user.display_name} - Chose auction: {row.to_dict()}")
            return row
        return None

    @staticmethod
    def calculate_timeout(row) -> float:
        return datetime.timedelta.total_seconds(row.end - get_current_time().replace(tzinfo=None))

    @auction.command(name='start', description='Starts an auction.')
    async def auction_start(self, ctx: commands.Context, *, arguments: str):
        channel = await menu.get_channel(ctx)
        item, end = await self.convert_item_name_and_time(ctx, arguments)
        log.info(f"auction_start - {ctx.author.display_name} - args: {arguments}; item = '{item}'; end = '{str(end)}")
        if end is None:
            await ctx.send("Valid time must be passed... Please try again.")
            return

        # Find matching auction and query user if they would like to reopen it
        matching_auctions = AuctionTable.select_open(item=item)
        row = await self.select_matching_auction(ctx, matching_auctions) if matching_auctions else None

        # Without a row, we need to create a new auction
        if row is None:
            try:
                log.info(f"auction_start - {ctx.author.display_name} - Did not find matching auctions for {item}")
                row = AuctionTable.make_auction(item=item, end=end)
                log.info(f"auction_start - {ctx.author.display_name} - Made new auction - {row.to_dict()}")
            except AttributeError as err:
                await ctx.send(str(err))
        elif end != row.end:
            await row.query_to_update_time(ctx, end)

        # Fetch row's current Message from discord
        message = await row.fetch_message(ctx)
        auction_channel_id = Connections.config['auction-channel-id']
        auction_channel = self.bot.get_channel(auction_channel_id)

        # Start the auction menu for players to react to
        m = self.AuctionMenu(row, message=message, delete_message_after=True, timeout=self.calculate_timeout(row))
        await m.start(ctx, channel=auction_channel)

        # Update the message if the auction menu created a new menu
        if message != m.message:
            if message is not None:
                log.info(f"auction_start - {ctx.author.display_name} - Deleting old message {message.id}")
                await message.delete()
            log.info(f"auction_start - {ctx.author.display_name} - Updating message id to {m.message.id}")
            message = m.message
            AuctionTable.update_message(row.auction_id, auction_channel_id, message.id)
        msg = f"'**{ctx.author.display_name}**' started an auction for {row.item} which ends in {m.timeout}s. Link: {message.jump_url}"
        await Connections.log_to_discord(self, msg)
        await channel.send(msg)

    @auction.command(name='history', description='Lists all past auctions')
    async def auction_history(self, ctx: commands.Context):
        auctions = AuctionTable.select_all()
        embed = discord.Embed(title='Auction History', colour=0xFFEF00)
        embed.set_thumbnail(url=menu.thumb_url)
        embed.description = "History of past auctions:"
        i = 0
        for k, g in itertools.groupby(auctions, lambda row: (row.start.month, row.start.year)):
            if i >= 10: break
            month, year = k
            auction_strings = "\n\n".join(str(auction) for auction in g)
            embed.add_field(name=f"{calendar.month_abbr[month]} {year}", value=auction_strings)
            i = i + 1
        if len(embed.fields) == 0:
            embed.add_field(name="None", value="None")
        await ctx.channel.send(embed=embed)

    @auction.command(name='bids', description='Check bids for an auction')
    @commands.is_owner()
    async def auction_bids(self, ctx: commands.Context, auction_id: Optional[uuid.UUID] = None,
                           num_bids: Optional[int] = 10):
        user = ctx.author
        log.info(f"auction_bids - {user.display_name} - Entered. {num_bids} bids requested.")
        if auction_id is None:
            log.info(f"auction_bids - {user.display_name} - Did not pass auction_id. Querying for selection.")
            matching_auctions = AuctionTable.select_open()
            row = await self.query_for_auction(matching_auctions, ctx, "Which would you like me to list bids for?")
            auction_id = row.auction_id
        else:
            log.info(f"auction_bids - {user.display_name} - auction_id was passed. Querying database for auction info.")

        await self.send_bids(auction_id, num_bids)

    @staticmethod
    def get_auction_listing_embed(auction):
        msg = 'A blind auction has started for an item! ' \
              'If you wish to place a bid, simply react to this message with \N{WHITE HEAVY CHECK MARK}. ' \
              'I will then message you directly with a request for your bid. ' \
              'After the duration has expired, the winner will be announced. '
        embed = discord.Embed(title=f'Auction for {auction.item}', colour=0xFFEF00)
        embed.set_thumbnail(url=menu.thumb_url)
        embed.description = msg
        embed.add_field(name="Item For Auction:", value=auction.item)
        duration = str(auction.end - get_current_time().replace(tzinfo=None)) if auction.end else 'Manually Controlled'
        embed.add_field(name="Auction Duration:", value=duration)
        log.info(f"Making auction embed for {auction.item} - {duration} - {auction.message_id}")
        return embed

    @staticmethod
    async def convert_user_friendly_time(ctx, argument):
        converter = time.UserFriendlyTime(commands.clean_content, default='\u2026')
        when = await converter.convert(ctx, argument)
        return True, when

    async def convert_item_name_and_time(self, ctx, arguments):
        try:
            status, when = await self.convert_user_friendly_time(ctx, arguments)
            return when.arg, when.dt
        except commands.BadArgument as err:
            log.info(f"auction_start - {ctx.author.display_name} - Bad time given. {str(err)}")
            await ctx.send(f"Time passed was invalid. {str(err)}")
            return arguments, None

    @staticmethod
    def bid_to_info_dict(bid: BidTable.Row):
        try:
            info = character_info_interface.fetch(bid.character_id)
            can_afford = info.gold >= bid.bid
            return [f"{bid.bid}gp", f"**{info.name}**", f"<@{info.discord_id}>", can_afford]
        except IndexError as e:
            return None

    @classmethod
    def bids_to_str(cls, bids: List[BidTable.Row], max_num, complete: bool = False):
        bid_info = []
        for bid in bids:
            log.info(f"bids_to_str - bid = {repr(bid)}")
            new_bid_info = cls.bid_to_info_dict(bid)
            if new_bid_info is not None:
                bid_info.append(new_bid_info)
            should_stop = len(bid_info) >= max_num if not complete else max_num <= len([i for i in bid_info if i[3]])
            if should_stop:
                break
        return "\n".join([f"{b[0]} - {b[1]} - {'Can Afford' if b[3] else 'Cannot Afford'} - {b[2]}" for b in bid_info])

    async def send_bids(self, auction: uuid.UUID, max_num: int, complete=False):
        row: AuctionTable.Row = AuctionTable.select_key(auction)
        bids = BidTable.get_auction_bids(auction)
        title = f"Current bids for '{row.item}'" if row.open else f"'{row.item}' auction complete!"
        colour = 0xFFEF00
        description = f"List of bids for auction: {str(row)}"
        field_name = f"Top {max_num} Bids"if row.open else "Winning Bids"
        field_msg = self.bids_to_str(bids, max_num, complete=complete)

        embed = discord.Embed(title=title, colour=colour, description=description)
        embed.set_thumbnail(url=menu.thumb_url)
        embed.add_field(name=field_name, value=field_msg if field_msg else 'None')

        channel = self.bot.get_channel(row.channel_id)
        log.info(f"auction_bids - Sending bids to channel {str(channel)} with id {row.channel_id}")
        if complete and channel:
            await channel.send(f"Auction completed for item '**{row.item}**'. Sending winning bids!")
        await channel.send(embed=embed)

    class AuctionMenu(menus.Menu):
        stop_role = 'Admins'

        def __init__(self, auction: AuctionTable.Row, **kwargs):
            self.auction = auction
            log.info(f"AuctionMenu created for auction: {repr(self.auction)}")
            super().__init__(clear_reactions_after=True, **kwargs)

        async def send_initial_message(self, ctx, channel):
            return await channel.send(embed=Auction.get_auction_listing_embed(self.auction))

        def reaction_check(self, payload):
            """ Override reaction_check to allow any member to react """
            if payload.message_id != self.message.id:
                return False
            if payload.user_id == self.ctx.bot.user.id:
                return False
            return payload.emoji in self.buttons

        @menus.button('\N{WHITE HEAVY CHECK MARK}', lock=False)
        async def request_bid(self, payload: discord.RawReactionActionEvent):
            if payload.event_type.lower() != 'reaction_add':
                log.info(f"request_bid - {payload.user_id} - performed invalid event {payload.event_type}")
                return

            only_one_bid_allowed = False
            member: discord.Member = payload.member
            dm_channel = await menu.get_dm_channel(member)

            menu_cog: Menu = await get_cog(self.bot, dm_channel, 'Menu')
            character_id = await menu_cog.select_character(self.ctx, author=member, channel=dm_channel)

            char_name = StandaloneQueries.get_character_name(character_id)
            if char_name is None:
                await dm_channel.send(f"You must make a character first before you can bid on an auction")
                return
            await dm_channel.send(f"Hello {char_name}, I see that you are looking to bid on "
                                  f"the item '**{self.auction.item}**'...")

            existing_bid = BidTable.get_bid(self.auction.auction_id, character_id)
            if only_one_bid_allowed and existing_bid:
                await dm_channel.send(f"Unfortunately, you have already bid {existing_bid}gp in this auction.")
                return

            def wait_for_float(message: discord.Message):
                try:
                    if member.id != message.author.id or dm_channel.id != message.channel.id:
                        return False
                    content = message.content.lower()
                    if content == 'stop' or content == 'exit':
                        return True
                    float(message.content)
                    return True
                except ValueError:
                    return False

            await dm_channel.send(f"How many gold pieces would you like to bid for '**{self.auction.item}**'? "
                                  f"[Enter a floating point value. eg: 10.5]")
            try:
                msg = await self.bot.wait_for('message', check=wait_for_float, timeout=30)
                amount = float(msg.content)
            except asyncio.TimeoutError:
                await dm_channel.send(f"Timed out, aborting...")
                return
            except ValueError:
                await dm_channel.send(f"Invalid number, aborting...")
                return

            if existing_bid:
                log.info(f"request_bid - {member.display_name} - Updating bid from {existing_bid} to {amount}gp")
                BidTable.update_bid(auction_id=self.auction.auction_id, character_id=character_id, bid=amount)
            else:
                log.info(f"request_bid - {member.display_name} - Creating bid for {amount}gp")
                bid = BidTable.Row(auction_id=self.auction.auction_id, character_id=character_id,
                                   time=get_current_time(), bid=amount)
                BidTable.insert_row(bid)
            await dm_channel.send(f"Successfully created bid for item '**{self.auction.item}**' for **{amount}** gp.")

        @menus.button("\N{CROSS MARK}")
        async def stop_auction(self, payload: discord.RawReactionActionEvent):
            if payload.event_type.lower() != 'reaction_add':
                log.info(f"stop_auction - {payload.user_id} - performed invalid event {payload.event_type}")
                return

            member: discord.Member = payload.member
            name = member.display_name
            log.info(f"stop_auction - {name} - '{payload.event_type}' '{payload.emoji}' {self.auction.to_dict()}")

            dm_channel = await menu.get_dm_channel(member)
            if not (await self.bot.is_owner(member) or member_utils.has_role(member, self.stop_role, member.guild)):
                log.info(f"stop_auction - {name} - does not meet correct permissions to stop auction.")
                await dm_channel.send("You do not meet the correct permissions to stop an auction.")
                return

            m = menu.ConfirmMenu('Are you sure you would like to stop this auction?')
            await m.start(self.ctx, channel=dm_channel, wait=True, author=payload.member)

            if m.confirm:
                log.info(f"stop_auction - {name} - Chose to stop the auction")
                AuctionTable.update_end(auction_id=self.auction.auction_id, open=False)
                self.stop()
                if self.delete_message_after:
                    await self.message.delete()

                log.info(f"stop_auction - {name} - Stopped and deleted reaction menu. Displaying bids.")
                auction_cog: Auction = await get_cog(self.bot, dm_channel, 'Auction')
                await auction_cog.send_bids(auction=self.auction.auction_id, max_num=3, complete=True)

                msg = f"'**{name}**' successfully stopped auction for '{self.auction.item}'."
                await Connections.log_to_discord(self.ctx, msg)
                await dm_channel.send(msg)
            else:
                log.info(f"stop_auction - {name} - Did not stop the auction")
            return

    async def task_fetch_message(self, channel_id: int, message_id: int):
        log.debug(f"task - Searching in {channel_id} for {message_id}")
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return None
        try:
            return await channel.fetch_message(message_id)
        except discord.Forbidden as err:
            log.debug(f"task - discord.Forbidden exception thrown - {err}")
            return None
        except discord.NotFound as err:
            log.debug(f"task - discord.NotFound exception thrown - {err}")
            return None

    async def task_update_auction_listing(self, auction: AuctionTable.Row, message):
        if message is None:
            return
        log.info(f"task - Updating open auction message: {auction.item} - {auction.auction_id}")
        return await message.edit(embed=self.get_auction_listing_embed(auction))

    async def task_update_auction_status(self, auction: AuctionTable.Row, now, message):
        log.info(f"task - Checking status: now={now} end={auction.end}")
        if (auction.open is True) and (auction.end is not None) and (auction.end < now.replace(tzinfo=None)):
            log.info(f"task - Closing auction with expired end: {auction.item} - {auction.auction_id}")
            AuctionTable.update_end(auction_id=auction.auction_id, end=now, open=False)
            auction_cog: Auction = await get_cog(self.bot, None, 'Auction')
            await auction_cog.send_bids(auction=auction.auction_id, max_num=3, complete=True)
            await Connections.log_to_discord(self, f"Auction timer has completed for {auction.item}!")
            if message is not None:
                await message.delete()
            return True
        return False

    async def task_update_auction(self, auction: AuctionTable.Row, now: datetime.datetime):
        message = await self.task_fetch_message(auction.channel_id, auction.message_id)
        closed = await self.task_update_auction_status(auction, now, message)
        if not closed:
            await self.task_update_auction_listing(auction, message)

    @tasks.loop(seconds=30.0)
    async def update_auctions(self):
        log.debug(f"task - update_auctions - Running")
        if AuctionTable.exists():
            now = get_current_time()
            open_auctions = AuctionTable.select_open()
            if open_auctions:
                await asyncio.wait([self.task_update_auction(auction, now) for auction in open_auctions])
        log.debug(f"task - update_auctions - Done")


def setup(bot):
    bot.add_cog(Auction(bot))
