from discord.ext import commands
import sys
import importlib


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.group(name='reload_cog', invoke_without_command=True)
    async def _reload_cog(self, ctx, *, module):
        """Reloads a cog."""
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.group(name='reload_module', invoke_without_command=True)
    async def _reload_module(self, ctx, *, module):
        """Reloads a module."""
        try:
            actual_module = sys.modules[module]
        except KeyError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            try:
                importlib.reload(actual_module)
            except Exception as e:
                await ctx.send(f'{e.__class__.__name__}: {e}')
            else:
                await ctx.send('\N{OK HAND SIGN}')


def setup(bot):
    bot.add_cog(Admin(bot))
