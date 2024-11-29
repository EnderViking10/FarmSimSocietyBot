import discord
from discord import Member, Guild
from discord.ext import commands

from bot import logger
from utils.database import get_db, User, Bank, add_user


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

        # Adds the user to the database
        add_user(member)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        members = guild.members
        for member in members:
            if member.bot:
                continue
            if User.get_user(next(get_db()), member.id):
                continue
            add_user(member)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        if before.name == after.name:
            return
        User.update_username(next(get_db()), before.id, after.name)
        logger.info(f"{before.name} : {before.id} changed to {after.name} : {after.id}")


async def setup(bot):
    await bot.add_cog(Greetings(bot))
