from discord.ext import commands
import discord


# connecting to discord
Token = open("Credentials\DiscordAPI.txt").read()
bot = commands.Bot(command_prefix="$", description="The Lost World Helper Bot")


# List cog files then load them in
initial_extensions = ['cogs.DM Commands', 'cogs.Utility Commands',
                      'cogs.Mod_Commands', 'cogs.Player_Menu_Commands']
#

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


# Auto response if user doesnt have role
@bot.event
async def on_command_error(message, error):
    if isinstance(error, commands.errors.CheckFailure):
        await message.send('You do not have the correct role for this command.')
    else:
        await message.send(error)


# what the bot does when its turned on
@bot.event
async def on_ready():
    game = discord.Game("Assuming Direct Control")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print('Logged in')


bot.run(Token, bot=True, reconnect=True)
