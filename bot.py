import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.database import init_db

error_handler = logging.FileHandler("bot_errors.log")
error_handler.setLevel(logging.ERROR)

info_handler = logging.FileHandler("bot_info.log")
info_handler.setLevel(logging.INFO)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[error_handler, info_handler]
)

# Logger for bot-specific messages
logger = logging.getLogger('FarmLifeBot')

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("COMMAND_PREFIX", "!")

# Intents
intents = discord.Intents.all()
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    # Prints the hello message for server side shit
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")

    init_db()
    logger.info(f"Database successfully initialized")

    # Load all cogs in the cogs/ folder
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"Loaded {cog_name}")
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")


@bot.event
async def on_command(ctx):
    logger.info(
        f"{ctx.author} : {ctx.author.id} ran {ctx.command} in channel '{ctx.channel}'."
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Type `!help` for a list of commands.")
    else:
        logger.error(f"Error in command {ctx.command}: {error}")


if __name__ == "__main__":
    bot.run(TOKEN)
