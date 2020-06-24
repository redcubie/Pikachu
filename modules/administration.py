import discord, os, importlib, asyncio
from discord.ext import commands
import configuration.variables as variables

class Administration(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, channel: discord.TextChannel, *, message): # p!say
        checkchannel = self.bot.get_channel(channel.id)
        pollchannel = self.bot.get_channel(variables.VOTING) # Channel #voting.
        if checkchannel == pollchannel:
            await ctx.send(f"{ctx.author.mention}, in order to send messages to {channel.mention}, please use `p!poll`.")
        else:
            async with channel.typing():
                characters = len(message)
                await asyncio.sleep(characters/10)
            await channel.send(f"{message}")
            if channel != ctx.channel:
                embed=discord.Embed(color=0x80ff80)
                embed.add_field(name="Sent Message:", value=message, inline=False)
                await ctx.send(f"{ctx.author.mention}, successfully sent the message to {channel.mention}.", embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def send(self, ctx, member: discord.Member, *, message): # p!send
        async with member.typing():
            characters = len(message)
            await asyncio.sleep(characters/10)
        try:
            await member.send(f"{message}")
            embed=discord.Embed(color=0x80ff80)
            embed.add_field(name="Sent Message:", value=message, inline=False)
            await ctx.send(f"{ctx.author.mention}, successfully sent the message to {member.mention}.", embed=embed)
        except discord.errors.Forbidden:
            pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sendrole(self, ctx, role: discord.Role, *, message): # p!sendrole
        members = (member for member in role.members if not member.bot)
        count = 0
        for member in members:
            async with member.typing():
                characters = len(message)
                await asyncio.sleep(characters/10)
            try:
                await member.send(f"{message}")
                count += 1
            except discord.errors.Forbidden:
                pass
        embed=discord.Embed(color=0x80ff80)
        embed.add_field(name="Sent Message:", value=message, inline=False)
        if count == 1:
            await ctx.send(f"{ctx.author.mention}, successfully sent the message to {count} user.", embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention}, successfully sent the message to {count} users.", embed=embed)
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def botstatus(self, ctx, status): # p!botstatus
        status = status.lower()
        if status == "online":
            await self.bot.change_presence(status=discord.Status.online)
        elif status == "idle":
            await self.bot.change_presence(status=discord.Status.idle)
        elif status == "do-not-disturb":
            await self.bot.change_presence(status=discord.Status.dnd)
        elif status == "invisible":
            await self.bot.change_presence(status=discord.Status.invisible)
        elif status == "offline":
            await self.bot.change_presence(status=discord.Status.offline)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def botaction(self, ctx, action, *, text=None): # p!botaction
        action = action.lower()
        if action == "playing" and text != None:
            activity = discord.Activity(name=text, type=discord.ActivityType.playing)
            await self.bot.change_presence(activity=activity)
        elif action == "watching" and text != None:
            activity = discord.Activity(name=text, type=discord.ActivityType.watching)
            await self.bot.change_presence(activity=activity)
        elif action == "listening" and text != None:
            activity = discord.Activity(name=text, type=discord.ActivityType.listening)
            await self.bot.change_presence(activity=activity)
        elif action == "default" and text == None:
            activity = discord.Activity(name=variables.STATUSACTIVITY, type=variables.STATUSTYPE)
            await self.bot.change_presence(activity=activity)
        elif action == "playing" or action == "watching" or action == "listening" and text == None:
            await ctx.send(f"{ctx.author.mention}, please specifiy something to go alongside the activity.")
        elif action != "playing" or action != "watching" or action != "listening" and action != None:
            await ctx.send(f"{ctx.author.mention}, that is not a valid action for the activity.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def vote(self, ctx, text, question, *choices: str): # p!poll
        if len(choices) <= 1:
            await ctx.send(f"{ctx.author.mention}, you need more than one choice to make a poll!")
        elif len(choices) > 10:
            await ctx.send(f"{ctx.author.mention}, you cannot make a poll with more than ten choices!")
        else:
            reactions = [
            "\U0001F1E6",
            "\U0001F1E7",
            "\U0001F1E8",
            "\U0001F1E9",
            "\U0001F1EA",
            "\U0001F1EB",
            "\U0001F1EC",
            "\U0001F1ED",
            "\U0001F1EE",
            "\U0001F1EF",
            ]
            description = []
            for x, option in enumerate(choices):
                description += "\n {} {}".format(reactions[x], option)
            embed = discord.Embed(title=question, description="".join(description), color=0xffff40)
            checkchannel = self.bot.get_channel(ctx.channel.id)
            pollchannel = self.bot.get_channel(variables.VOTING) # Channel #voting.
            pollmessage = await pollchannel.send(f"{text}", embed=embed)
            for reaction in reactions[:len(choices)]:
                await pollmessage.add_reaction(reaction)
            if checkchannel != pollchannel:
                await ctx.send(f"{ctx.author.mention}, successfully sent the poll to {pollchannel.mention}. A preview is attached.", embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def rolecopy(self, ctx, source: discord.Role, destination: discord.Role): # p!rolecopy
        await destination.edit(permissions=source.permissions, hoist=source.hoist, mentionable=source.mentionable)
        await ctx.send(f"{ctx.author.mention}, role permissions from {source.mention} have sucessfully been copied to {destination.mention}.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reboot(self, ctx): # p!reboot
        print("Bot reboot has been requested.")
        await ctx.send(f"{ctx.author.mention}, rebooting the system. Please wait a moment.")
        await ctx.bot.logout()

    @botstatus.error
    async def botstatus_error(self, ctx, error): # p!botstatus error handlers.
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, please specifiy a status to set the bot to.")

    @botaction.error
    async def botaction_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument): # p!botaction error handlers.
            await ctx.send(f"{ctx.author.mention}, please specifiy an action for the activity.")
    
def setup(bot): bot.add_cog(Administration(bot))
