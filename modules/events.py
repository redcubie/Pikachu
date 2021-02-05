import discord, os, importlib, shutil
from discord.ext import commands; from discord.utils import get
import configuration.variables as variables
import configuration.arrays as arrays

class Events(commands.Cog):
    "Actions called when certain things happen."
    def __init__(self, bot): self.bot = bot

    async def userJoinLeaveInfo(self, user):
        global embed
        embed=discord.Embed(color=0x8080ff)
        embed.set_thumbnail(url=user.avatar_url_as(static_format="png"))
        embed.add_field(name="Account Name", value=user.name, inline=True)
        embed.add_field(name="Discriminator", value="#"+user.discriminator, inline=False)
        embed.add_field(name="Account Identification", value=user.id, inline=False)
        formatCreate = user.created_at
        formatCreate2 = formatCreate.strftime("%B %d, %Y (%I:%M %p)")
        formatJoin = user.joined_at
        formatJoin2 = formatJoin.strftime("%B %d, %Y (%I:%M %p)")
        embed.add_field(name="Creation Date and Time", value=f"{formatCreate2}", inline=False)
        embed.add_field(name="Server Join Date and Time", value=f"{formatJoin2}", inline=False)
        embed.set_footer(text="Use the command \"p!userinfo\" for more information.")

    @commands.Cog.listener() # The bot startup process.
    async def on_ready(self):
        activity = discord.Activity(name=variables.STATUSACTIVITY, type=variables.STATUSTYPE)
        await self.bot.change_presence(activity=activity)
        print("Bot is active. It will take commands and appear online now.")

    @commands.Cog.listener() # When a user joins.
    async def on_member_join(self, user):
        print("Member has joined the server.")
        channel = self.bot.get_channel(variables.SERVERLOGS) # Channel #server-logs.
        await self.userJoinLeaveInfo(user)
        await channel.send(f"{user.mention} ({user.id}) has joined the server.", embed=embed)

    @commands.Cog.listener() # When a user leaves.
    async def on_member_remove(self, user):
        print("Member has left the server.")
        channel = self.bot.get_channel(variables.SERVERLOGS) # Channel #server-logs.
        await self.userJoinLeaveInfo(user)
        await channel.send(f"{user.mention} ({user.id}) has left the server.", embed=embed)

    @commands.Cog.listener() # When a member update is detected.
    async def on_member_update(self, before, after):
        pass

def setup(bot): bot.add_cog(Events(bot))