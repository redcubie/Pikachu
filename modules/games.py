import discord, os, random
from discord.ext import commands

class Games(commands.Cog):
    "Games which can be played through the Discord platform."
    def __init__(self, bot): self.bot = bot

    @commands.command()
    async def guessing(self, ctx):
        "A simple number guessing game that you can play!"
        number = random.randint(0, 100)
        await ctx.send("A random interger has been generated from 1 to 100. Enter your guess!")
        while True:
            response = await self.bot.wait_for("message")
            guess = int(response.content)
            if isinstance(guess, int) == False:
                break
            if guess < 1 or guess > 100:
                await ctx.send("But wait, that's illegal!")
            elif guess > number:
                await ctx.send("Your guess is too high. Enter another guess!")
            elif guess < number:
                await ctx.send('Your guess is too low. Enter another guess!')
            else:
                await ctx.send(f"You guessed it correctly! The correct interger is {guess}.")
                break

def setup(bot): bot.add_cog(Games(bot)) 