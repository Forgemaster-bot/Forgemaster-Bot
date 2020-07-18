from discord.ext import commands
import Connections
import discord
import time
import os
# os.environ['TDSVER'] = '8.0'

# connecting to discord
Token = open(os.path.join('Credentials','DiscordAPI.txt')).read()
bot = commands.Bot(command_prefix="$", description="The Lost World Helper Bot")


# List cog files then load them in
initial_extensions = ['cogs.DM Commands', 'cogs.Utility Commands',
                      'cogs.Mod_Commands', 'cogs.Player_Menu_Commands']


if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


# Auto response if user doesnt have role
@bot.event
async def on_command_error(message, error):
    if isinstance(error, commands.errors.CheckFailure):
        await message.send('You do not have the correct role for this command.')

    else:
        discord_id = message.author.id
        discord_command = message.message.clean_content
        Connections.sql_log_error(discord_id, discord_command, error.args[0])
        await message.send(error)


# what the bot does when its turned on
@bot.event
async def on_ready():
    game = discord.Game("Assuming Direct Control")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print('Logged in at {}'.format(time.strftime('%Y-%m-%d %H:%M:%S')))


bot.run(Token, bot=True, reconnect=True)
