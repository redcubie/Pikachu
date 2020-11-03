import discord, os, importlib
from discord.ext import commands
import configuration.variables as variables
import configuration.arrays as arrays
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=("P!", "p!"), case_insensitive=True, allowed_mentions=discord.AllowedMentions.none(), intents=intents)
bot.help_command = commands.DefaultHelpCommand(no_category="Other")

def is_staff_member(): # The staff member check.
    async def predicate(ctx):
        if ctx.author == ctx.guild.owner: return True
        for role in ctx.author.roles:
            if role.id in arrays.STAFFROLES:
                return True
        else: return False
    return commands.check(predicate)

@bot.event # The #bot-commands check.
async def on_message(ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        if ctx.content.lower().startswith("p!"):
            try:
                for role in ctx.author.roles:
                    if role.id in arrays.STAFFROLES:
                        await bot.process_commands(ctx)
                        return ctx.command.reset_cooldown(ctx)
                if ctx.channel.id in arrays.BOTCHANNELS: return await bot.process_commands(ctx)
            except AttributeError: pass # Doesn't really help, but I'll figure it out eventually.

@bot.command(hidden=True)
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def load(ctx, extension): # p!load
    "Loads the specified module into the bot.\nThis command is only usable by administrators."
    try:
        bot.load_extension(f"modules.{extension}")
        print(f"{extension.capitalize()} module has been loaded.")
        await ctx.send(f"{ctx.author.mention}, the {extension} module has been loaded.")
    except commands.ExtensionAlreadyLoaded: await ctx.send(f"{ctx.author.mention}, the {extension} module is already loaded.")
    except commands.ExtensionNotFound: await ctx.send(f"{ctx.author.mention}, the {extension} module does not exist.")

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def unload(ctx, extension): # p!unload
    "Unloads the specified module out of the bot.\nThis command is only usable by administrators."
    try:
        bot.unload_extension(f"modules.{extension}")
        print(f"{extension.capitalize()} module has been unloaded.")
        await ctx.send(f"{ctx.author.mention}, the {extension} module has been unloaded.")
    except commands.ExtensionNotLoaded: await ctx.send(f"{ctx.author.mention}, the {extension} module is already unloaded.")
    except commands.ExtensionNotFound: await ctx.send(f"{ctx.author.mention}, the {extension} module does not exist.")

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def reload(ctx, extension): # p!reload
    "Reloads the specified module into the bot.\nThis command is only usable by administrators."
    bot.reload_extension(f"modules.{extension}")
    print(f"{extension.capitalize()} module has been reloaded.")
    await ctx.send(f"{ctx.author.mention}, the {extension} module has been reloaded.")

@bot.command(aliases=["arrays"], hidden=True)
@commands.has_permissions(administrator=True)
async def array(ctx, action, array, variable = None): # p!key
    "Allows viewing and temporary editing of arrays.\nThis command is only usable by administrators."
    array = array.upper()
    try: result = getattr(arrays, array)
    except: result = None
    if variable != None:
        if variable.isdigit() == False:
            variable = variable.upper()
            try: variable = getattr(variables, variable)
            except: variable = None
        else: variable = int(variable)
    if action.lower() == "list":
        if result == None: return await ctx.send(f"{ctx.author.mention}, here is the list of contents in your specified array.\n```Input: {array}\nOutput: None```")
        else: await ctx.send(f"{ctx.author.mention}, here is the list of contents in your specified array.\n```Input: {array}\nOutput: {result}```")
    elif action.lower() == "add":
        if variable != None:
            try: result.append(variable)
            except: return await ctx.send(f"{ctx.author.mention}, an error has occurred updating the array. No changes have been made.\n```Input: {array}\nOutput: {result}```")
        else: return await ctx.send(f"{ctx.author.mention}, an error has occurred updating the array. No changes have been made.\n```Input: {array}\nOutput: {result}```")
        await ctx.send(f"{ctx.author.mention}, here is the array with the updated variables.\n```Input: {array} + {variable}\nOutput: {result}```")
    elif action.lower() == "remove":
        if variable != None:
            try: result.remove(variable)
            except: return await ctx.send(f"{ctx.author.mention}, an error has occurred updating the array. No changes have been made.\n```Input: {array}\nOutput: {result}```")
        else: return await ctx.send(f"{ctx.author.mention}, an error has occurred updating the array. No changes have been made.\n```Input: {array}\nOutput: {result}```")
        await ctx.send(f"{ctx.author.mention}, here is the array with the updated variables.\n```Input: {array} - {variable}\nOutput: {result}```")

@bot.command(aliases=["dictionaries", "key", "keys"], hidden=True)
@commands.has_permissions(administrator=True)
async def dictionary(ctx, variable, attribute = None): # p!key
    "Allows viewing of dictionary keys and values.\nThis command is only usable by administrators."
    variable = variable.upper()
    try: variable = getattr(variables, variable); result = arrays.ROLEINFORMATION.get(variable)
    except: result = None
    if attribute != None:
        attribute = attribute.capitalize()
        try: result = result.get(attribute)
        except: attribute = None
    if result == None: await ctx.send(f"{ctx.author.mention}, here are the keys and values for your specified dictionary.\n```Input: {variable}\nOutput: None```")
    elif attribute == None: await ctx.send(f"{ctx.author.mention}, here are the keys and values for your specified dictionary.\n```Input: {variable}\nOutput: {result}```")
    else: await ctx.send(f"{ctx.author.mention}, here are the keys and values for your specified dictionary.\n```Input: {variable}\nOutput: {attribute} = {result}```")

for filename in os.listdir("./modules"):
    if filename.endswith(".py"): bot.load_extension(f"modules.{filename[:-3]}")
    if filename.startswith("filters"): bot.unload_extension(f"modules.{filename[:-3]}")

bot.run(variables.BOTTOKEN)