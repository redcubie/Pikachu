import discord, os, importlib, asyncio, pymongo, re, typing
from discord.ext import commands; from pymongo import MongoClient
from manager import is_staff_member, check_staff_member
import configuration.variables as variables
import configuration.arrays as arrays

class Moderation(commands.Cog):
    "Commands which can be used by staff members."
    def __init__(self, bot): self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 1, *, reason = None): # p!clear
        "Clear the specified amount of messages last sent.\nThis command is only usable by staff members."
        embed = discord.Embed(color = 0xff8080)
        embed.add_field(name = "Reason", value = reason, inline = False)
        deleted = await ctx.channel.purge(limit=amount+1)
        log_channel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        if amount >= 1 and reason != None:
            await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has cleared {len(deleted)-1} messages in {ctx.channel.mention}.", embed = embed)
        elif amount >= 1 and reason == None:
            await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has cleared {len(deleted)-1} messages in {ctx.channel.mention}.")

    @commands.command(aliases = ["addwarn"])
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def warn(self, ctx, member: discord.Member, *, reason): # p!warn
        "Warns a user on the server.\nTwo warns will kick automatically, three will ban.\nThis command is only usable by staff members."
        log_channel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        if check_staff_member(member):
            return await ctx.reply("This user cannot be warned in the server.")

        if collection.count_documents({"_id": member.id}, limit = 1) == 0:
            post = {"_id": member.id, "Warn 1": None, "Warn 2": None, "Warn 3": None}
            collection.insert_one(post)
            results = collection.find({"_id": member.id})
            for result in results:
                check_warn_1 = result["Warn 1"]
                check_warn_2 = result["Warn 2"]
                check_warn_3 = result["Warn 3"]

            if check_warn_1 == None:
                collection.update_one({"_id": member.id}, {"$set":{"Warn 1": reason}})
                embed = discord.Embed(color = 0xff8080)
                embed.add_field(name = "Warning 1", value = reason, inline = False)
                try:
                    await member.send(f"You have been warned in {ctx.guild.name}. This is your first warning and only warning without an automatic punishment. Please reconsider the rules before participating in the server. Your next offense will result in an automatic kick.", embed = embed)
                except discord.errors.Forbidden: pass
                await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has given a warning to {member.mention} ({member.id}).", embed = embed)
                await ctx.reply(f"A warning has been given to {member.mention}.")
        else:
            results = collection.find({"_id": member.id})
            for result in results:
                check_warn_1 = result["Warn 1"]
                check_warn_2 = result["Warn 2"]
                check_warn_3 = result["Warn 3"]

            if check_warn_2 == None and check_warn_1 != None:
                collection.update_one({"_id": member.id}, {"$set":{"Warn 2": reason}})
                embed = discord.Embed(color = 0xff8080)
                embed.add_field(name = "Warning 2", value = reason, inline = False)
                try:
                    await member.send(f"You have been warned in {ctx.guild.name}. This is your second warning, therefore you have automatically been kicked from the server. Please reconsider the rules before participating in the server. Your next offense will result in an automatic ban.", embed = embed)
                except discord.errors.Forbidden: pass
                await log_channel.send(f"{ctx.author} ({ctx.author.id}) has given a warning to {member.mention} ({member.id}). A kick has been initiated automatically.", embed = embed)
                await member.kick(reason = f"Automatically kicked. ({check_warn_1}, {reason})")
                await ctx.reply(f"A warning has been given to {member.mention}. A kick has been initiated automatically.")
            
            elif check_warn_3 == None and check_warn_2 != None:
                collection.update_one({"_id": member.id}, {"$set":{"Warn 3": reason}})
                embed = discord.Embed(color = 0xff8080)
                embed.add_field(name = "Warning 3", value = reason, inline = False)
                try:
                    await member.send(f"You have been warned in {ctx.guild.name}. This is your third warning, therefore you have automatically been banned from the server. Please contact a staff member if you feel you have been wrongfully punished.", embed = embed)
                except discord.errors.Forbidden: pass
                await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has given a warning to {member.mention} ({member.id}). A ban has been initiated automatically.", embed = embed)
                await member.ban(reason = f"Automatically banned. ({check_warn_1}, {check_warn_2}, {reason})")
                await ctx.reply(f"A warning has been given to {member.mention}. A ban has been initiated automatically.")
                
            elif check_warn_3 != None and check_warn_2 != None:
                await ctx.reply(f"There are too many warnings recorded for {member.mention}.")
                    
    @commands.command(aliases = ["removewarn"])
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def pardon(self, ctx, member: discord.Member): # p!warn
        "Removes a warn from a user on the server.\nThis command is only usable by staff members."
        log_channel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]

        if check_staff_member(member):
            return await ctx.reply("This user cannot be warned in the server.")

        if collection.count_documents({"_id": member.id}, limit = 1) == 1:
            results = collection.find({"_id": member.id})
            for result in results:
                check_warn_1 = result["Warn 1"]
                check_warn_2 = result["Warn 2"]
                check_warn_3 = result["Warn 3"]
        
            if check_warn_3 != None:
                embed = discord.Embed(color = 0xff8080)
                embed.add_field(name = "Warning 3", value = check_warn_3, inline = False)
                await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has pardoned a warning from {member.mention} ({member.id}).", embed = embed)
                collection.update_one({"_id": member.id}, {"$set":{"Warn 3": None}})
                return await ctx.reply(f"The latest warning given to {member.mention} has been removed successfully.")

            elif check_warn_2 != None and check_warn_3 == None:
                embed = discord.Embed(color = 0xff8080)
                embed.add_field(name = "Warning 2", value = check_warn_2, inline = False)
                await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has pardoned a warning from {member.mention} ({member.id}).", embed = embed)
                collection.update_one({"_id": member.id}, {"$set":{"Warn 2": None}})
                return await ctx.reply(f"The latest warning given to {member.mention} has been removed successfully.")
                
            elif check_warn_1 != None and check_warn_2 == None:
                embed = discord.Embed(color = 0xff8080)
                embed.add_field(name = "Warning 1", value = check_warn_1, inline = False)
                await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has pardoned a warning from {member.mention} ({member.id}).", embed = embed)
                collection.delete_one({"_id": member.id})
                return await ctx.reply(f"The latest warning given to {member.mention} has been removed successfully.")
            else: return await ctx.reply(f"There are no warnings recorded for {member.mention}.")            
        else: return await ctx.reply(f"There are no warnings recorded for {member.mention}.")
                    
    @commands.command(aliases = ["listwarns"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def listwarn(self, ctx, member: discord.Member = None): # p!listwarn
        "Lists the warns that a user has received.\nStaff members can use this command on others."
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]
        async def user_warn_list(user):
            if collection.count_documents({"_id": member.id}, limit = 1) == 0:
                if member == ctx.author:
                    await ctx.reply("There are no warnings recorded.")
                else:
                    await ctx.reply(f"There are no warnings recorded for {member.mention}.")
            else:
                results = collection.find({"_id": member.id})
                for result in results:
                    check_warn_1 = result["Warn 1"]
                    check_warn_2 = result["Warn 2"]
                    check_warn_3 = result["Warn 3"]

                embed = discord.Embed(color = 0xff8080)
                if check_warn_1 != None: embed.add_field(name = "Warning 1", value = check_warn_1, inline = False)
                if check_warn_2 != None: embed.add_field(name = "Warning 2", value = check_warn_2, inline = False)
                if check_warn_3 != None: embed.add_field(name = "Warning 3", value = check_warn_3, inline = False)
                embed.set_footer(text = "To appeal a warn, speak to a staff member.")

                if member == ctx.author:
                    await ctx.reply(f"Here are all recorded warnings.", embed = embed)
                else:
                    await ctx.reply(f"Here are all recorded warnings for {member.mention}.", embed = embed)

        if check_staff_member(ctx.author):
            if member == None: member = ctx.author
            if check_staff_member(member):
                return await ctx.reply("This user cannot be warned in the server.")
            return await user_warn_list(member)

        if member != None:
            return await ctx.reply("Using this command on others is only allowed for staff members.")
        else:
            member = ctx.author
            if check_staff_member(member): return await ctx.reply("This user cannot be warned in the server.")
            else: return await user_warn_list(member)

    @commands.command(aliases = ["clearwarns"])
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def clearwarn(self, ctx, member: discord.Member): # p!clearwarn
        "Clears all warns from a specified user.\nThis command is only usable by staff members."
        log_channel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Moderation"]
        collection = database["Warns"]

        if check_staff_member(member):
            return await ctx.reply("This user cannot be warned in the server.")

        if collection.count_documents({"_id": member.id}, limit = 1) != 0:
            results = collection.find({"_id": member.id})
            for result in results:
                check_warn_1 = result["Warn 1"]
                check_warn_2 = result["Warn 2"]
                check_warn_3 = result["Warn 3"]

            embed = discord.Embed(color = 0xff8080)
            if check_warn_1 != None: embed.add_field(name = "Warning 1", value = check_warn_1, inline = False)
            if check_warn_2 != None: embed.add_field(name = "Warning 2", value = check_warn_2, inline = False)
            if check_warn_3 != None: embed.add_field(name = "Warning 3", value = check_warn_3, inline = False)

            collection.delete_one({"_id": member.id})
            await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has cleared all warnings from {member.mention} ({member.id}).", embed = embed)
            await ctx.reply(f"All warnings given to {member.mention} have been cleared sucessfully.")
        else: await ctx.reply(f"There are no warnings recorded for {member.mention}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason = None): # p!kick
        "Kicks a user from the server.\nThis command is only usable by staff members."
        log_channel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        if check_staff_member(member): return await ctx.send("This user cannot be kicked from the server.")
        if reason != None:
            embed = discord.Embed(color = 0xff8080)
            embed.add_field(name = "Reason", value = reason, inline = False)
            await member.send(f"You have been kicked from {ctx.guild.name}. You may rejoin, however please read the #rules channel before participating in the server.", embed = embed)
            await member.kick(reason = reason)
            await ctx.reply(f"{member.mention} has been kicked from the server.")
            await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has kicked {member.mention} ({member.id}).", embed = embed)
        else:
            try: await member.send(f"You have been kicked from {ctx.guild.name}. You may rejoin, however please read the #rules channel before participating in the server.")
            except discord.errors.Forbidden: pass
            await member.kick(reason = reason)
            await ctx.reply(f"{member.mention} has been kicked from the server.")
            await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has kicked {member.mention} ({member.id}).")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: typing.Union[discord.Member, int, str], *, reason = None): # p!ban
        "Bans a member from the server.\nThis command is only usable by staff members."
        log_channel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        try:
            if isinstance(member, int):
                member = await self.bot.fetch_user(member)
            elif isinstance(member, str):
                member = await self.bot.fetch_user(member[3:-1])

            embed = discord.Embed(color = 0xff8080)
            embed.add_field(name = "Reason", value = reason, inline = False)

            if isinstance(member, int):
                try:
                    await ctx.guild.ban(member, reason = reason)
                    await ctx.reply(f"{member.mention} has been banned from the server.")
                    if reason != None: await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has banned {member.mention} ({member.id}).", embed = embed)
                    else: await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has banned {member.mention} ({member.id}).")
                except discord.errors.NotFound:
                    return await ctx.reply(f"There is no user associated with ID {member}.")
    
            if isinstance(member, discord.Member):
                if check_staff_member(member): return await ctx.reply("This user cannot be banned from the server.")
                try:
                    if reason != None:
                        await member.send(f"You have been banned from {ctx.guild.name}. If you wish to rejoin, you must reach out to a member of the moderation team.", embed = embed)
                    else:
                        await member.send(f"You have been banned from {ctx.guild.name}. If you wish to rejoin, you must reach out to a member of the moderation team.")
                except discord.errors.Forbidden: pass
                await ctx.guild.ban(member, reason = reason, delete_message_days = 0)
                await ctx.reply(f"{member.mention} has been banned from the server.")
                if reason != None:
                    await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has banned {member.mention} ({member.id}).", embed = embed)
                else:
                    await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has banned {member.mention} ({member.id}).")
        except: return await ctx.reply("There was an error finding the user associated with your request.")

    @commands.command(aliases = ["quietkick"])
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    async def silentkick(self, ctx, member: discord.Member, *, reason = None): # p!silentkick
        "Kicks a member from the server without messaging.\nThis command is only usable by staff members."
        log_channel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        if check_staff_member(member): return await ctx.reply("This user cannot be kicked from the server.")
        await member.kick(reason = reason)
        embed = discord.Embed(color = 0xff8080)
        embed.add_field(name = "Reason", value = reason, inline = False)
        await ctx.reply(f"{member.mention} has been kicked from the server.")
        if reason != None: await log_channel.reply(f"{ctx.author.mention} ({ctx.author.id}) has silently kicked {member.mention} ({member.id}).", embed = embed)
        else: await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has silently kicked {member.mention} ({member.id}).")

    @commands.command(aliases = ["quietban"])
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def silentban(self, ctx, member: discord.Member, *, reason = None): # p!silentban
        "Bans a member from the server without messaging.\nThis command is only usable by staff members."
        log_channel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        if check_staff_member(member): return await ctx.reply("This user cannot be banned from the server.")
        await ctx.guild.ban(member, reason = reason)
        embed = discord.Embed(color = 0xff8080)
        embed.add_field(name = "Reason", value = reason, inline = False)
        await ctx.reply(f"{member.mention} has been banned from the server.")
        if reason != None:
            await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has silently banned {member.mention} ({member.id}).", embed = embed)
        else:
            await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has silently banned {member.mention} ({member.id}).")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, member: typing.Union[discord.User, int, str], *, reason = None): # p!unban
        "Unbans a member from the server.\nThis command is only usable by staff members."
        log_channel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        try:
            if isinstance(member, str):
                member = await self.bot.fetch_user(member[3:-1])
            else:
                member = await self.bot.fetch_user(member)

            await ctx.guild.unban(member, reason = reason)
            await ctx.reply(f"{member.mention} has been unbanned from the server.")

            try:
                await member.send(f"You have been unbanned from {ctx.guild.name}. You may rejoin, however please read the #rules channel before participating in the server.")
            except discord.errors.Forbidden: pass

            embed = discord.Embed(color = 0xff8080)
            embed.add_field(name = "Reason", value = reason, inline = False)
            await ctx.reply(f"{member.mention} has been unbanned from the server.")

            if reason != None:
                await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has unbanned {member.mention} ({member.id}).", embed = embed)
            else:
                await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has unbanned {member.mention} ({member.id}).")
        except: return await ctx.reply("There was an error finding the user associated with your request.")

    @commands.command()
    @commands.guild_only()
    @is_staff_member()
    async def slowmode(self, ctx, time: int, channel: discord.TextChannel = None, *, reason = None): # p!slowmode
        "Adjusts the slowmode time in the specified channel.\nThis command is only usable by staff members."
        log_channel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        if channel == None: channel = ctx.channel
        if time > 21600:
            return await ctx.reply("You cannot set a slowmode for this amount of time!")
        await channel.edit(slowmode_delay = time)
        
        embed = discord.Embed(color = 0xff8080)
        embed.add_field(name = "Reason", value = reason, inline = False)
        await ctx.reply(f"Slowmode has been adjusted to {time} seconds.")
        await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has adjusted slowmode in {channel.mention} to {time} seconds.", embed = embed)

    @commands.command()
    @commands.guild_only()
    @is_staff_member()
    async def lockmode(self, ctx, channel: discord.TextChannel = None, *, reason = None): # p!lockmode
        "Toggles sending messages in the specified channel for members.\nThis command is only usable by staff members."
        log_channel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #action-logs.
        if channel == None: channel = ctx.channel
        if channel.id in arrays.CHANNELINFORMATION:
            text_channel = channel; info = arrays.CHANNELINFORMATION.get(text_channel.id)
            lockdown_setting = info.get("Lockdown"); voice_setting = info.get("Voice")

            if not lockdown_setting:
                return await ctx.reply("The channel cannot be locked down.")
            if voice_setting:
                voiceChannel = self.bot.get_channel(voice_setting)
                talkPermissions = voiceChannel.overwrites_for(ctx.guild.default_role)
            sendPermissions = text_channel.overwrites_for(ctx.guild.default_role)
            
            if sendPermissions.send_messages == None:
                if voice_setting: talkPermissions.connect = False
                sendPermissions.send_messages = False
            else:
                if voice_setting: talkPermissions.connect = None
                sendPermissions.send_messages = None
            if voice_setting:
                await voiceChannel.set_permissions(ctx.guild.default_role, overwrite = talkPermissions)
            await text_channel.set_permissions(ctx.guild.default_role, overwrite = sendPermissions)

            embed = discord.Embed(color = 0xff8080)
            embed.add_field(name = "Reason", value = reason, inline = False)
            if sendPermissions.send_messages == False:
                await ctx.reply("The channel has successfully been locked down.")
                await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has toggled on lockmode in {text_channel.mention}.", embed = embed)
            else:
                await ctx.reply("The channel has successfully been unlocked.")
                await log_channel.send(f"{ctx.author.mention} ({ctx.author.id}) has toggled off lockmode in {text_channel.mention}.", embed = embed)
        else: await ctx.reply("The channel cannot be locked down.")

    @commands.command()
    @commands.guild_only()
    @is_staff_member()
    @commands.cooldown(1, 3600, commands.BucketType.guild)
    async def sendrules(self, ctx):
        "Sends the rule messages in the specified rules channel.\nThis command is only usable by staff members."
        rules_channel = self.bot.get_channel(variables.SERVERRULES) # Channel #server-rules.
        staff_list = []

        for role in arrays.ROLEINFORMATION:
            if role != variables.SERVERBOT:
                info = arrays.ROLEINFORMATION.get(role)
                staff_setting = info.get("Staff")
                if staff_setting:
                    staff_role = discord.utils.get(ctx.guild.roles, id=role)
                    for member in staff_role.members:
                        if member.mention not in staff_list:
                            staff_list.append(member.mention)

        await rules_channel.purge(limit = 20)
        await rules_channel.send(f"__**Introduction:**__\nHello, and welcome to {ctx.guild.name}, our small but amazing Discord server where you can talk about anything related to Nintendo and their franchises! We mainly focus on competitive gaming, but you can talk about the games casually as well. Here, we host clubs, tournaments, and more! If you need a small space to talk about your favorite Nintendo games, this is the place for you!")
        await rules_channel.send(f"__**Rules:**__\n**<:smash_mario:665610205509451790> 1. Use common sense.**\nIf it isn't right, don't do it. If it can hurt someone else, or make someone feel uncomfortable, don't say it. Everyone has rights to have different opinions, but any hate speech with intentions to do bad will not, and never will be tolerated. This also includes actions such as mini-modding, spreading copypasta, and flooding channels.\n**<:smash_donkey_kong:665610202187431939> 2. Advertising is available, with permission that is.**\nBefore you advertise, please inform a staff member. Don't post the link yourself, it is considered to be rude. Same with advertising your server randomly in someone else's private messages. Note that this will not help you become an affiliate.\n**<:smash_link:665610203634335799> 3. Refrain from inappropriate topics.**\nDo not send, upload content, or set profile information that is inappropriate or NSFW. This includes but not limited to, sex or sexual themes, nudity, extreme violence, illegal content, and the like. Swearing is okay, slurs are not.\n**<:smash_samus:665610206369153064> 4. Mark spoilers as needed, and no leaks!**\nAll spoilers for unreleased and leaked content must be formatted as spoilers until permission has been given to post the information without proper formatting. To do this, put two |s, then your spoilers, then another two |s. Discussion of leaked content obtained through illegal means (pirated content, etc.) will not be allowed under any circumstances.")
        await rules_channel.send(f"__**Staff Team:**__\nPlease do not message staff unless it is necessary. You can view this list by running `p!liststaff`.\n" + "\n".join(staff_list), allowed_mentions=discord.AllowedMentions(users = True))
        await rules_channel.send(f"__**Agreement:**__\nWhen agreeing to the server rules, you are accepting the fact that members of staff can and will take action against you if necessary, and can punish you for any reason. You are also allowing all bots on the server to store data about you, such as, your user ID, messages, and anything necessary to perform proper server functions. The server is required to inform you to accept the collecting of this data, per Discord's Developer Terms of Service (<https://discordapp.com/developers/docs/legal>). We also require you to agree and abide by Discord's Terms of Service (<https://discordapp.com/terms>) Finally, we are required by Discord's new Terms of Service to ask you to agree to the Children's Online Privacy Protection Rule (<https://www.ftc.gov/enforcement/rules/rulemaking-regulatory-reform-proceedings/childrens-online-privacy-protection-rule>). These documents, as well as these rules, will change over time. If you do not agree to these terms, please leave the server.")
        await ctx.reply(f"The rules have successfully been sent to {rules_channel.mention}.")

def setup(bot): bot.add_cog(Moderation(bot))