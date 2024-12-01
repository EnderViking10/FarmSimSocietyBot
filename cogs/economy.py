import discord
from discord.ext import commands

from utils.database import Bank, get_db
from utils.fssapi import FSSAPI


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self._last_member = None

    @commands.hybrid_command(name="bank", description="The bank command")
    async def bank(self, ctx: commands.Context):
        member = ctx.author

        bank_account = Bank.get_bank(next(get_db()), member.id)
        if ctx.interaction:
            await ctx.interaction.response.send_message(f"Your balance is {bank_account.balance}", ephemeral=True)
        else:
            await ctx.author.send(f"Your balance is {bank_account.balance}")

    @commands.hybrid_group(name="transfer", description="Transfer money")
    async def transfer(self, ctx: commands.Context):
        if ctx.interaction:
            await ctx.interaction.response.send_message("Use a subcommand to transfer money")
        else:
            await ctx.reply("Use a subcommand to transfer money")

    @transfer.command(name="player", description="Transfer money to another player")
    async def player(self, ctx: commands.Context, user: discord.User, amount: int):
        db = next(get_db())
        author = ctx.author
        author_bank = Bank.get_bank(db, author.id)
        user_bank = Bank.get_bank(db, user.id)

        if user_bank is None:
            if ctx.interaction:
                await ctx.interaction.response.send_message(f"User {user.name} is not in the database", ephemeral=True)
            else:
                await author.send(f"User {user.name} is not in the database")
            return

        if author_bank.balance < amount:
            if ctx.interaction:
                await ctx.interaction.response.send_message(f"You have insufficient funds", ephemeral=True)
            else:
                await author.send(f"You have insufficient funds")
            return

        user_bank.balance += amount
        author_bank.balance -= amount
        db.commit()
        db.close()

        if ctx.interaction:
            await ctx.interaction.response.send_message(f"{amount} has been transfer to {user.name}", ephemeral=True)
        else:
            await author.send(f"{amount} has been transfer to {user.name}")

    @transfer.command(namer="server", description="Transfer money to a server")
    async def server(self, ctx: commands.Context, server: int, farm_name: str, amount: int):
        db = next(get_db())
        author = ctx.author
        author_bank = Bank.get_bank(db, author.id)

        if author_bank.balance < amount:
            if ctx.interaction:
                await ctx.interaction.response.send_message(f"You have insufficient funds", ephemeral=True)
            else:
                await author.send(f"You have insufficient funds")
            return

        fss_api = FSSAPI("http://192.168.1.207:8000")

        fss_api.send_command("add_money",
                             {
                                 "farm_name": farm_name,
                                 "amount": amount
                             })

        if ctx.interaction:
            await ctx.interaction.response.send_message(f"Transfer has been added to the queue", ephemeral=True)
        else:
            await author.send(f"Transfer has been added to the queue")


async def setup(bot):
    await bot.add_cog(Economy(bot))
