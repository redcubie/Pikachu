import discord, os, importlib, shutil
from discord.ext import commands; from discord.utils import get
import configuration.variables as variables; import configuration.arrays as arrays

class Events(commands.Cog):
    "Actions called when certain things happen."
    def __init__(self, bot): self.bot = bot

    @commands.Cog.listener() # The bot startup process.
    async def on_ready(self):
        activity = discord.Activity(name=variables.STATUSACTIVITY, type=variables.STATUSTYPE)
        await self.bot.change_presence(activity=activity)
        queueInFile = os.path.isdir("./queue")
        if queueInFile is True: shutil.rmtree("./queue")
        songThere = os.path.isfile("song.mp3")
        if songThere: os.remove("song.mp3")
        print("Bot is active. It will take commands and appear online now.")

    @commands.Cog.listener() # When a user joins.
    async def on_member_join(self, user):
        print("Member has joined the server.")
        channel = self.bot.get_channel(variables.SERVERLOGS) # Channel #server-logs.
        embed=discord.Embed(color=0x8080ff)
        embed.set_thumbnail(url=user.avatar_url_as(static_format="png"))
        formatCreate = user.created_at
        formatCreate2 = formatCreate.strftime("%B %d, %Y (%I:%M %p)")
        formatJoin = user.joined_at
        formatJoin2 = formatJoin.strftime("%B %d, %Y (%I:%M %p)")
        embed.add_field(name="Created:", value="{}".format(formatCreate2), inline=False)
        embed.add_field(name="Joined:", value="{}".format(formatJoin2), inline=False)
        embed.set_footer(text="Use the command \"p!userinfo\" for more information.")
        await channel.send(f"{user.mention} ({user.id}) has joined the server.", embed=embed)

    @commands.Cog.listener() # When a user leaves.
    async def on_member_remove(self, user):
        print("Member has left the server.")
        channel = self.bot.get_channel(variables.SERVERLOGS) # Channel #server-logs.
        embed=discord.Embed(color=0x8080ff)
        embed.set_thumbnail(url=user.avatar_url_as(static_format="png"))
        formatCreate = user.created_at
        formatCreate2 = formatCreate.strftime("%B %d, %Y (%I:%M %p)")
        formatJoin = user.joined_at
        formatJoin2 = formatJoin.strftime("%B %d, %Y (%I:%M %p)")
        embed.add_field(name="Creation Date and Time:", value="{}".format(formatCreate2), inline=False)
        embed.add_field(name="Server Join Date and Time:", value="{}".format(formatJoin2), inline=False)
        embed.set_footer(text="Use the command \"p!userinfo\" for more information.")
        await channel.send(f"{user.mention} ({user.id}) has left the server.", embed=embed)

    @commands.Cog.listener() # When a message is edited.
    async def on_message_edit(self, before, after):
        if not isinstance(after.channel, discord.channel.DMChannel):
            if before.content.strip() != after.content.strip():
                print("Message has been edited.")
                logChannel = self.bot.get_channel(variables.MESSAGELOGS) # Channel #message-logs.
                embed=discord.Embed(color=0x80ff80)
                embed.add_field(name="Message Before:", value=before.content, inline=False)
                embed.add_field(name="Message After:", value=after.content, inline=False)
                try: await logChannel.send(f"A message by {before.author.mention} ({before.author.id}) has been edited in {before.channel.mention}.", embed=embed)
                except AttributeError: pass
            else: pass

    @commands.Cog.listener() # When a message is deleted.
    async def on_message_delete(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            currentChannel = ctx.channel.id
            if currentChannel in arrays.LOGCHANNELS: pass
            else:
                print("Message has been deleted.")
                logChannel = self.bot.get_channel(variables.MESSAGELOGS)
                embed=discord.Embed(color=0x80ff80)
                embed.add_field(name="Deleted Message:", value=ctx.content, inline=False)
                try: await logChannel.send(f"A message by {ctx.author.mention} ({ctx.author.id}) has been deleted in {ctx.channel.mention}.", embed=embed)
                except AttributeError: pass

    @commands.Cog.listener() # When a member update is detected.
    async def on_member_update(self, before, after):
        pass

def setup(bot): bot.add_cog(Events(bot))
