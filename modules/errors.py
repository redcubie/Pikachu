import discord, os, importlib
from discord.ext import commands

class Errors(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.Cog.listener() # Ignore wrong commands.
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound): pass
        if isinstance(error, commands.CommandOnCooldown): await ctx.send(f"{ctx.author.mention}, this command is on cooldown. Please try again in {error.retry_after:.0f} seconds.")
        if isinstance(error, commands.MissingPermissions): await ctx.send(f"{ctx.author.mention}, you don't have permission to use this command!")
        if isinstance(error, commands.CheckFailure): await ctx.send(f"{ctx.author.mention}, you don't have permission to use this command!")

def setup(bot): bot.add_cog(Errors(bot))