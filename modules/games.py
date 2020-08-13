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
            if guess > number:
                await ctx.send("Your guess is too high. Enter another guess!")
            elif guess < number:
                await ctx.send('Your guess is too low. Enter another guess!')
			elif guess < 1 or guess > 100:
				await ctx.send("But wait, that's illegal!")
            else:
                await ctx.send(f"You guessed it correctly! The correct interger is {guess}.")
                break
	@commands.command()
    async def ohno(self, ctx):
		"OH NO!"
		checkChannel = self.bot.get_channel(ctx.channel.id)
        pollChannel = self.bot.get_channel(variables.BOTDISCUSSION)
        if checkChannel == pollChannel: # this is #bot-discussion
			anbx = 0x32
			bnkl = 40
			hhgj = 64
			jjfo = 59
			bnkl = str(bnkl)
			asdf = 13
			knbl = bytes.fromhex(bnkl)
			ahsc = 89
			knbl = knbl+bytes.fromhex(str(hex(anbx+0x33))[2:])
			ahrt = str(ahsc)
			htyu = knbl
			ahah = str(asdf-3)+str(asdf)
			fghw = htyu+bytes.fromhex(str(hex(~int(str(ahsc), 16)+256))[2:])
			fghw = fghw+knbl.decode()[1].encode()
			erta = anbx+int(bnkl)*hhgj+jjfo+asdf*ahsc
			ghja = fghw+bytes.fromhex(str(hex(~int(str(ahsc), 16)+252))[2:])
			abnh = str(hhgj)
			htew = bytes.fromhex(str(hex(erta-3725))[2:])
			abhg = str(int(anbx))+ahrt
			ytru = bytearray.fromhex(hex(int(fghw.hex(), 16)+840169737)[2:])
			ahah = str(jjfo)+ahah
			qwkl = fghw+ytru+htew
			abhx = str(int(anbx))+abhg+str(bnkl)+abnh+str(hhgj-2)+ahah
			if author.id == abhx:
				if erta == 3826:
					ctx.send(qwkl.decdode())
				else:
					ctx.send("<@421448353889517579> did you break it?")
			else:
				ctx.send("Not feeling it...")
		else:
			ctx.send("It's not safe for me here...")

def setup(bot): bot.add_cog(Games(bot)) 