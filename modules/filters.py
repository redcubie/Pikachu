import discord, os, importlib, re
from discord.ext import commands; from string import printable
import configuration.variables as variables; import configuration.arrays as arrays

class Filters(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx): # Initial message filtering.
        msgcheck = "".join(char for char in ctx.content.lower() if char in printable)
        msg_no_separators = re.sub(r"[ \*_\-~.!`@#$%^&+=?/|)(]", "", msgcheck)
        filter_alert = any(x in msg_no_separators for x in arrays.MESSAGEFILTER)
        if filter_alert:
            try:
                ownerrole = discord.utils.get(ctx.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
                modrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
                botrole = discord.utils.get(ctx.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
                logchannel = self.bot.get_channel(variables.MESSAGELOGS) # Channel #message-logs.
                if ownerrole in ctx.author.roles or modrole in ctx.author.roles or botrole in ctx.author.roles:
                    pass
                elif ctx.channel.id in arrays.UNFILTERCHANNELS:
                    pass
                else:
                    print("Filter has been set off.")
                    await ctx.delete()
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Deleted Message:", value=ctx.content, inline=False)
                    try:
                        await ctx.author.send(f"Your message has been automatically deleted as it violated the server rules. Please read <#450903022613168129> for more information.", embed=embed)
                    except discord.errors.Forbidden:
                        pass
                    await logchannel.send(f"{ctx.author} ({ctx.author.id}) has sent a message in {ctx.channel.mention} in violation of the server rules which was automatically deleted.", embed=embed)
            except AttributeError:
                pass

    @commands.Cog.listener() # Message edit filtering.
    async def on_message_edit(self, before, after):
        if before.content.strip() != after.content.strip():
            msgcheck = "".join(char for char in after.content.lower() if char in printable)
            msg_no_separators = re.sub(r"[ \*_\-~.!`@#$%^&+=?/|)(]", "", msgcheck)
            filter_alert = any(x in msg_no_separators for x in arrays.MESSAGEFILTER)
            if filter_alert:
                try:
                    ownerrole = discord.utils.get(after.guild.roles, id=variables.SERVEROWNER) # Role @Server Owner.
                    modrole = discord.utils.get(after.guild.roles, id=variables.SERVERMODERATOR) # Role @Server Moderator.
                    botrole = discord.utils.get(after.guild.roles, id=variables.SERVERBOT) # Role @Server Bot.
                    logchannel = self.bot.get_channel(variables.MESSAGELOGS) # Channel #message-logs.
                    if ownerrole in after.author.roles or modrole in after.author.roles or botrole in after.author.roles: pass
                    else:
                        print("Filter has been set off.")
                        await after.delete()
                        embed = discord.Embed(color=0xff8080)
                        embed.add_field(name="Deleted Message:", value=after.content, inline=False)
                        try: await after.author.send(f"Your message has been automatically deleted as it violated the server rules. Please read <#450903022613168129> for more information.", embed=embed)
                        except discord.errors.Forbidden: pass
                        await logchannel.send(f"{after.author} ({after.author.id}) has sent a message in violation of the server rules which was automatically deleted.", embed=embed)
                except AttributeError: pass

def setup(bot): bot.add_cog(Filters(bot))