from discord.ext import commands
from cogs.utils import textmenus


description = "Nested textmenus example"
bot = commands.Bot(command_prefix='?', description=description)


class CharacterSheetMenu(textmenus.Menu):
    timed_out = False

    def get_initial_message(self):
        details = "\n".join(["**Name:** Guin", "**Class:**", "**Stats:**", "**Feats:**", "**Professions:**"])
        return f"Welcome to your character sheet.\n{details}"

    def finalize(self, timed_out):
        self.timed_out = timed_out

    @textmenus.submenu('View your inventory')
    async def view_inventory(self, payload):
        await self.ctx.channel.send("Your inventory would be listed here.")

    @textmenus.submenu('View your spells')
    async def view_spells(self, payload):
        await self.ctx.channel.send("Your spells would be listed here.")


class WorkshopMenu(textmenus.Menu):
    timed_out = False

    def get_initial_message(self):
        return "Welcome to the workshop."

    def finalize(self, timed_out):
        self.timed_out = timed_out

    @textmenus.submenu('Create a mundane item')
    async def craft_mundane(self, payload):
        await self.ctx.channel.send("Your mundane recipes would be listed here.")

    @textmenus.submenu('Create a consumable item')
    async def craft_consumable(self, payload):
        await self.ctx.channel.send("Your consumable recipes would be listed here.")


class MarketMenu(textmenus.Menu):
    timed_out = False

    def get_initial_message(self):
        return "Welcome to the market."

    def finalize(self, timed_out):
        self.timed_out = timed_out

    @textmenus.submenu('Buy items from the market')
    async def buy_item_menu(self, payload):
        await self.ctx.channel.send("This would list the menu for buying items from the market")

    @textmenus.submenu('Sell items on the market')
    async def sell_item_menu(self, payload):
        await self.ctx.channel.send("This would list the menu for selling items on the market")


class MainMenu(textmenus.Menu):
    """
    Definition of main menu object
    """
    timed_out = False

    def get_initial_message(self):
        return "Welcome to the main menu."

    def finalize(self, timed_out):
        self.timed_out = timed_out

    @textmenus.submenu('Character Sheet')
    async def character_sheet(self, payload):
        await CharacterSheetMenu().start(self.ctx)

    @textmenus.submenu('Workshop')
    async def workshop(self, payload):
        await WorkshopMenu().start(self.ctx)

    @textmenus.submenu('Market')
    async def market(self, payload):
        await MarketMenu().start(self.ctx)


@bot.command()
async def menu_example(ctx):
    m = MainMenu()
    await m.start(ctx)


@bot.command()
async def looping_menu_example(ctx):
    def get_exit_reason(menu):
        if isinstance(menu.exception, textmenus.ExitException):
            return "'exit' received."
        if isinstance(menu.exception, textmenus.StopException):
            return "'stop' received."
        if menu.timed_out:
            return "Menu timed out."
        return ""

    m = MainMenu()
    await m.start(ctx)
    await ctx.channel.send(f"Closing menu. {get_exit_reason(m)}")


# bot.run('token')
import secrets
bot.run(secrets.token)
