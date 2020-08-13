import discord, os, importlib
from discord.ext import commands
import configuration.variables as variables
bot = commands.Bot(command_prefix="p!", case_insensitive=True)

@bot.event # The #bot-commands check.
async def on_message(ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        ownerRole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER)
        modRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR)
        if ctx.content.lower().startswith("p!"):
            try:
                if ownerRole in ctx.author.roles or modRole in ctx.author.roles: await bot.process_commands(ctx)
                elif ctx.channel.id == variables.BOTCOMMANDS or ctx.channel.id == variables.TRUSTEDCHAT or ctx.channel.id == variables.MODERATORCHAT or ctx.channel.id == variables.BOTDISCUSSION: await bot.process_commands(ctx)
            except AttributeError: pass # Doesn't really help, but I'll figure it out eventually.

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def load(ctx, extension): # p!load
    "Loads the specified cog into the bot."
    bot.load_extension(f"modules.{extension}")
    await ctx.send(f"The {extension} module has been loaded.")

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def unload(ctx, extension): # p!unload
    "Unloads the specified cog out of the bot."
    bot.unload_extension(f"modules.{extension}")
    await ctx.send(f"The {extension} cog has been unloaded.")

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def reload(ctx, extension): # p!reload
    "Reloads the specified cog into the bot."
    bot.reload_extension(f"modules.{extension}")
    await ctx.send(f"The {extension} module has been reloaded.")

for filename in os.listdir("./modules"):
    if filename.endswith(".py"): bot.load_extension(f"modules.{filename[:-3]}")
    if filename.startswith("filters"): bot.unload_extension(f"modules.{filename[:-3]}")

bot.run(variables.BOTTOKEN)