import discord, os, random
from discord.ext import commands

class Games(commands.Cog):
    "Games which can be played through the Discord platform."
    def __init__(self, bot): self.bot = bot

    @commands.command(aliases=["guess"])
    async def guessing(self, ctx, difficulty = "medium"):
        "A simple number guessing game that you can play! Choose from easy, medium, hard, or extreme difficulties."
        if difficulty.lower() == "easy": difficultyNumber = 10
        elif difficulty.lower() == "hard": difficultyNumber = 1000
        elif difficulty.lower() == "extreme": difficultyNumber = 10000
        else: difficultyNumber = 100
        number = random.randint(1, difficultyNumber)
        await ctx.send(f"A random integer has been generated from 1 to {difficultyNumber}. Enter your guess!")
        while True:
            response = await self.bot.wait_for("message")
            if ctx.author.id == response.author.id and ctx.channel.id == response.channel.id:
                guess = int(response.content)
                if isinstance(guess, int) == False:
                    break
                if guess < 1 or guess > difficultyNumber:
                    await ctx.send("But wait, that's illegal!")
                elif guess > number:
                    await ctx.send("Your guess is too high. Enter another guess!")
                elif guess < number:
                    await ctx.send('Your guess is too low. Enter another guess!')
                else:
                    await ctx.send(f"You guessed it correctly! The correct integer is {guess}.")
                    break
            else:
                pass

def setup(bot): bot.add_cog(Games(bot)) 