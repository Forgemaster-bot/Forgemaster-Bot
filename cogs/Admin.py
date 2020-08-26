from discord.ext import commands
import Crafting.Parser


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.group(name='reload', hidden=True, invoke_without_command=True)
    async def _reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.group(name='refresh_recipe', hidden=True, invoke_without_command=True)
    async def _refresh_recipe(self, ctx, *, label):
        """Refreshes global recipes for label."""
        try:
            Crafting.Parser.refresh_file(label)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')


def setup(bot):
    bot.add_cog(Admin(bot))
