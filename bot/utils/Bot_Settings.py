import discord
from discord.ext import commands

from . import checks
from .Bot_Logging import human


class Bot_Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner_or_coowner()
    @commands.command(aliases=["sp"])
    async def set_prefix(self, ctx, *, prefix: str = "!"):
        """: Change the prefix for using bot commands. This will overwrite all prefixes."""
        prefix = prefix.split(" ")
        self.bot.command_prefix = prefix
        self.bot.settings.data["Bot Settings"]["command_prefix"] = prefix
        self.bot.settings.save()
        await ctx.channel.send(
            f'Commands will now be called with **{", ".join(prefix)}**'
        )

    @checks.is_owner_or_coowner()
    @commands.command(name="toggle_traceback")
    async def _print_traceback(self, ctx):
        """: Toggle printing the traceback for debugging"""
        self.bot.settings.data["traceback"] = not self.bot.settings.data["traceback"]
        self.bot.settings.save()
        await ctx.channel.send(
            f'Traceback is now: {human.get(self.bot.settings.data.get("traceback"))}'
        )

    @checks.is_owner_or_coowner()
    @commands.command()
    async def change_description(self, ctx, *, description: str = ""):
        """: Change the description for the bot displayed in the help menu"""
        self.bot.description = description
        self.bot.settings.data["Bot Settings"]["description"] = description
        self.bot.settings.save()
        await ctx.channel.send(f"The bots description is now ```{description}```")

    # pm_help attribute was removed, might make another command that does the same thing later
    # @checks.is_owner_or_coowner()
    # @commands.command()
    # async def toggle_help(self, ctx):
    #     """: Toggle how the bot send the help menu in a pm"""
    #     self.bot.pm_help = not self.bot.pm_help
    #     self.bot.settings.data["Bot Settings"]["pm_help"] = not self.bot.settings.data[
    #         "Bot Settings"
    #     ]["pm_help"]
    #     self.bot.settings.save()
    #     if self.bot.pm_help:
    #         await ctx.channel.send("The help menu will be sent as a PM now.")
    #     else:
    #         await ctx.channel.send("The help menu will be posted locally.")

    @checks.is_owner_or_coowner()
    @commands.command()
    async def add_coowner(self, ctx, member: discord.Member = None):
        """: Add a co-owner to your bot
        WARNING!! A coowner can use the same commands as the owner!"""
        config = self.bot.settings
        if member is None:
            return
        else:
            if "coowners" not in config.data:
                config.data["coowners"] = []
            if member.id not in config.data["coowners"]:
                config.data["coowners"].append(member.id)
                config.save()
                await ctx.channel.send(
                    f"{member.mention} has been added as a co-owner!"
                )

    @checks.is_owner_or_coowner()
    @commands.command()
    async def remove_coowner(self, ctx, member: discord.Member = None):
        ": Remove a co-owner from your bot"
        config = self.bot.settings
        if member is None:
            return
        else:
            if "coowners" not in config.data:
                config.data["coowners"] = []
            if member.id in config.data["coowners"]:
                config.data["coowners"].remove(member.id)
                config.save()
                await ctx.channel.send(
                    f"{member.mention} has been removed from co-owners!"
                )

    @checks.is_owner_or_coowner()
    @commands.command()
    async def coowners(self, ctx):
        ": Check the co-owners of a bot"
        coowners = ""
        for coowner in self.bot.settings.data.get("coowners", []):
            coowners += f"{ctx.bot.get_user(coowner)}\n"
        embed = discord.Embed(title="Co-Owners", description=coowners)
        await ctx.channel.send(embed=embed)
