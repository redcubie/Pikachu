import discord, os, importlib
from discord.ext import commands
import configuration.variables as variables
import configuration.arrays as arrays

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=("P!", "p!"), case_insensitive=True, allowed_mentions=discord.AllowedMentions.none(), intents=intents)
bot.help_command = commands.DefaultHelpCommand(no_category="Other")

def is_staff_member(): # The staff member permission check.
    async def predicate(ctx):
        for role in ctx.author.roles:
            if role.id in arrays.ROLEINFORMATION:
                info = arrays.ROLEINFORMATION.get(role.id)
                staffSetting = info.get("Staff")
                if staffSetting: return True
        else: return False
    return commands.check(predicate)

def check_staff_member(user): # The staff member status check.
    try:
        for role in user.roles:
            if role.id in arrays.ROLEINFORMATION:
                info = arrays.ROLEINFORMATION.get(role.id)
                staffSetting = info.get("Staff")
                if staffSetting: return True
        else: return False
    except: return False

@bot.event # The #bot-commands check.
async def on_message(ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        if ctx.content.lower().startswith("p!"):
            try:
                if check_staff_member(ctx.author):
                    await bot.process_commands(ctx)
                    return ctx.command.reset_cooldown(ctx)
                if ctx.channel.id in arrays.CHANNELINFORMATION:
                    info = arrays.CHANNELINFORMATION.get(ctx.channel.id)
                    botSetting = info.get("Bot")
                    if botSetting: return await bot.process_commands(ctx)
                    else: return None
            except AttributeError: pass # Doesn't really help, but I'll figure it out eventually.

@bot.command(hidden=True)
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def load(ctx, extension): # p!load
    "Loads the specified module into the bot.\nThis command is only usable by administrators."
    try:
        bot.load_extension(f"modules.{extension}")
        print(f"{extension.capitalize()} module has been loaded.")
        await ctx.reply(f"The {extension} module has been loaded.")
    except commands.ExtensionAlreadyLoaded: await ctx.reply(f"The {extension} module is already loaded.")
    except commands.ExtensionNotFound: await ctx.reply(f"The {extension} module does not exist.")

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def unload(ctx, extension): # p!unload
    "Unloads the specified module out of the bot.\nThis command is only usable by administrators."
    try:
        bot.unload_extension(f"modules.{extension}")
        print(f"{extension.capitalize()} module has been unloaded.")
        await ctx.reply(f"The {extension} module has been unloaded.")
    except commands.ExtensionNotLoaded: await ctx.reply(f"The {extension} module is already unloaded.")
    except commands.ExtensionNotFound: await ctx.reply(f"The {extension} module does not exist.")

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def reload(ctx, extension): # p!reload
    "Reloads the specified module into the bot.\nThis command is only usable by administrators."
    bot.reload_extension(f"modules.{extension}")
    print(f"{extension.capitalize()} module has been reloaded.")
    await ctx.reply(f"The {extension} module has been reloaded.")

@bot.command(aliases=["keys", "key"], hidden=True)
@commands.has_permissions(administrator=True)
async def dictionary(ctx, dictionary, variable, attribute = None, setting: bool = None): # p!key
    "Allows viewing and editing of dictionary keys and values.\nValid dictionaries include \"role\" and \"channel\".\nAny attribute of a variable using boolean settings can be edited.\nThis command is only usable by administrators."
    if dictionary.lower() == "role" or dictionary.upper() == "ROLEINFORMATION":
        dictionary = "ROLEINFORMATION"
        try: variable = getattr(variables, variable.upper()); result = arrays.ROLEINFORMATION.get(variable)
        except: result = None
    elif dictionary.lower() == "channel" or dictionary.upper() == "CHANNELINFORMATION":
        dictionary = "CHANNELINFORMATION"
        try:
            variable = getattr(variables, variable.upper()); result = arrays.CHANNELINFORMATION.get(variable)
        except: result = None
    else: return await ctx.reply(f"The dictionary you have specified is not a valid option.")
    if attribute != None:
        attribute = attribute.capitalize()
        try: result = result.get(attribute)
        except: attribute = None
    if setting != None:
        if dictionary == "ROLEINFORMATION": result = arrays.ROLEINFORMATION.get(variable)
        elif dictionary == "CHANNELINFORMATION": result = arrays.CHANNELINFORMATION.get(variable)
        if not isinstance(result[attribute], bool): return await ctx.reply(f"This value tied to the role cannot be edited.")
        else: result[attribute] = setting
        return await ctx.reply(f"Here are the keys and values for your specified dictionary.\n```Input: {variable}\nOutput: {attribute} = {result[attribute]}```")
    if result == None: await ctx.reply(f"Here are the keys and values for your specified dictionary.\n```Input: {variable}\nOutput: None```")
    elif attribute == None: await ctx.reply(f"Here are the keys and values for your specified dictionary.\n```Input: {variable}\nOutput: {result}```")
    else: await ctx.reply(f"Here are the keys and values for your specified dictionary.\n```Input: {variable}\nOutput: {attribute} = {result}```")

for filename in os.listdir("./modules"):
    if filename.endswith(".py"): bot.load_extension(f"modules.{filename[:-3]}")

bot.run(variables.BOTTOKEN)