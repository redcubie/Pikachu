import discord, os, asyncio, pymongo, re
from discord.ext import commands; from pymongo import MongoClient
import configuration.variables as variables

class Friends(commands.Cog):
    "Commands which manage friend codes and IDs for services."
    def __init__(self, bot): self.bot = bot

    @commands.command(aliases = ["friendlink", "fcadd"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def accountlink(self, ctx, system, code): # p!accountlink
        "Links a friend code or username to the database.\nValid systems are \"3ds\", \"switch\", and \"wiiu\".\nLinked accounts can include \"Nintendo Switch\", \"Nintendo 3DS\", and \"Nintendo Wii U\"."
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Friends"]
        
        async def check_3DS_ID(code):
            return (True if re.match(r"^(\d{4}-\d{4}-\d{4}|\d{12})$", code) else False)
        async def check_Switch_ID(code):
            return (True if re.match(r"^(SW-\d{4}-\d{4}-\d{4}|SW\d{12}|\d{4}-\d{4}-\d{4}|\d{12})$", code) else False)
        async def check_WiiU_ID(code):
            if len(code) < 6 or len(code) > 16 or re.search(r"[^a-zA-Z\d\.\-\_]", code): return False
            return (False if re.search(r"^[\.\-\_]|[\.\-\_]$", code) or re.search(r"[\.\-\_][\.\-\_]", code) else True)

        if system.lower() == "wiiu":
            collection = database["Nintendo Wii U"]
            if not await check_WiiU_ID(code): return await ctx.reply("The account you have provided is invalid.")

        elif system.lower() == "3ds":
            collection = database["Nintendo 3DS"]
            if not await check_3DS_ID(code): return await ctx.reply("The account you have provided is invalid.")
            if len(code) == 12: code = "-".join((code[0:4], code[4:8], code[8:12]))

        elif system.lower() in {"switch", "nx"}:
            collection = database["Nintendo Switch"]; code = code.upper()
            if not await check_Switch_ID(code):
                return await ctx.reply("The account you have provided is invalid.")
            if len(code) == 12:
                code = "-".join(("SW", code[0:4], code[4:8], code[8:12]))
            elif len(code) == 14 and code.startswith("SW"):
                code = "-".join((code[0:2], code[2:6], code[6:10], code[10:14]))
            elif len(code) == 14 and not code.startswith("SW"): code = "SW-" + code

        else: await ctx.reply("The system you have specified is not supported.")
        if collection.count_documents({"_id": ctx.author.id}, limit = 1) == 0:
            post = {"_id": ctx.author.id, "Account": None}
            collection.insert_one(post)
        collection.update_one({"_id": ctx.author.id}, {"$set":{"Account": code}})
        await ctx.reply("Your account has been linked successfully.")

    @commands.command(aliases = ["friendunlink", "fcremove"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def accountunlink(self, ctx, system): # p!accountunlink
        "Unlinks a friend code or username from the database.\nValid systems are \"3ds\", \"switch\", and \"wiiu\".\nLinked accounts can include \"Nintendo Switch\", \"Nintendo 3DS\", and \"Nintendo Wii U\"."
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Friends"]
        if system.lower() == "wiiu": collection = database["Nintendo Wii U"]
        elif system.lower() == "3ds": collection = database["Nintendo 3DS"]
        elif system.lower() in {"switch", "nx"}: collection = database["Nintendo Switch"]

        if collection.count_documents({"_id": ctx.author.id}, limit = 1) == 1:
            collection.delete_one({"_id": ctx.author.id})
            return await ctx.reply("Your account has been unlinked successfully.")
        else: return await ctx.reply("No account for this system has been linked.")

    @commands.command(aliases = ["friendcheck", "fc"])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def accountview(self, ctx, member: discord.Member = None): # p!accountcheck
        "Shows a user's linked friend codes and usernames.\nLinked accounts can include \"Nintendo 3DS\", \"Nintendo Switch\", and \"Nintendo Wii U\"."
        cluster = MongoClient(variables.DBACCOUNT)
        database = cluster["Friends"]
        if member == None: member = ctx.author
        embed = discord.Embed(color = 0xffff40)
        account_counter = 0

        collection = database["Nintendo 3DS"]
        if collection.count_documents({"_id": member.id}, limit = 1) == 1:
            account_counter = account_counter + 1
            results = collection.find({"_id": member.id})
            for result in results: account_ID = result["Account"]
            embed.add_field(name = "Nintendo 3DS (Friend Code)", value = account_ID, inline = False)

        collection = database["Nintendo Switch"]
        if collection.count_documents({"_id": member.id}, limit = 1) == 1:
            account_counter = account_counter + 1
            results = collection.find({"_id": member.id})
            for result in results: account_ID = result["Account"]
            embed.add_field(name = "Nintendo Switch (Friend Code)", value = account_ID, inline = False)

        collection = database["Nintendo Wii U"]
        if collection.count_documents({"_id": member.id}, limit = 1) == 1:
            account_counter = account_counter + 1
            results = collection.find({"_id": member.id})
            for result in results: account_ID = result["Account"]
            embed.add_field(name = "Nintendo Wii U (Username)", value = account_ID, inline = False)

        embed.set_footer(text = "Update accounts with p!accountlink.")
        if account_counter > 0 and member == ctx.author:
            return await ctx.reply("Here's your list of linked accounts.", embed = embed)
        elif account_counter > 0 and member != ctx.author:
            return await ctx.reply(f"Here's the list of linked accounts for {member.mention}.", embed = embed)
        elif account_counter == 0 and member != ctx.author:
            return await ctx.reply(f"{member.mention} has not linked any accounts.")
        else: await ctx.reply("You have not linked any acccounts.")
    
def setup(bot): bot.add_cog(Friends(bot))