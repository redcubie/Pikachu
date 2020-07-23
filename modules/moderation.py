import discord, os, importlib, asyncio, pymongo, re, typing
from discord.ext import commands; from pymongo import MongoClient
import configuration.variables as variables; import configuration.arrays as arrays

class FindMember(commands.IDConverter):
    async def convert(self, ctx, argument) -> discord.User:
        match = self._get_id_match(argument) or re.match(r'<@!?([0-9]+)>$', argument)
        if match == None and ctx.guild:
            result = ctx.guild.get_member_named(argument)
        else:
            userid = int(match.group(1))
            result = ctx.guild.get_member(userid) or await ctx.bot.fetch_user(userid) if ctx.guild else await ctx.bot.fetch_user(userid)
        if result == None:
            await ctx.send(f"{ctx.author.mention}, this user cannot be found. Please specify the correct user.")
        return result

class Moderation(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(variables.SERVERBOT, variables.SERVEROWNER, variables.SERVERMODERATOR) # Roles @Server Bot, @Server Owner, @Server Moderator.
    async def checkactivity(self, ctx, days = 30): # p!checkactivity
        if days < 1:
            await ctx.send(f"{ctx.author.mention}, the minimum allowed days is 1.")
            return
        if days > 30:
            await ctx.send(f"{ctx.author.mention}, the maximum allowed days is 30.")
            return
        async with ctx.channel.typing():
            count = await ctx.guild.estimate_pruned_members(days=days)
            await asyncio.sleep(1)
            if days == 1:
                await ctx.send(f"{ctx.author.mention}, over the past {days} day, approximately {ctx.guild.member_count-count:,} members were counted as active.")
            else:
                await ctx.send(f"{ctx.author.mention}, over the past {days} days, approximately {ctx.guild.member_count-count:,} members were counted as active.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1): # p!clear
        deleted = await ctx.channel.purge(limit=amount+1)
        logchannel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        if amount != 0:
            await logchannel.send(f"{ctx.author} ({ctx.author.id}) has cleared {len(deleted)-1} messages in {ctx.channel}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason): # p!warn
        ownerrole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        logchannel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        if ownerrole in member.roles or modrole in member.roles or botrole in member.roles:
            await ctx.send(f"{ctx.author.mention}, this user cannot be warned in the server.")
        else:
            if collection.count_documents({"_id": member.id}, limit = 1) == 0:
                post = {"_id": member.id, "Warn 1": None, "Warn 2": None, "Warn 3": None}
                collection.insert_one(post)
                results = collection.find({"_id": member.id})
                for result in results:
                    checkwarn1 = result["Warn 1"]
                    checkwarn2 = result["Warn 2"]
                    checkwarn3 = result["Warn 3"]
                if checkwarn1 == None:
                    collection.update_one({"_id": member.id}, {"$set":{"Warn 1": reason}})
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 1:", value=reason, inline=False)
                    try: await member.send(f"You have been warned in {ctx.guild.name} for \"{reason}\". This is your first warning and only warning without an automatic punishment. Please reconsider the rules before participating in the server. Your next offense will result in an automatic kick.")
                    except discord.errors.Forbidden: pass
                    await logchannel.send(f"{ctx.author} ({ctx.author.id}) has given a warning to {member.mention} ({member.id}).", embed=embed)
                    await ctx.send(f"{ctx.author.mention}, a warning has been given to {member.mention}.")
            else:
                results = collection.find({"_id": member.id})
                for result in results:
                    checkwarn1 = result["Warn 1"]
                    checkwarn2 = result["Warn 2"]
                    checkwarn3 = result["Warn 3"]
                if checkwarn2 == None and checkwarn1 != None:
                    collection.update_one({"_id": member.id}, {"$set":{"Warn 2": reason}})
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 2:", value=reason, inline=False)
                    try: await member.send(f"You have been warned in {ctx.guild.name} for \"{reason}\". This is your second warning, therefore you have automatically been kicked from the server. Please reconsider the rules before participating in the server. Your next offense will result in an automatic ban.")
                    except discord.errors.Forbidden: pass
                    await logchannel.send(f"{ctx.author} ({ctx.author.id}) has given a warning to {member.mention} ({member.id}).", embed=embed)
                    await member.kick(reason=f"{checkwarn1}, {reason}")
                    await ctx.send(f"{ctx.author.mention}, a warning has been given to {member.mention}. A kick has been initiated automatically.")
                elif checkwarn3 == None and checkwarn2 != None:
                    collection.update_one({"_id": member.id}, {"$set":{"Warn 3": reason}})
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 3:", value=reason, inline=False)
                    try: await member.send(f"You have been warned in {ctx.guild.name} for \"{reason}\". This is your third warning, therefore you have automatically been banned from the server. Please contact a staff member if you feel you have been wrongfully punished.")
                    except discord.errors.Forbidden: pass
                    await logchannel.send(f"{ctx.author} ({ctx.author.id}) has given a warning to {member.mention} ({member.id}).", embed=embed)
                    await member.ban(reason=f"{checkwarn1}, {checkwarn2}, {reason}")
                    await ctx.send(f"{ctx.author.mention}, a warning has been given to {member.mention}. A ban has been initiated automatically.")
                elif checkwarn3 != None and checkwarn2 != None:
                    await ctx.send(f"{ctx.author.mention}, there are too many warnings recorded for {member.mention}.")
                    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def pardon(self, ctx, member: discord.Member): # p!warn
        ownerrole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        logchannel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        if ownerrole in member.roles or modrole in member.roles or botrole in member.roles:
            await ctx.send(f"{ctx.author.mention}, this user cannot be warned in the server.")
        else:
            if collection.count_documents({"_id": member.id}, limit = 1) == 0:
                await ctx.send(f"{ctx.author.mention}, there are no warnings recorded for {member.mention}.")
            else:
                results = collection.find({"_id": member.id})
                for result in results:
                    checkwarn1 = result["Warn 1"]
                    checkwarn2 = result["Warn 2"]
                    checkwarn3 = result["Warn 3"]
                if checkwarn3 != None:
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 3:", value=checkwarn3, inline=False)
                    await logchannel.send(f"{ctx.author} ({ctx.author.id}) has pardoned a warning from {member.mention} ({member.id}).", embed=embed)
                    collection.update_one({"_id": member.id}, {"$set":{"Warn 3": None}})
                    await ctx.send(f"{ctx.author.mention}, the latest warning given to {member.mention} has been removed successfully.")
                elif checkwarn2 != None and checkwarn3 == None:
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 2:", value=checkwarn2, inline=False)
                    await logchannel.send(f"{ctx.author} ({ctx.author.id}) has pardoned a warning from {member.mention} ({member.id}).", embed=embed)
                    collection.update_one({"_id": member.id}, {"$set":{"Warn 2": None}})
                    await ctx.send(f"{ctx.author.mention}, the latest warning given to {member.mention} has been removed successfully.")
                elif checkwarn1 != None and checkwarn2 == None:
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 1:", value=checkwarn1, inline=False)
                    await logchannel.send(f"{ctx.author} ({ctx.author.id}) has pardoned a warning from {member.mention} ({member.id}).", embed=embed)
                    collection.delete_one({"_id": member.id})
                    await ctx.send(f"{ctx.author.mention}, the latest warning given to {member.mention} has been removed successfully.")
                else:
                    await ctx.send(f"{ctx.author.mention}, there are no warnings recorded for {member.mention}.")
                    
    @commands.command()
    @commands.guild_only()
    async def listwarn(self, ctx, member: discord.Member = None): # p!listwarn
        ownerrole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        if ownerrole in ctx.author.roles or modrole in ctx.author.roles or botrole in ctx.author.roles:
            if member == None: member = ctx.author
            if ownerrole in member.roles or modrole in member.roles or botrole in member.roles:
                await ctx.send(f"{ctx.author.mention}, this user cannot be warned in the server.")
            else:
                if collection.count_documents({"_id": member.id}, limit = 1) == 0:
                    if member == ctx.author: await ctx.send(f"{ctx.author.mention}, there are no warnings recorded.")
                    else: await ctx.send(f"{ctx.author.mention}, there are no warnings recorded for {member.mention}.")
                else:
                    results = collection.find({"_id": member.id})
                    for result in results:
                        checkwarn1 = result["Warn 1"]
                        checkwarn2 = result["Warn 2"]
                        checkwarn3 = result["Warn 3"]
                    embed = discord.Embed(color=0xff8080)
                    if checkwarn1 != None: embed.add_field(name="Warning 1:", value=checkwarn1, inline=False)
                    if checkwarn2 != None: embed.add_field(name="Warning 2:", value=checkwarn2, inline=False)
                    if checkwarn3 != None: embed.add_field(name="Warning 3:", value=checkwarn3, inline=False)
                    embed.set_footer(text="To appeal a warn, speak to a staff member.")
                    await ctx.send(embed=embed)
        else: # This is an example of horrible Python coding. I plan to simplify it later on, but as of now, it works at least.
            if member != None:
                await ctx.send(f"{ctx.author.mention}, using this command on others is only allowed for staff members.")
            else:
                member = ctx.author
                if ownerrole in member.roles or modrole in member.roles or botrole in member.roles:
                    await ctx.send(f"{ctx.author.mention}, this user cannot be warned in the server.")
                else:
                    if collection.count_documents({"_id": member.id}, limit = 1) == 0:
                        await ctx.send(f"{ctx.author.mention}, there are no warnings recorded for {member.mention}.")
                    else:
                        results = collection.find({"_id": member.id})
                        for result in results:
                            checkwarn1 = result["Warn 1"]
                            checkwarn2 = result["Warn 2"]
                            checkwarn3 = result["Warn 3"]
                        embed = discord.Embed(color=0xff8080)
                        if checkwarn1 != None: embed.add_field(name="Warning 1:", value=checkwarn1, inline=False)
                        if checkwarn2 != None: embed.add_field(name="Warning 2:", value=checkwarn2, inline=False)
                        if checkwarn3 != None: embed.add_field(name="Warning 3:", value=checkwarn3, inline=False)
                        embed.set_footer(text="To appeal a warn, speak to a staff member.")
                        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def clearwarn(self, ctx, member: discord.Member): # p!clearwarn
        ownerrole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        logchannel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        if ownerrole in member.roles or modrole in member.roles or botrole in member.roles:
            await ctx.send(f"{ctx.author.mention}, this user cannot be warned in the server.")
        else:
            if collection.count_documents({"_id": member.id}, limit = 1) != 0:
                results = collection.find({"_id": member.id})
                for result in results:
                    checkwarn1 = result["Warn 1"]
                    checkwarn2 = result["Warn 2"]
                    checkwarn3 = result["Warn 3"]
                embed = discord.Embed(color=0xff8080)
                if checkwarn1 != None: embed.add_field(name="Warning 1:", value=checkwarn1, inline=False)
                if checkwarn2 != None: embed.add_field(name="Warning 2:", value=checkwarn2, inline=False)
                if checkwarn3 != None: embed.add_field(name="Warning 3:", value=checkwarn3, inline=False)
                collection.delete_one({"_id": member.id})
                await logchannel.send(f"{ctx.author} ({ctx.author.id}) has cleared all warnings from {member.mention} ({member.id}).", embed=embed)
                await ctx.send(f"{ctx.author.mention}, all warnings given to {member.mention} have been cleared sucessfully.")
            else:
                await ctx.send(f"{ctx.author.mention}, there are no warnings given to {member.mention}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None): # p!kick
        ownerrole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        if ownerrole in member.roles or modrole in member.roles or botrole in member.roles:
            await ctx.send(f"{ctx.author.mention}, this user cannot be kicked from the server.")
        else:
            if reason != None:
                await member.send(f"You have been kicked from {ctx.guild.name} for \"{reason}\". You may rejoin, however please read the #rules channel before participating in the server.")
                await member.kick(reason=reason)
                await ctx.send(f"{ctx.author.mention}, {member.mention} has been kicked from the server.")
            else:
                try:
                    await member.send(f"You have been kicked from {ctx.guild.name}. You may rejoin, however please read the #rules channel before participating in the server.")
                except discord.errors.Forbidden: pass
                await member.kick(reason=reason)
                await ctx.send(f"{ctx.author.mention}, {member.mention} has been kicked from the server.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: typing.Union[discord.Member, int], *, reason=None): # p!ban
        ownerrole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        if isinstance(member, int):
            try:
                member = await self.bot.fetch_user(member)
                await ctx.guild.ban(member, reason=reason)
                await ctx.send(f"{ctx.author.mention}, {member.mention} has been banned from the server.")
            except discord.errors.NotFound:
                await ctx.send(f"{ctx.author.mention}, there is no user associated with ID {member}.")
                return
            else:
                pass
        if isinstance(member, discord.Member):
            if ownerrole in member.roles or modrole in member.roles or botrole in member.roles:
                await ctx.send(f"{ctx.author.mention}, this user cannot be banned from the server.")
                return
            else:
                try:
                    if reason != None:
                        await member.send(f"You have been banned from {ctx.guild.name} for \"{reason}\". If you wish to rejoin, you must reach out to a member of the moderation team.")
                    else: 
                        await member.send(f"You have been banned from {ctx.guild.name}. If you wish to rejoin, you must reach out to a member of the moderation team.")
                except discord.errors.Forbidden:
                    pass
                await ctx.guild.ban(member, reason=reason)
                await ctx.send(f"{ctx.author.mention}, {member.mention} has been banned from the server.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def silentkick(self, ctx, member: discord.Member, *, reason=None): # p!silentkick
        ownerrole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        if ownerrole in member.roles or modrole in member.roles or botrole in member.roles:
            await ctx.send(f"{ctx.author.mention}, this user cannot be kicked from the server.")
        else:
            await member.kick(reason=reason)
            await ctx.send(f"{ctx.author.mention}, {member.mention} has been kicked from the server.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def silentban(self, ctx, member: discord.Member, *, reason=None): # p!silentban
        ownerrole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        if ownerrole in member.roles or modrole in member.roles or botrole in member.roles:
            await ctx.send(f"{ctx.author.mention}, this user cannot be banned from the server.")
        else:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f"{ctx.author.mention}, {member.mention} has been banned from the server.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member): # p!unban
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                try: await member.send(f"You have been unbanned from {ctx.guild.name}. You may rejoin, however please read the #rules channel before participating in the server.")
                except discord.errors.Forbidden: pass
                await ctx.guild.unban(user)
                await ctx.send(f"{ctx.author.mention}, {user.mention} has been unbanned from the server.")

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(variables.SERVERBOT, variables.SERVEROWNER, variables.SERVERMODERATOR) # Roles @Server Bot, @Server Owner, @Server Moderator.
    async def slowmode(self, ctx, time: int, channel: discord.TextChannel = None): # p!slowmode
        if channel == None: channel = ctx.channel
        if time > 21600: return await ctx.send(f"{ctx.author.mention}, you cannot set a slowmode for this amount of time!")
        await channel.edit(slowmode_delay=time)
        await ctx.send(f"{ctx.author.mention}, slowmode has been adjusted to {time} seconds.")

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(variables.SERVERBOT, variables.SERVEROWNER, variables.SERVERMODERATOR) # Roles @Server Bot, @Server Owner, @Server Moderator.
    async def lockmode(self, ctx, channel: discord.TextChannel = None): # p!lockmode
        if channel == None: channel = ctx.channel
        if channel.id in arrays.LOCKDOWNCHANNELS:
            sendpermissions = channel.overwrites_for(ctx.guild.default_role)
            if sendpermissions.send_messages == None: sendpermissions.send_messages = False
            else: sendpermissions.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=sendpermissions)
            if sendpermissions.send_messages is False: await ctx.send(f"{ctx.author.mention}, the channel has successfully been locked down.")
            else: await ctx.send(f"{ctx.author.mention}, the channel has successfully been unlocked.")
        else: await ctx.send(f"{ctx.author.mention}, the channel cannot be locked down.")

    @warn.error
    async def warn_error(self, ctx, error): # p!warn error handlers.
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention}, this user cannot be found. Please specify the correct user.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, there is no user or reason specified. Please specify a user and reason.")

    @pardon.error
    async def pardon_error(self, ctx, error): # p!pardon error handlers.
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention}, this user cannot be found. Please specify the correct user.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, there is no user specified. Please specify a user.")

    @kick.error
    async def kick_error(self, ctx, error): # p!kick error handlers.
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention}, this user cannot be found. Please specify the correct user.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, there is no user specified. Please specify a user.")

    @ban.error
    async def ban_error(self, ctx, error): # p!ban error handlers.
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention}, this user cannot be found. Please specify the correct user.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, there is no user specified. Please specify a user.")

    @silentkick.error
    async def silentkick_error(self, ctx, error): # p!silentkick error handlers.
        if isinstance(error, commands.BadArgument):
            await ctx.send("This user cannot be found. Please specify the correct user.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("There is no user specified. Please specify a user.")

    @silentban.error
    async def silentban_error(self, ctx, error): # p!silentban error handlers.
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention}, this user cannot be found. Please specify the correct user.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, there is no user specified. Please specify a user.")

    @slowmode.error
    async def slowmode_error(self, ctx, error): # p!slowmode error handlers.
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention}, this time is invalid. Please specify the correct amount of time.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, there is no time specified. Please specify an amount of time.")

    @lockmode.error
    async def lockmode_error(self, ctx, error): # p!lockmode error handlers.
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention}, this channel is invalid. Please specify the correct channel.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, there is no channel specified. Please specify a channel.")

def setup(bot): bot.add_cog(Moderation(bot))
