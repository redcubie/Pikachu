import discord, os, importlib
from discord.ext import commands
import configuration.variables as variables; import configuration.arrays as arrays
bot = commands.Bot(command_prefix=("P!", "p!"), case_insensitive=True, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))
bot.remove_command('help')

@bot.event # The #bot-commands check.
async def on_message(message):
    if not isinstance(message.channel, discord.channel.DMChannel) and message.content.lower().startswith("p!"):
        try:
            if message.channel.id in arrays.BOTCHANNELS or any(item in arrays.STAFFROLES for item in message.author.roles):
                await bot.process_commands(message)
        except AttributeError:
            pass # Doesn't really help, but I'll figure it out eventually.

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