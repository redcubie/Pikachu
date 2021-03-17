import discord, os, random
from discord.ext import commands

class Games(commands.Cog):
    "Games which can be played through the Discord platform."
    def __init__(self, bot): self.bot = bot

    @commands.command(aliases=["guess"])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def guessing(self, ctx, difficulty = "normal"):
        "A simple number guessing game that you can play.\nValid difficulties are \"easy\", \"normal\", \"hard\", and \"extreme\"."
        guessList = []; guessCounter = 0
        if difficulty.lower() == "easy": difficultyNumber = 10
        elif difficulty.lower() == "hard": difficultyNumber = 1000
        elif difficulty.lower() == "extreme": difficultyNumber = 10000
        else: difficulty = "normal"; difficultyNumber = 100
        number = random.randint(1, difficultyNumber)
        async def guessEmbed():
            global embed
            embed = discord.Embed(color=0xffff40)
            embed.add_field(name="Current Difficulty", value=f"{difficulty.capitalize()} ({difficultyNumber})", inline=False)
            if len(guessList) != 0: embed.add_field(name="Attempted Guesses", value=f", ".join(guessList), inline=False)
            else: embed.add_field(name="Attempted Guesses", value="None", inline=False)
        await ctx.send(f"{ctx.author.mention}, a random integer has been generated from 1 to {difficultyNumber}. Enter your guess!")
        while True:
            response = await self.bot.wait_for("message")
            if ctx.author.id == response.author.id and ctx.channel.id == response.channel.id:
                guess = int(response.content)
                if isinstance(guess, int) == False: break
                if guess < 1 or guess > difficultyNumber:
                    await guessEmbed()
                    await ctx.send(f"{ctx.author.mention}, but wait, that's illegal! Enter another guess!", embed=embed)
                else:
                    if guessCounter <= 8:
                        if str(guess) not in guessList:
                            guessList.append(str(guess)); guessCounter += 1
                        guessList.sort(key=int)
                        if guess > number:
                            await guessEmbed()
                            await ctx.send(f"{ctx.author.mention}, your guess is too high. Enter another guess!", embed=embed)   
                        elif guess < number:
                            await guessEmbed()
                            await ctx.send(f"{ctx.author.mention}, your guess is too low. Enter another guess!", embed=embed)
                        else: return await ctx.send(f"{ctx.author.mention}, you guessed the integer correctly! The correct integer is {guess}.")
                    else:
                        if guess == number: return await ctx.send(f"{ctx.author.mention}, you guessed the integer correctly! The correct integer is {guess}.")
                        else: return await ctx.send(f"{ctx.author.mention}, you were unable to guess the integer. The correct integer is {number}.")
            else: pass

    @commands.command(aliases=["8ball"])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def magicball(self, ctx):
        "Randomly selects a prediction/response using magic."
        magicAnswers = [
            "As I see it, yes.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "It is certain.",
            "It is decidedly so.",
            "Most likely.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Outlook good.",
            "Reply hazy, try again.",
            "Signs point to yes.",
            "Very doubtful.",
            "Without a doubt.",
            "Yes.",
            "Yes – definitely.",
            "You may rely on it.",
        ]
        magicAnswer = random.choice(magicAnswers)
        if random.randint(1, 100) == 1: magicAnswer = "My uncle says it's confirmed." # Secret prediction. :)
        elif random.randint(1, 100) == 2: magicAnswer = "My uncle says it's deconfirmed." # Secret prediction. :)
        embed = discord.Embed(color=0xffff00)
        embed.add_field(name="Prediction", value=magicAnswer)
        await ctx.send(f"{ctx.author.mention}, the magical ball has spoken!", embed=embed)

def setup(bot): bot.add_cog(Games(bot))
