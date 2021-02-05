import discord, os, importlib, re
from discord.ext import commands; from string import printable
from manager import check_staff_member
import configuration.variables as variables
import configuration.arrays as arrays

class Filters(commands.Cog):
    "Word filter that will delete messages which trigger it."
    def __init__(self, bot): self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx): # Initial message filtering.
        logChannel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #message-logs.
        messageCheck = "".join(char for char in ctx.content.lower() if char in printable)
        messageNoSeparators = re.sub(r"[ \*_\-~.!`@#$%^&+=?/|)(]", "", messageCheck)
        filterAlert = any(x in messageNoSeparators for x in arrays.MESSAGEFILTER)
        if filterAlert:
            try:
                if check_staff_member(ctx.author): return None
                if ctx.channel.id in arrays.CHANNELINFORMATION:
                    info = arrays.CHANNELINFORMATION.get(ctx.channel.id)
                    filterSetting = info.get("Filter")
                    if filterSetting: return None
                print("Filter has been set off.")
                await ctx.delete()
                embed = discord.Embed(color=0xff8080)
                embed.add_field(name="Deleted Message", value=ctx.content, inline=False)
                try: await ctx.author.send(f"Your message has been automatically deleted as it violated the server rules. Please read <#450903022613168129> for more information.", embed=embed)
                except discord.errors.Forbidden: pass
                await logChannel.send(f"{ctx.author.mention} ({ctx.author.id}) has sent a message in {ctx.channel.mention} in violation of the server rules which was automatically deleted.", embed=embed)
            except AttributeError: pass

    @commands.Cog.listener() # Message edit filtering.
    async def on_message_edit(self, before, after):
        if before.content.strip() != after.content.strip():
            logChannel = self.bot.get_channel(variables.ACTIONLOGS) # Channel #message-logs.
            messageCheck = "".join(char for char in after.content.lower() if char in printable)
            messageNoSeparators = re.sub(r"[ \*_\-~.!`@#$%^&+=?/|)(]", "", messageCheck)
            filterAlert = any(x in messageNoSeparators for x in arrays.MESSAGEFILTER)
            if filterAlert:
                try:
                    if check_staff_member(before.author): return None
                    if before.channel.id in arrays.CHANNELINFORMATION:
                        info = arrays.CHANNELINFORMATION.get(before.channel.id)
                        filterSetting = info.get("Filter")
                        if filterSetting: return None
                    print("Filter has been set off.")
                    await after.delete()
                    embed = discord.Embed(color=0xff8080)
                    embed.add_field(name="Deleted Message", value=after.content, inline=False)
                    try: await after.author.send(f"Your message has been automatically deleted as it violated the server rules. Please read <#450903022613168129> for more information.", embed=embed)
                    except discord.errors.Forbidden: pass
                    await logChannel.send(f"{after.author.mention} ({after.author.id}) has sent a message in violation of the server rules which was automatically deleted.", embed=embed)
                except AttributeError: pass

def setup(bot): bot.add_cog(Filters(bot))