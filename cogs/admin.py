from discord.ext import commands
from utils.permissions import has_any_role


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self._last_member = None

    @commands.hybrid_command(name="sync_commands", description="Sync commands")
    @has_any_role("Owner", "Co Owner")
    async def sync_commands(self, ctx: commands.Context):
        await self.bot.tree.sync()

        if ctx.interaction:
            await ctx.interaction.response.send_message(f"Commands have been synced")
        else:
            await ctx.reply(f"Commands have been synced")

    @sync_commands.error
    async def sync_commands_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CheckFailure):
            if ctx.interaction:
                await ctx.interaction.response.send_message(f"You must have all required roles to use this command.")
            else:
                await ctx.reply(f"You must have all required roles to use this command.")


async def setup(bot):
    await bot.add_cog(Admin(bot))
