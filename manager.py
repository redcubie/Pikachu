import discord, os, importlib
from discord.ext import commands
import configuration.variables as variables
bot = commands.Bot(command_prefix="p!", case_insensitive=True)

@bot.event # The #bot-commands check.
async def on_message(ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        ownerrole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER)
        modrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR)
        if ctx.content.lower().startswith("p!"):
            try:
                if ownerrole in ctx.author.roles or modrole in ctx.author.roles: await bot.process_commands(ctx)
                elif ctx.channel.id == variables.BOTCOMMANDS or ctx.channel.id == variables.MODERATORCHAT or ctx.channel.id == variables.BOTDISCUSSION: await bot.process_commands(ctx)
            except AttributeError: pass # Doesn't really help, but I'll figure it out eventually.

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def load(ctx, extension): # p!load
    bot.load_extension(f"modules.{extension}")
    await ctx.send(f"The {extension} module has been loaded.")

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def unload(ctx, extension): # p!unload
    bot.unload_extension(f"modules.{extension}")
    await ctx.send(f"The {extension} cog has been unloaded.")

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def reload(ctx, extension): # p!reload
    bot.unload_extension(f"modules.{extension}")
    bot.load_extension(f"modules.{extension}")
    await ctx.send(f"The {extension} module has been reloaded.")

for filename in os.listdir("./modules"):
    if filename.endswith(".py"): bot.load_extension(f"modules.{filename[:-3]}")

bot.run(variables.BOTTOKEN)