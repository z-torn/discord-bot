import discord
from discord.ext import commands

from . import checks
from .bot_logging_cog import humanize


class Bot_Settings(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @checks.is_owner_or_coowner()
    @commands.command(aliases=["sp"])
    async def set_prefix(self, ctx: commands.Context, *, prefix: str = "!"):
        """: Change the prefix for using bot commands. This will overwrite all prefixes."""
        prefix = prefix.split(" ")
        self.bot.command_prefix = prefix
        self.bot.config.data["BOT"]["command_prefix"] = prefix
        self.bot.config.save()
        await ctx.channel.send(
            f'Commands will now be called with **{", ".join(prefix)}**'
        )

    @checks.is_owner_or_coowner()
    @commands.command(name="toggle_traceback")
    async def _print_traceback(self, ctx: commands.Context):
        """: Toggle printing the traceback for debugging"""
        self.bot.config.data["TRACEBACK"] = not self.bot.config.data["TRACEBACK"]
        self.bot.config.save()
        await ctx.channel.send(
            f'Traceback is now: {humanize.get(self.bot.config.data.get("TRACEBACK"))}'
        )

    @checks.is_owner_or_coowner()
    @commands.command()
    async def change_description(self, ctx: commands.Context, *, description: str = ""):
        """: Change the description for the bot displayed in the help menu"""
        self.bot.description = description
        self.bot.config.data["BOT"]["description"] = description
        self.bot.config.save()
        await ctx.channel.send(f"The bots description is now ```{description}```")

    @checks.is_owner_or_coowner()
    @commands.command()
    async def toggle_help(self, ctx: commands.Context):
        """: Toggle how the bot send the help menu in a pm"""
        dm_help = not self.bot.help_command.dm_help
        self.bot.help_command = commands.DefaultHelpCommand(dm_help=dm_help)
        self.bot.config.data["BOT"]["dm_help"] = dm_help
        self.bot.config.save()
        if dm_help:
            await ctx.channel.send("The help menu will be sent as a PM now.")
        else:
            await ctx.channel.send("The help menu will be posted locally.")

    @checks.is_owner_or_coowner()
    @commands.command()
    async def add_coowner(self, ctx: commands.Context, member: discord.Member = None):
        """: Add a co-owner to your bot
        WARNING!! A coowner can use the same commands as the owner!"""
        if member is None:
            return
        else:
            config = self.bot.config
            if "coowners" not in config.data.get("BOT"):
                config.data["BOT"]["coowners"] = []
            if member.id not in config.data["BOT"]["coowners"]:
                config.data["BOT"]["coowners"].append(member.id)
                config.save()
                await ctx.channel.send(
                    f"{member.mention} has been added as a co-owner!"
                )

    @checks.is_owner_or_coowner()
    @commands.command()
    async def remove_coowner(
        self, ctx: commands.Context, member: discord.Member = None
    ):
        ": Remove a co-owner from your bot"
        if member is None:
            return
        else:
            config = self.bot.config
            if "coowners" not in config.data["BOT"]:
                config.data["BOT"]["coowners"] = []
            if member.id in config.data["BOT"]["coowners"]:
                config.data["BOT"]["coowners"].remove(member.id)
                config.save()
                await ctx.channel.send(
                    f"{member.mention} has been removed from co-owners!"
                )

    @checks.is_owner_or_coowner()
    @commands.command()
    async def coowners(self, ctx: commands.Context):
        ": Check the co-owners of a bot"
        coowners = ""
        for coowner in self.bot.config.data["BOT"].get("coowners", []):
            coowners += f"{ctx.bot.get_user(coowner)}\n"
        embed = discord.Embed(title="Co-Owners", description=coowners)
        await ctx.channel.send(embed=embed)
