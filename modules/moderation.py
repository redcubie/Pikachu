import discord, os, importlib, asyncio, pymongo, re, typing
from discord.ext import commands; from pymongo import MongoClient
import configuration.variables as variables; import configuration.arrays as arrays

class FindMember(commands.IDConverter):
    async def convert(self, ctx, argument) -> discord.User:
        match = self._get_id_match(argument) or re.match(r'<@!?([0-9]+)>$', argument)
        if match == None and ctx.guild:
            result = ctx.guild.get_member_named(argument)
        else:
            userID = int(match.group(1))
            result = ctx.guild.get_member(userID) or await ctx.bot.fetch_user(userID) if ctx.guild else await ctx.bot.fetch_user(userID)
        if result == None:
            await ctx.send(f"{ctx.author.mention}, this user cannot be found. Please specify the correct user.")
        return result

class Moderation(commands.Cog):
    "Commands which can be used by staff members."
    def __init__(self, bot): self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(variables.SERVERBOT, variables.SERVEROWNER, variables.SERVERMODERATOR) # Roles @Server Bot, @Server Owner, @Server Moderator.
    async def checkactivity(self, ctx, days = 30): # p!checkactivity
        "Check the amount of active members on the server, plus those with roles."
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
        "Clear the specified amount of messages last sent."
        deleted = await ctx.channel.purge(limit=amount+1)
        logChannel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        if amount != 0:
            await logChannel.send(f"{ctx.author} ({ctx.author.id}) has cleared {len(deleted)-1} messages in {ctx.channel}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason): # p!warn
        "Warns a user on the server. Two warns will kick automatically, three will ban."
        ownerRole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        logChannel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        if ownerRole in member.roles or modRole in member.roles or botRole in member.roles:
            await ctx.send(f"{ctx.author.mention}, this user cannot be warned in the server.")
        else:
            if collection.count_documents({"_id": member.id}, limit = 1) == 0:
                post = {"_id": member.id, "Warn 1": None, "Warn 2": None, "Warn 3": None}
                collection.insert_one(post)
                results = collection.find({"_id": member.id})
                for result in results:
                    checkWarn1 = result["Warn 1"]
                    checkWarn2 = result["Warn 2"]
                    checkWarn3 = result["Warn 3"]
                if checkWarn1 == None:
                    collection.update_one({"_id": member.id}, {"$set":{"Warn 1": reason}})
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 1:", value=reason, inline=False)
                    try: await member.send(f"You have been warned in {ctx.guild.name} for \"{reason}\". This is your first warning and only warning without an automatic punishment. Please reconsider the rules before participating in the server. Your next offense will result in an automatic kick.")
                    except discord.errors.Forbidden: pass
                    await logChannel.send(f"{ctx.author} ({ctx.author.id}) has given a warning to {member.mention} ({member.id}).", embed=embed)
                    await ctx.send(f"{ctx.author.mention}, a warning has been given to {member.mention}.")
            else:
                results = collection.find({"_id": member.id})
                for result in results:
                    checkWarn1 = result["Warn 1"]
                    checkWarn2 = result["Warn 2"]
                    checkWarn3 = result["Warn 3"]
                if checkWarn2 == None and checkWarn1 != None:
                    collection.update_one({"_id": member.id}, {"$set":{"Warn 2": reason}})
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 2:", value=reason, inline=False)
                    try: await member.send(f"You have been warned in {ctx.guild.name} for \"{reason}\". This is your second warning, therefore you have automatically been kicked from the server. Please reconsider the rules before participating in the server. Your next offense will result in an automatic ban.")
                    except discord.errors.Forbidden: pass
                    await logChannel.send(f"{ctx.author} ({ctx.author.id}) has given a warning to {member.mention} ({member.id}).", embed=embed)
                    await member.kick(reason=f"{checkWarn1}, {reason}")
                    await ctx.send(f"{ctx.author.mention}, a warning has been given to {member.mention}. A kick has been initiated automatically.")
                elif checkWarn3 == None and checkWarn2 != None:
                    collection.update_one({"_id": member.id}, {"$set":{"Warn 3": reason}})
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 3:", value=reason, inline=False)
                    try: await member.send(f"You have been warned in {ctx.guild.name} for \"{reason}\". This is your third warning, therefore you have automatically been banned from the server. Please contact a staff member if you feel you have been wrongfully punished.")
                    except discord.errors.Forbidden: pass
                    await logChannel.send(f"{ctx.author} ({ctx.author.id}) has given a warning to {member.mention} ({member.id}).", embed=embed)
                    await member.ban(reason=f"{checkWarn1}, {checkWarn2}, {reason}")
                    await ctx.send(f"{ctx.author.mention}, a warning has been given to {member.mention}. A ban has been initiated automatically.")
                elif checkWarn3 != None and checkWarn2 != None:
                    await ctx.send(f"{ctx.author.mention}, there are too many warnings recorded for {member.mention}.")
                    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def pardon(self, ctx, member: discord.Member): # p!warn
        "Removes a warn from a user on the server."
        ownerRole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        logChannel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        if ownerRole in member.roles or modRole in member.roles or botRole in member.roles:
            await ctx.send(f"{ctx.author.mention}, this user cannot be warned in the server.")
        else:
            if collection.count_documents({"_id": member.id}, limit = 1) == 0:
                await ctx.send(f"{ctx.author.mention}, there are no warnings recorded for {member.mention}.")
            else:
                results = collection.find({"_id": member.id})
                for result in results:
                    checkWarn1 = result["Warn 1"]
                    checkWarn2 = result["Warn 2"]
                    checkWarn3 = result["Warn 3"]
                if checkWarn3 != None:
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 3:", value=checkWarn3, inline=False)
                    await logChannel.send(f"{ctx.author} ({ctx.author.id}) has pardoned a warning from {member.mention} ({member.id}).", embed=embed)
                    collection.update_one({"_id": member.id}, {"$set":{"Warn 3": None}})
                    await ctx.send(f"{ctx.author.mention}, the latest warning given to {member.mention} has been removed successfully.")
                elif checkWarn2 != None and checkWarn3 == None:
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 2:", value=checkWarn2, inline=False)
                    await logChannel.send(f"{ctx.author} ({ctx.author.id}) has pardoned a warning from {member.mention} ({member.id}).", embed=embed)
                    collection.update_one({"_id": member.id}, {"$set":{"Warn 2": None}})
                    await ctx.send(f"{ctx.author.mention}, the latest warning given to {member.mention} has been removed successfully.")
                elif checkWarn1 != None and checkWarn2 == None:
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Warning 1:", value=checkWarn1, inline=False)
                    await logChannel.send(f"{ctx.author} ({ctx.author.id}) has pardoned a warning from {member.mention} ({member.id}).", embed=embed)
                    collection.delete_one({"_id": member.id})
                    await ctx.send(f"{ctx.author.mention}, the latest warning given to {member.mention} has been removed successfully.")
                else:
                    await ctx.send(f"{ctx.author.mention}, there are no warnings recorded for {member.mention}.")
                    
    @commands.command()
    @commands.guild_only()
    async def listwarn(self, ctx, member: discord.Member = None): # p!listwarn
        "Lists the warns that a user has received. Staff can see other users' warns."
        ownerRole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        if ownerRole in ctx.author.roles or modRole in ctx.author.roles or botRole in ctx.author.roles:
            if member == None: member = ctx.author
            if ownerRole in member.roles or modRole in member.roles or botRole in member.roles:
                await ctx.send(f"{ctx.author.mention}, this user cannot be warned in the server.")
            else:
                if collection.count_documents({"_id": member.id}, limit = 1) == 0:
                    if member == ctx.author: await ctx.send(f"{ctx.author.mention}, there are no warnings recorded.")
                    else: await ctx.send(f"{ctx.author.mention}, there are no warnings recorded for {member.mention}.")
                else:
                    results = collection.find({"_id": member.id})
                    for result in results:
                        checkWarn1 = result["Warn 1"]
                        checkWarn2 = result["Warn 2"]
                        checkWarn3 = result["Warn 3"]
                    embed = discord.Embed(color=0xff8080)
                    if checkWarn1 != None: embed.add_field(name="Warning 1:", value=checkWarn1, inline=False)
                    if checkWarn2 != None: embed.add_field(name="Warning 2:", value=checkWarn2, inline=False)
                    if checkWarn3 != None: embed.add_field(name="Warning 3:", value=checkWarn3, inline=False)
                    embed.set_footer(text="To appeal a warn, speak to a staff member.")
                    await ctx.send(embed=embed)
        else: # This is an example of horrible Python coding. I plan to simplify it later on, but as of now, it works at least.
            if member != None:
                await ctx.send(f"{ctx.author.mention}, using this command on others is only allowed for staff members.")
            else:
                member = ctx.author
                if ownerRole in member.roles or modRole in member.roles or botRole in member.roles:
                    await ctx.send(f"{ctx.author.mention}, this user cannot be warned in the server.")
                else:
                    if collection.count_documents({"_id": member.id}, limit = 1) == 0:
                        await ctx.send(f"{ctx.author.mention}, there are no warnings recorded for {member.mention}.")
                    else:
                        results = collection.find({"_id": member.id})
                        for result in results:
                            checkWarn1 = result["Warn 1"]
                            checkWarn2 = result["Warn 2"]
                            checkWarn3 = result["Warn 3"]
                        embed = discord.Embed(color=0xff8080)
                        if checkWarn1 != None: embed.add_field(name="Warning 1:", value=checkWarn1, inline=False)
                        if checkWarn2 != None: embed.add_field(name="Warning 2:", value=checkWarn2, inline=False)
                        if checkWarn3 != None: embed.add_field(name="Warning 3:", value=checkWarn3, inline=False)
                        embed.set_footer(text="To appeal a warn, speak to a staff member.")
                        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def clearwarn(self, ctx, member: discord.Member): # p!clearwarn
        "Clears all warns from a specified user."
        ownerRole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        logChannel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        if ownerRole in member.roles or modRole in member.roles or botRole in member.roles:
            await ctx.send(f"{ctx.author.mention}, this user cannot be warned in the server.")
        else:
            if collection.count_documents({"_id": member.id}, limit = 1) != 0:
                results = collection.find({"_id": member.id})
                for result in results:
                    checkWarn1 = result["Warn 1"]
                    checkWarn2 = result["Warn 2"]
                    checkWarn3 = result["Warn 3"]
                embed = discord.Embed(color=0xff8080)
                if checkWarn1 != None: embed.add_field(name="Warning 1:", value=checkWarn1, inline=False)
                if checkWarn2 != None: embed.add_field(name="Warning 2:", value=checkWarn2, inline=False)
                if checkWarn3 != None: embed.add_field(name="Warning 3:", value=checkWarn3, inline=False)
                collection.delete_one({"_id": member.id})
                await logChannel.send(f"{ctx.author} ({ctx.author.id}) has cleared all warnings from {member.mention} ({member.id}).", embed=embed)
                await ctx.send(f"{ctx.author.mention}, all warnings given to {member.mention} have been cleared sucessfully.")
            else:
                await ctx.send(f"{ctx.author.mention}, there are no warnings given to {member.mention}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None): # p!kick
        "Kicks a user from the server."
        ownerRole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        if ownerRole in member.roles or modRole in member.roles or botRole in member.roles:
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
        "Bans a member from the server."
        ownerRole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
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
            if ownerRole in member.roles or modRole in member.roles or botRole in member.roles:
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
        "Kicks a member from the server without messaging."
        ownerRole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        if ownerRole in member.roles or modRole in member.roles or botRole in member.roles:
            await ctx.send(f"{ctx.author.mention}, this user cannot be kicked from the server.")
        else:
            await member.kick(reason=reason)
            await ctx.send(f"{ctx.author.mention}, {member.mention} has been kicked from the server.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def silentban(self, ctx, member: discord.Member, *, reason=None): # p!silentban
        "Bans a member from the server without messaging."
        ownerRole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
        modRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
        botRole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
        if ownerRole in member.roles or modRole in member.roles or botRole in member.roles:
            await ctx.send(f"{ctx.author.mention}, this user cannot be banned from the server.")
        else:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f"{ctx.author.mention}, {member.mention} has been banned from the server.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: FindMember, *, reason=None): # p!unban
        "Unbans a member from the server."
        try: await ctx.guild.fetch_ban(member)
        except discord.errors.NotFound: return await ctx.safe_send(f"{ctx.author.mention}, {member.mention} is not banned!")
        try: await member.send(f"You have been unbanned from {ctx.guild.name}. You may rejoin, however please read the #rules channel before participating in the server.")
        except discord.errors.Forbidden: pass
        await ctx.guild.unban(member, reason=reason)
        await ctx.send(f"{ctx.author.mention}, {member.mention} has been unbanned from the server.")

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(variables.SERVERBOT, variables.SERVEROWNER, variables.SERVERMODERATOR) # Roles @Server Bot, @Server Owner, @Server Moderator.
    async def slowmode(self, ctx, time: int, channel: discord.TextChannel = None): # p!slowmode
        "Enables slowmode in the specified channel."
        if channel == None: channel = ctx.channel
        if time > 21600: return await ctx.send(f"{ctx.author.mention}, you cannot set a slowmode for this amount of time!")
        await channel.edit(slowmode_delay=time)
        await ctx.send(f"{ctx.author.mention}, slowmode has been adjusted to {time} seconds.")

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(variables.SERVERBOT, variables.SERVEROWNER, variables.SERVERMODERATOR) # Roles @Server Bot, @Server Owner, @Server Moderator.
    async def lockmode(self, ctx, channel: discord.TextChannel = None): # p!lockmode
        "Disables the sending of messages in the specified channel for regular users."
        if channel == None: channel = ctx.channel
        if channel.id in arrays.LOCKDOWNCHANNELS:
            sendpermissions = channel.overwrites_for(ctx.guild.default_role)
            if sendpermissions.send_messages == None: sendpermissions.send_messages = False
            else: sendpermissions.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=sendpermissions)
            if sendpermissions.send_messages is False: await ctx.send(f"{ctx.author.mention}, the channel has successfully been locked down.")
            else: await ctx.send(f"{ctx.author.mention}, the channel has successfully been unlocked.")
        else: await ctx.send(f"{ctx.author.mention}, the channel cannot be locked down.")

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(variables.SERVERBOT, variables.SERVEROWNER, variables.SERVERMODERATOR) # Roles @Server Bot, @Server Owner, @Server Moderator.
    async def sendrules(self, ctx):
        "Sends the rule messages in the specified rules channel in case they need to be resent."
        rulesChannel = self.bot.get_channel(variables.MODERATORCHAT) # Channel #rules.
        await rulesChannel.purge(limit=10)
        await rulesChannel.send("__**Introduction:**__\nHello, and welcome to Nincord, our small but amazing Discord server where you can talk about anything related to Nintendo and their franchises! We mainly focus on competitive gaming, but you can talk about the games casually as well. Here, we host clubs, tournaments, and more! If you need a small space to talk about your favorite Nintendo games, this is the place for you!")
        await rulesChannel.send("__**Rules:**__\n**<:smash_mario:665610205509451790> 1. Use common sense.**\nIf it isn't right, don't do it. If it can hurt someone else, or make someone feel uncomfortable, don't say it. Everyone has rights to have different opinions, but any hate speech with intentions to do bad will not, and never will be tolerated. This also includes mini-modding. If something's wrong, just ping a staff role without spamming them. Don't ask for roles either.\n**<:smash_donkey_kong:665610202187431939>  2. No spamming, copypasta, flooding, ectara.**\nRepeating your message over and over is not polite. Spreading copypasta or flooding channels with messages is also not tolerated. Please be respectful with your messages in the server channels so that they don't disrupt the flow of the conversation.\n**<:smash_link:665610203634335799>  3. Advertising is available, with permission that is.**\nBefore you advertise, please inform a staff member. Don't post the link yourself, you'll get warned without permission. Same with advertising your server randomly in someone else's private messages. Note that this will not help you become an affiliate.")
        await rulesChannel.send("**<:smash_samus:665610206369153064> 4. Refrain from inappropriate topics.**\nDo not send, upload content, have profile information, or for those with the permission, set nicknames that is inappropriate or NSFW. This includes but not limited to, sex or sexual themes, nudity, extreme violence, illegal content, and the like. Swearing is allowed, just be careful what you say.\n**<:smash_yoshi:665610206704828425> 5. Don't attempt to evade any punishments.**\nIf you're banned, it means to not come back until an unban is issued. If you're caught doing this, action will be taken. You can appeal your ban by contacting a staff member. There is currently no appeal form that can be filled out.\n**<:smash_kirby:665610203353579550> 6. Mark spoilers as needed.**\nAll spoilers for unreleased content must be formatted as spoilers until permission has been given to post the information without proper formatting. This includes leaks, data-mining, and the like. To do this, put two |s, then your spoilers, then another two |s.")
        await rulesChannel.send("**<:smash_fox:665610202745143296> 7. No unnecessary noise in the voice channels.**\nNo harmful or ear-blasting sounds. Please try to refrain from echoing as well. People should be able to hear you clearly while you participate in the voice channel.\n**<:smash_pikachu:665610205236690982> 8. Piracy discussion is not allowed.**\nDiscussing where to download video games for free is not allowed under the Discord Terms of Service. While people may have different views on where the line is drawn when it comes to piracy, it is best to not bring it up on this server.")
        await rulesChannel.send("__**Agreement:**__\nWhen agreeing to the server rules, you are accepting the fact that members of staff can and will take action against you if necessary, and can punish you for any reason. You are also allowing all bots on the server to store data about you, such as, your user ID, messages, and anything necessary to perform proper server functions. The server is required to inform you to accept the collecting of this data, per Discord's Developer Terms of Service (https://discordapp.com/developers/docs/legal). We also require you to agree and abide by Discord's Terms of Service (https://discordapp.com/terms) Finally, we are required by Discord's new Terms of Service to ask you to agree to the Children's Online Privacy Protection Rule (https://www.ftc.gov/enforcement/rules/rulemaking-regulatory-reform-proceedings/childrens-online-privacy-protection-rule). These documents, as well as these rules, will change over time. If you do not agree to these terms, please leave the server.")

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