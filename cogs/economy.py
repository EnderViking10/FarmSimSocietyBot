from discord.ext import commands

from utils.database import Bank, get_db


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.hybrid_command(name="bank", description="The bank command")
    async def bank(self, ctx: commands.Context):
        member = ctx.author

        bank_account = Bank.get_bank(next(get_db), member.id)
        await ctx.reply(f"Your balance is {bank_account.balance}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Economy(bot))
