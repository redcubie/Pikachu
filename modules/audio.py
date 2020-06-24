import discord, asyncio, os, shutil, youtube_dl, importlib
from discord.ext import commands; from discord.utils import get
 
queues = {}

class Audio(commands.Cog):
    def __init__(self, bot): self.bot = bot
 
    @commands.command()
    async def join(self, ctx): # p!join
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        channelcheck = self.bot.get_channel(channel.id)
        audiochannel = self.bot.get_channel(469988877180993546) # Channel #Bot Commands.
        modchannel = self.bot.get_channel(482916026674053120) # Channel #Moderator Chat.
        if channelcheck == audiochannel or channelcheck == modchannel:
            if voice != None: return await voice.move_to(channel)
            await channel.connect()
        else: await ctx.send(f"{ctx.author.mention}, please join {audiochannel} to use this command.")
 
    @commands.command()
    @commands.has_guild_permissions(move_members=True)
    async def leave(self, ctx): # p!leave
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            queues.clear()
            queue_infile = os.path.isdir("./queue")
            if queue_infile is True: shutil.rmtree("./queue")
            song_there = os.path.isfile("song.mp3")
            if song_there: os.remove("song.mp3")
            await ctx.send(f"{ctx.author.mention}, sucessfully left {channel}.")
    
    @commands.command()
    async def play(self, ctx, *url: str): # p!play
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            def check_queue():
                song_there = os.path.isfile("song.mp3")
                if song_there: os.remove("song.mp3")
                Queue_infile = os.path.isdir("./queue")
                if Queue_infile is True:
                    filedir = os.path.abspath(os.path.realpath("queue"))
                    length = len(os.listdir(filedir))
                    still_q = length - 1
                    try: first_file = os.listdir(filedir)[0]
                    except:
                        print("No more queued songs.")
                        queues.clear()
                        return
                    main_location = os.path.dirname(os.path.realpath("modules"))
                    song_path = os.path.abspath(os.path.realpath("queue") + "\\" + first_file)
                    if length != 0:
                        print("Song done, playing next queued.")
                        print(f"Queue: {still_q}")
                        song_there = os.path.isfile("song.mp3")
                        if song_there: os.remove("song.mp3")
                        shutil.move(song_path, main_location)
                        for file in os.listdir("./"):
                            if file.endswith(".mp3"): os.rename(file, "song.mp3")
                        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                        voice.source = discord.PCMVolumeTransformer(voice.source)
                        voice.source.volume = 1.00
                    else:
                        queues.clear()
                        return
                else:
                    queues.clear()
                    print("No audio was queued before the ending of the last song.")
            song_there = os.path.isfile("song.mp3")
            if song_there:
                await ctx.send(f"{ctx.author.mention}, please wait until the current audio is over before requesting new audio.")
                return
            Queue_infile = os.path.isdir("./queue")
            try:
                queue_folder = "./queue"
                if Queue_infile is True:
                    print("Remove old queue folder.")
                    shutil.rmtree(queue_folder)
            except: print("No old queue folder.")
            await ctx.channel.send(f"{ctx.author.mention}, your audio will be played shortly.")
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            ydl_opts = {
                "format": "bestaudio/best",
                "noplaylist": True,
                "nocheckcertificate": True,
                "ignoreerrors": False,
                "logtostderr": False,
                "source_address": "0.0.0.0",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }
            song_search = " ".join(url)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now...")
                ydl.download([f"ytsearch1:{song_search}"])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
                    print(f"Renamed File: {file}\n")
            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 1.00
        else:
            await ctx.send(f"{ctx.author.mention}, please use `p!join` before using this command.")
 
    @commands.command()
    @commands.has_guild_permissions(move_members=True)
    async def pause(self, ctx): # p!pause
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print("Audio paused.")
            voice.pause()
        else:
            print("Audio not playing, failed pause.")
            await ctx.send(f"{ctx.author.mention}, there is no audio playing.")
 
    @commands.command()
    @commands.has_guild_permissions(move_members=True)
    async def resume(self, ctx): # p!resume
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            print("Resumed audio.")
            voice.resume()
            await ctx.send("Resumed audio.")
        else:
            print("Audio is not paused.")
            await ctx.send(f"{ctx.author.mention}, the audio is not paused.")

    @commands.command()
    @commands.has_guild_permissions(move_members=True)
    async def stop(self, ctx): # p!stop
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        queues.clear()
        queue_infile = os.path.isdir("./queue")
        if queue_infile is True:
            shutil.rmtree("./queue")
        if voice and voice.is_playing():
            print("Audio stopped.")
            voice.stop()
            await ctx.send(f"{ctx.author.mention}, the audio has been stopped.")
            song_there = os.path.isfile("song.mp3")
            if song_there:
                os.remove("song.mp3")
        else:
            print("No audio playing, failed to stop.")
            await ctx.send(f"{ctx.author.mention}, there is no audio playing.")

    @commands.command()
    async def volume(self, ctx, volume: int): # p!volume
        channel = ctx.author.voice.channel
        membercheck = channel.members
        membercount = len(membercheck)
        if membercount == 2 or ctx.author.guild_permissions.move_members==True:
            if ctx.voice_client is None: return await ctx.send(f"{ctx.author.mention}, not connected to a voice channel.")
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"{ctx.author.mention}, changed the volume to {volume}%.")
        else:
            await ctx.send(f"{ctx.author.mention}, you are not alone in the voice channel.")

    @pause.error
    async def pause_error(self, ctx, error): # p!pause error handlers.
        if isinstance(error, commands.CheckFailure):
            channel = ctx.author.voice.channel
            membercheck = channel.members
            membercount = len(membercheck)
            if membercount <= 2:
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                if voice and voice.is_paused():
                    print("Resumed audio.")
                    voice.resume()
                    await ctx.send("Resumed audio.")
                else:
                    print("Audio is not paused.")
                    await ctx.send(f"{ctx.author.mention}, the audio is not paused.")
            else: await ctx.send(f"{ctx.author.mention}, you are not alone in the voice channel.")
                    
    @resume.error
    async def resume_error(self, ctx, error): # p!resume error handlers.
        if isinstance(error, commands.CheckFailure):
            channel = ctx.author.voice.channel
            membercheck = channel.members
            membercount = len(membercheck)
            if membercount <= 2:
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                if voice and voice.is_playing():
                    print("Audio paused.")
                    voice.pause()
                else:
                    print("Audio not playing, failed pause.")
                    await ctx.send(f"{ctx.author.mention}, there is no audio playing.")
            else: await ctx.send(f"{ctx.author.mention}, you are not alone in the voice channel.")

    @stop.error
    async def stop_error(self, ctx, error): # p!stop error handlers.
        if isinstance(error, commands.CheckFailure):
            channel = ctx.author.voice.channel
            membercheck = channel.members
            membercount = len(membercheck)
            if membercount <= 2:
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                queues.clear()
                queue_infile = os.path.isdir("./queue")
                if queue_infile is True:
                    shutil.rmtree("./queue")
                if voice and voice.is_playing():
                    print("Audio stopped.")
                    voice.stop()
                    await ctx.send(f"{ctx.author.mention}, the audio has been stopped.")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                else:
                    print("No audio playing, failed to stop.")
                    await ctx.send(f"{ctx.author.mention}, there is no audio playing.")
            else: await ctx.send(f"{ctx.author.mention}, you are not alone in the voice channel.")

def setup(bot): bot.add_cog(Audio(bot))
