import discord

def has_role(member: discord.Member, role_name: str, guild: discord.Guild):
    return True if discord.utils.find(lambda r: r.name == role_name, guild.roles) in member.roles else False
