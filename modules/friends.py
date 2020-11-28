import discord, os, asyncio, pymongo, re
from discord.ext import commands; from pymongo import MongoClient
import configuration.variables as variables

class Friends(commands.Cog):
    "Commands which manage friend codes and IDs for services."
    def __init__(self, bot): self.bot = bot

    @commands.command(aliases=["friendlink", "fcadd"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def accountlink(self, ctx, system, code): # p!accountlink
        "Links a friend code or username to the database.\nValid argument options are \"3ds\", \"switch\", \"nx\", and \"wiiu\".\nLinked profiles can include \"Nintendo Switch\", \"Nintendo 3DS\", and \"Nintendo Wii U\"."
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Friends"]
        async def checkIDWiiU(code):
            if len(code) < 6 or len(code) > 16: return False
            if code.startswith((".", "!", "_")) or code.endswith((".", "!", "_")): return False
            else: return True
        async def checkID3DS(code):
            if len(code) != 12 and len(code) != 14: return False
            if len(code) == 12 and code.isdigit() == False: return False
            if len(code) == 14 and (code[4] != "-" or code[9] != "-"): return False
            if re.search('[a-zA-Z]', code): return False
            else: return True
        async def checkIDSwitch(code):
            if len(code) != 12 and len(code) != 14 and len(code) != 17: return False
            if len(code) == 12 and code.isdigit() == False: return False
            if len(code) == 14 and code.startswith("SW") == False and (code[4] != "-" or code[9] != "-"): return False
            if len(code) == 17 and code.startswith("SW") and (code[3] != "-" or code[8] != "0" or code[13] != "-"): return False
            else: return True
        if system.lower() == "wiiu":
            collection = database["Nintendo Wii U"]
            if await checkIDWiiU(code) == False: return await ctx.send(f"{ctx.author.mention}, the account you have provided is invalid.")
        elif system.lower() == "3ds":
            collection = database["Nintendo 3DS"]
            if await checkID3DS(code) == False: return await ctx.send(f"{ctx.author.mention}, the account you have provided is invalid.")
            if len(code) == 12: code = "-".join((code[0:4], code[4:8], code[8:12]))
        elif system.lower() == "switch" or system.lower() == "nx":
            collection = database["Nintendo Switch"]
            if await checkIDSwitch(code) == False: return await ctx.send(f"{ctx.author.mention}, the account you have provided is invalid.")
            if len(code) == 12: code = "-".join(("SW", code[0:4], code[4:8], code[8:12]))
            elif len(code) == 14 and code.startswith("SW"): code = "-".join((code[0:2], code[2:6], code[6:10], code[10:14]))
            elif len(code) == 14 and code.startswith("SW") == False: code = "SW-" + code
        else: await ctx.send(f"{ctx.author.mention}, the system you have specified is not supported.")
        if collection.count_documents({"_id": ctx.author.id}, limit = 1) == 0:
            post = {"_id": ctx.author.id, "Profile": None}
            collection.insert_one(post)
        collection.update_one({"_id": ctx.author.id}, {"$set":{"Profile": code}})
        await ctx.send(f"{ctx.author.mention}, your account has been linked successfully.")

    @commands.command(aliases=["friendunlink", "fcremove"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def accountunlink(self, ctx, system): # p!accountunlink
        "Unlinks a friend code or profile from the database.\nValid argument options are \"3ds\", \"switch\", \"nx\", and \"wiiu\".\nLinked profiles can include \"Nintendo Switch\", \"Nintendo 3DS\", and \"Nintendo Wii U\"."
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Friends"]
        if system.lower() == "wiiu": collection = database["Nintendo Wii U"]
        elif system.lower() == "3ds": collection = database["Nintendo 3DS"]
        elif system.lower() == "switch" or system.lower() == "nx": collection = database["Nintendo Switch"]
        if collection.count_documents({"_id": ctx.author.id}, limit = 1) == 1:
            collection.delete_one({"_id": ctx.author.id})
            return await ctx.send(f"{ctx.author.mention}, your account has been unlinked successfully.")
        else: return await ctx.send(f"{ctx.author.mention}, no account for this system has been linked.")

    @commands.command(aliases=["fcview", "fc"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def accountcheck(self, ctx, member: discord.Member = None): # p!accountcheck
        "Shows a user's linked friend codes and usernames.\nLinked accounts can include \"Nintendo 3DS\", \"Nintendo Switch\", and \"Nintendo Wii U\"."
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Friends"]
        if member == None: member = ctx.author
        embed = discord.Embed(color=0xffff40)
        accountCounter = 0
        collection = database["Nintendo 3DS"]
        if collection.count_documents({"_id": member.id}, limit = 1) == 1:
            accountCounter = accountCounter + 1
            results = collection.find({"_id": member.id})
            for result in results: accountCode = result["Account"]
            embed.add_field(name="Nintendo 3DS", value=accountCode, inline=False)
        collection = database["Nintendo Switch"]
        if collection.count_documents({"_id": member.id}, limit = 1) == 1:
            accountCounter = accountCounter + 1
            results = collection.find({"_id": member.id})
            for result in results: accountCode = result["Account"]
            embed.add_field(name="Nintendo Switch", value=accountCode, inline=False)
        collection = database["Nintendo Wii U"]
        if collection.count_documents({"_id": member.id}, limit = 1) == 1:
            accountCounter = accountCounter + 1
            results = collection.find({"_id": member.id})
            for result in results: accountCode = result["Account"]
            embed.add_field(name="Nintendo Wii U", value=accountCode, inline=False)
        embed.set_footer(text=f"Update accounts with p!friendadd.")
        if accountCounter > 0 and member == ctx.author: return await ctx.send(f"{ctx.author.mention}, here's your list of linked accounts.", embed=embed)
        elif accountCounter > 0 and member != ctx.author: return await ctx.send(f"{ctx.author.mention}, here's the list of linked accounts for {member.mention}.", embed=embed)
        elif accountCounter == 0 and member != ctx.author: return await ctx.send(f"{ctx.author.mention}, {member.mention} has not linked any accounts.")
        else: await ctx.send(f"{ctx.author.mention}, you have not linked any acccounts.")
    
def setup(bot): bot.add_cog(Friends(bot))