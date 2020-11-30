import sys
import time
from pathlib import Path

import discord
import jthon
from discord.ext import commands

# Check the installed python version
if sys.version_info <= (3, 6):
    print("Need Python 3.6 or greater to run this bot. Exiting...")
    time.sleep(3)
    sys.exit()


__version__ = "0.8.0"

# Basic invite link for your bot. Specify more permissions on the discord.app site
invite_link = "https://discordapp.com/api/oauth2/authorize?client_id={}&scope=bot"

CONFIG = jthon.load("config")

# reserved bot attributes
reserved = ["config"] + CONFIG.data.get("RESERVED")


help_command = commands.DefaultHelpCommand(
    dm_help=CONFIG.data.get("BOT").get("dm_help")
)


class Bot(commands.Bot):
    def __setattr__(self, name, value):
        if name in reserved and hasattr(self, name):
            raise AttributeError(f"{name} is a reserved attribute")
        return super().__setattr__(name, value)


# Sets default intents, reference https://discordpy.readthedocs.io/en/latest/intents.html?highlight=gateway%20intents
intents = CONFIG.data.get("INTENTS")
INTENTS = discord.Intents.default() if not intents else discord.Intents(**intents)

INSTANCE = Bot(**CONFIG.data.get("BOT"), help_command=help_command, intents=INTENTS)

INSTANCE.config = CONFIG

# Basic message to console when the bot is ready
@INSTANCE.event
async def on_ready():
    print(f"Logged in as: {INSTANCE.user.name}")
    print(f"With user ID: {INSTANCE.user.id}")
    print(f"Invite Link: {invite_link.format(INSTANCE.user.id)}\n")


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
            INSTANCE.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}\n{e}")
    print()


def run():
    # Load bot utilities if enabled in the config
    utils = CONFIG.data.get("UTILS", {})
    from .utils import Bot_Logging, Bot_Settings, Bot_Utils

    if utils.get("bot_logging", True):
        INSTANCE.add_cog(Bot_Logging(INSTANCE))
    if utils.get("bot_settings", True):
        INSTANCE.add_cog(Bot_Settings(INSTANCE))
    if utils.get("bot_utils", True):
        INSTANCE.add_cog(Bot_Utils(INSTANCE))

    load_extensions()

    # Run the bot
    INSTANCE.run(CONFIG.data.get("TOKEN"))
