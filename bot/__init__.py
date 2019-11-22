import sys
import time
from pathlib import Path

from .utils.clean_config import CleanConfig

# Check the installed python version
if sys.version_info <= (3, 6):
    print("Need Python 3.6 or greater to run this bot. Exiting...")
    time.sleep(3)
    sys.exit()

import discord
import jthon
import yaml
from aiohttp import ClientSession
from discord.ext import commands
from orator import DatabaseManager

from bot.utils import Bot_Logging, Bot_Settings, Bot_Utils, MakeSettings

__version__ = "0.5"

# Bot settings save path
settings_path = "./bot/database/json/"

# Basic invite link for your bot. Specify more permissions on the discord.app site
invite_link = "https://discordapp.com/api/oauth2/authorize?client_id={}&scope=bot"

# Get the bot settings or create them if they arenot already made
settings = MakeSettings(settings=settings_path).get_settings()

# Load the config file
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    config = CleanConfig(config).cleaned

# Create a discord bot instance
bot_instance = commands.Bot(**settings.data.get("Bot Settings"))

# Basic message to console when the bot has loaded successfully
@bot_instance.event
async def on_ready():
    print(f"Logged in as: {bot_instance.user.name}")
    print(f"With user ID: {bot_instance.user.id}")
    print(f"Invite Link: {invite_link.format(bot_instance.user.id)}")


# pull all extensions from the cogs folder
def load_extensions():
    files = Path("bot/extensions").rglob("*.py")
    extensions = (
        f"{file.relative_to(Path()).with_suffix('')}".replace("\\", ".")
        for file in files
        if "__init__" not in file.name
    )
    # load cogs and commands from the bot.extensions folder
    for extension in extensions:
        # print(extension)
        try:
            bot_instance.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}\n{e}")


def run():
    # Create an aiohttp session that cogs can use
    bot_instance.aiohttp = ClientSession(loop=bot_instance.loop)
    bot_instance.settings = settings

    # Load bot utilities
    bot_instance.add_cog(Bot_Logging.Bot_Logging(bot_instance))
    bot_instance.add_cog(Bot_Settings.Bot_Settings(bot_instance))
    bot_instance.add_cog(Bot_Utils.Bot_Utils(bot_instance))

    load_extensions()

    # Run the bot
    bot_instance.run(config.get("discord").get("TOKEN"))
