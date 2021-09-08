import discord, os, importlib, asyncio, sys
from discord.ext import commands
from manager import is_staff_member
import configuration.variables as variables
import configuration.arrays as arrays

class Administration(commands.Cog):
    "Powerful commands which can be used by an administrator."
    def __init__(self, bot): self.bot = bot

    @commands.command(aliases = ["countactive"])
    @commands.guild_only()
    @is_staff_member()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def activecount(self, ctx, days = 30): # p!checkactivity
        "Estimates the amount of active members on the server.\nThis command is only usable by staff members."
        if days < 1: return await ctx.reply("The minimum allowed days is 1.")
        if days > 30: return await ctx.reply("The maximum allowed days is 30.")
        async with ctx.channel.typing():
            count = await ctx.guild.estimate_pruned_members(days = days)
            await asyncio.sleep(1)
            if days == 1:
                await ctx.reply(f"Over the past {days} day, approximately {ctx.guild.member_count-count:,} members were counted as active.")
            else:
                await ctx.reply(f"Over the past {days} days, approximately {ctx.guild.member_count-count:,} members were counted as active.")

    @commands.command(aliases = ["speak"])
    @commands.guild_only()
    @is_staff_member()
    async def say(self, ctx, channel: discord.TextChannel, *, message): # p!say
        "Sends a message to a specified channel.\nThis command is only usable by staff members."
        if channel.id in arrays.CHANNELINFORMATION:
            info = arrays.CHANNELINFORMATION.get(channel.id)
            say_setting = info.get("Say")
            if not say_setting:
                return await ctx.reply(f"You are not allowed to send messages to {channel.mention}.")
        
        async with channel.typing():
            characters = len(message)
            await asyncio.sleep(characters/25)
        await channel.send(message, allowed_mentions =
            discord.AllowedMentions(everyone = True, roles = True, users = True))
        
        if channel != ctx.channel:
            embed=discord.Embed(color = 0x80ff80)
            embed.add_field(name = "Sent Message", value = message, inline = False)
            await ctx.reply(f"The message was successfully sent to {channel.mention}.", embed = embed)

    @commands.command(aliases = ["dm"])
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def send(self, ctx, member: discord.Member, *, message): # p!send
        "Sends a message to a specified user.\nThis command is only usable by administrators."
        async with member.typing():
            characters = len(message)
            await asyncio.sleep(characters/25)

        try:
            await member.send(message, allowed_mentions =
                discord.AllowedMentions(everyone = True, roles = True, users = True))
                
            embed=discord.Embed(color = 0x80ff80)
            embed.add_field(name = "Sent Message", value = message, inline = False)
            await ctx.reply(f"The message was successfully sent to {member.mention}.", embed = embed)
        except discord.errors.Forbidden: pass

    @commands.command(aliases = ["dmrole"])
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def sendrole(self, ctx, role: discord.Role, *, message): # p!sendrole
        "Sends a message to everyone with a specified role.\nThis command is only usable by administrators."
        members = (member for member in role.members if not member.bot)
        count = 0

        for member in members:
            async with member.typing(): characters = len(message); await asyncio.sleep(characters/25)
            try:
                await member.send(message, allowed_mentions = discord.AllowedMentions(everyone = True, roles = True, users = True)); count += 1
            except discord.errors.Forbidden: pass

        embed=discord.Embed(color = 0x80ff80)
        embed.add_field(name = "Sent Message", value = message, inline = False)
        if count == 1:
            await ctx.reply(f"The message was successfully sent to {count} user.", embed = embed)
        else:
            await ctx.reply(f"The message was successfully sent to {count} users.", embed = embed)

    @commands.command()
    @commands.guild_only()
    @is_staff_member()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def botaction(self, ctx, action, *, text = None): # p!botaction
        "Changes the text which shows under the bot.\nThis command is only usable by staff members.\nValid argument options are \"playing\", \"watching\", and \"listening\". You can also use \"default\" to reset the text.\nIncompatible with p!botstatus."
        action = action.lower()
        if action == "playing" and text != None:
            activity = discord.Activity(name = text, type = discord.ActivityType.playing)
            await self.bot.change_presence(activity = activity)
            return await ctx.reply(f"The activity has been successfully changed to \"Playing {text}\".")
        elif action == "watching" and text != None:
            activity = discord.Activity(name = text, type = discord.ActivityType.watching)
            await self.bot.change_presence(activity = activity)
            return await ctx.reply(f"The activity has been successfully changed to \"Watching {text}\".")
        elif action == "listening" and text != None:
            activity = discord.Activity(name = text, type = discord.ActivityType.listening)
            await self.bot.change_presence(activity = activity)
            return await ctx.reply(f"The activity has been successfully changed to \"Listening to {text}\".")
        elif action == "default" and text == None:
            activity = discord.Activity(name = variables.STATUSACTIVITY, type = variables.STATUSTYPE)
            await self.bot.change_presence(activity = activity)
            return await ctx.reply(f"The activity has been successfully changed to \"Watching {variables.STATUSACTIVITY}\".")
        else: return await ctx.reply("That is not a valid action for the activity.") # Some simple error handling.
        
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def botstatus(self, ctx, status): # p!botstatus
        "Changes the current presense of the bot.\nThis command is only usable by administrators.\nValid argument options are \"online\", \"idle\", \"do-not-disturb\", \"dnd\", \"invisible\", and \"offline\".\nIncompatible with p!botaction."
        status = status.lower()
        if status == "online":
            await self.bot.change_presence(status = discord.Status.online)
            await ctx.reply("The status has been successfully changed to show as online.")
        elif status == "idle":
            await self.bot.change_presence(status = discord.Status.idle)
            await ctx.reply("The status has been successfully changed to show as idle.")
        elif status == "dnd" or status == "do-not-disturb":
            await self.bot.change_presence(status = discord.Status.dnd)
            await ctx.reply("The status has been successfully changed to show as do not disturb.")
        elif status == "invisible":
            await self.bot.change_presence(status = discord.Status.invisible)
            await ctx.reply("The status has been successfully changed to show as invisible.")
        elif status == "offline":
            await self.bot.change_presence(status = discord.Status.offline)
            await ctx.reply("The status has been successfully changed to show as offline.")
        else: return await ctx.reply("That is not a valid status for the bot.") # Some simple error handling.

    @commands.command(aliases = ["vote"])
    @commands.guild_only()
    @is_staff_member()
    @commands.cooldown(1, 86400, commands.BucketType.guild)
    async def poll(self, ctx, question, *choices: str): # p!poll
        "Sends a poll to the specified voting channel.\nThis command is only usable by staff members."
        if len(choices) <= 1:
            return await ctx.reply("You need more than one choice to make a poll!")
        elif len(choices) > 10:
            return await ctx.reply("You cannot make a poll with more than ten choices!")
        else:
            reactions = ["\U0001F1E6", "\U0001F1E7", "\U0001F1E8", "\U0001F1E9", "\U0001F1EA",
            "\U0001F1EB", "\U0001F1EC", "\U0001F1ED",  "\U0001F1EE", "\U0001F1EF",]
            description = []

            for x, option in enumerate(choices):
                description += f"\n {reactions[x]} {option}"
            embed = discord.Embed(title = question, description = "".join(description), color = 0xffff40)
            embed.set_footer(text = f"This poll was posted by {ctx.author}.")

            current_channel = self.bot.get_channel(ctx.channel.id)
            poll_channel = self.bot.get_channel(variables.STAFFHANGOUT) # Channel #everybody-votes.
            poll_message = await poll_channel.send(embed = embed)

            for reaction in reactions[:len(choices)]:
                await poll_message.add_reaction(reaction)
            if current_channel != poll_channel:
                return await ctx.reply(f"The poll was successfully sent to {poll_channel.mention}. A preview is attached.", embed = embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def rolecopy(self, ctx, source: discord.Role, destination: discord.Role): # p!rolecopy
        "Grabs the permissions of one role and copies them to another.\nThis command is only usable by administrators."
        await destination.edit(permissions = source.permissions, hoist = source.hoist, mentionable = source.mentionable)
        await ctx.reply(f"Role permissions from {source.mention} have sucessfully been copied to {destination.mention}.")
    
def setup(bot): bot.add_cog(Administration(bot))
