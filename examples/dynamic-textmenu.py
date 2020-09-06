from discord.ext import commands
from cogs.utils import textmenus


description = "Simple textmenu example"
bot = commands.Bot(command_prefix='?', description=description)


class MainMenu(textmenus.Menu):
    """
    Definition of main menu object
    """
    def get_initial_message(self):
        return "Welcome to the main menu."

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

    @m.submenu('Menu added while in a command')
    async def additional_menu(menu, payload):
        await menu.ctx.channel.send("This is an example of a dynamically added menu.")

    await m.start(ctx)


# bot.run('token')
import secrets
bot.run(secrets.token)
