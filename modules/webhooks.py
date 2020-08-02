import discord, os, dhooks
from discord.ext import commands
import configuration.variables as variables

class Webhooks(commands.Cog):
    "Webhook intergrations used with the server in certain instances."
    def __init__(self, bot): self.bot = bot

    @commands.command()
    async def sakurai(self, ctx): # p!sakurai
        "A testing command to ensure the functionality of webhooks."
        sakuraiHook = dhooks.Webhook(variables.SAKURAIHOOK)
        sakuraiHook.send("Hello! The Masahiro Sakurai webhook is online!")

def setup(bot): bot.add_cog(Webhooks(bot))