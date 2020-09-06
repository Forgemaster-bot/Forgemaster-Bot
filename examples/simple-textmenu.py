from discord.ext import commands
from cogs.utils import textmenus


description = "Simple textmenu example"
bot = commands.Bot(command_prefix='?', description=description)


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
        await self.ctx.channel.send("Your character sheet would be listed here.")

    @textmenus.submenu('Workshop')
    async def workshop(self, payload):
        await self.ctx.channel.send("The workshop would be here.")

    @textmenus.submenu('Market')
    async def market(self, payload):
        await self.ctx.channel.send("The market would be here.")


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

    m = MainMenu(stop_on_first=False)
    await m.start(ctx, wait=True)
    await ctx.channel.send(f"Closing menu. {get_exit_reason(m)}")


# bot.run('token')
import secrets
bot.run(secrets.token)

