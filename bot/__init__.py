import sys
import time
from pathlib import Path

import discord
import jthon
import yaml
from aiohttp import ClientSession
from discord.ext import commands
from orator import DatabaseManager

from bot.utils import MakeSettings
from bot.utils.basic_bot import BasicBot

from .utils.clean_config import CleanConfig

# Check the installed python version
if sys.version_info <= (3, 6):
    print("Need Python 3.6 or greater to run this bot. Exiting...")
    time.sleep(3)
    sys.exit()


__version__ = "0.7"

# Basic invite link for your bot. Specify more permissions on the discord.app site
invite_link = "https://discordapp.com/api/oauth2/authorize?client_id={}&scope=bot"

# Get the bot settings or create them if they arenot already made
settings = MakeSettings(settings="./bot/database/json/").get_settings()

# Load the config file
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    config = CleanConfig(config).cleaned

# Create a discord bot instance
initial = settings.data.get("Bot Settings")
bot_instance = BasicBot(
    **initial,
    help_command=commands.DefaultHelpCommand(dm_help=initial.get("pm_help")),
    db=DatabaseManager(config.get("databases")),
    settings=settings,
)


# Basic message to console when the bot is ready
@bot_instance.event
async def on_ready():
    print(f"Logged in as: {bot_instance.user.name}")
    print(f"With user ID: {bot_instance.user.id}")
    print(f"Invite Link: {invite_link.format(bot_instance.user.id)}\n")


# pull all potential extensions from the extensions folder
def collect_extensions():
    files = Path("bot", "extensions").rglob("*.py")
    for file in files:
        if "__init__" not in file.name:
            yield file.as_posix()[:-3].replace("/", ".")


# load cogs and commands from the bot.extensions folder
def load_extensions():
    for extension in collect_extensions():
        try:
            bot_instance.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}\n{e}")
    print()


def run():
    # Load bot utilities if enabled in the config
    utils = config.get("config", {}).get("utils", {})
    from .utils import Bot_Logging, Bot_Settings, Bot_Utils

    if utils.get("bot_logging", True):
        bot_instance.add_cog(Bot_Logging.Bot_Logging(bot_instance))
    if utils.get("bot_settings", True):
        bot_instance.add_cog(Bot_Settings.Bot_Settings(bot_instance))
    if utils.get("bot_utils", True):
        bot_instance.add_cog(Bot_Utils.Bot_Utils(bot_instance))

    load_extensions()

    # Run the bot
    bot_instance.run(config.get("discord").get("TOKEN"))
