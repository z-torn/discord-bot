from datetime import datetime

from discord.ext import commands

from . import checks


class Bot_Utils(commands.Cog):
    """Some useful utils for the discord bot"""

    def __init__(self, bot):
        self.bot = bot
        self.bot.starttime = datetime.now()

    @checks.is_owner_or_coowner()
    @commands.command()
    async def shutdown(self, ctx):
        """: Shutdown the bot"""
        await ctx.channel.send("Shutting Down!")
        self.bot.reboot = False
        await self.bot.logout()
        await self.bot.close()

    # unload an extension
    @checks.is_owner_or_coowner()
    @commands.command()
    async def unload(self, ctx, cog: str = None):
        """: Unload an extension"""
        try:
            self.bot.unload_extension("bot.cogs." + cog)
            await ctx.channel.send("Unloaded Extension: " + cog)
        except:
            await ctx.channel.send("Invalid Extension Name!")

    # load an extension
    @checks.is_owner_or_coowner()
    @commands.command()
    async def load(self, ctx, cog: str = None):
        """: Load an extension"""
        try:
            self.bot.load_extension("bot.cogs." + cog)
            await ctx.channel.send("Loaded Extension: " + cog)
        except:
            await ctx.channel.send("Invalid Extension Name!")

    # reload an extension
    @checks.is_owner_or_coowner()
    @commands.command(name="reload")
    async def _reload(self, ctx, cog: str = None):
        """: Reload an extension"""
        try:
            extension = "bot.cogs." + cog
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
            await ctx.channel.send("Reloaded Extension: " + cog)
        except:
            await ctx.channel.send("Invalid Extension Name!")

    @commands.command()
    async def uptime(self, ctx):
        """: See how long I've been online"""
        time = datetime.now() - self.bot.starttime
        days = time.days
        hours, remainder = divmod(time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.channel.send(
            f"I've been online for {days} days, {minutes} min, {seconds} seconds!"
        )
