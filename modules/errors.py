import discord, os, importlib
from discord.ext import commands
import configuration.arrays as arrays

class Errors(commands.Cog):
    "When something goes wrong with the bot."
    def __init__(self, bot): self.bot = bot

    @commands.Cog.listener() # Ignore wrong commands.
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            for role in ctx.author.roles:
                if role.id in arrays.STAFFROLES:
                    return await ctx.reinvoke()
            return await ctx.send(f"{ctx.author.mention}, this command is on cooldown. Please try again in {error.retry_after:.0f} seconds.")
        elif isinstance(error, commands.MissingPermissions):
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"{ctx.author.mention}, you don't have permission to use this command.")
        elif isinstance(error, commands.CheckFailure):
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"{ctx.author.mention}, you don't have permission to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            ctx.command.reset_cooldown(ctx)
            await ctx.send(f"{ctx.author.mention}, you missed a required argument for this command.")
            return await ctx.send_help(ctx.command)
        elif isinstance(error, commands.BadArgument):
            ctx.command.reset_cooldown(ctx)
            await ctx.send(f"{ctx.author.mention}, you provided an invalid argument for this command.")
            return await ctx.send_help(ctx.command)

def setup(bot): bot.add_cog(Errors(bot))