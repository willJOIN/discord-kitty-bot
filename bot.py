import discord
from discord.ext import commands
import dotenv
import os
import youtube_dl

# Commands starts with "."
client = commands.Bot(command_prefix=".")
play_count = 0


@client.command()
# Asynchronous function that requires two arguments, ctx and url, also casts url to str
async def play(ctx, url: str):
    global play_count
    ydl_prefs = {
        # .webm
        "format": "249/250/251"
    }
    if play_count == 0:
        # Join author's voice channel
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
        # Pick voice client
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        # Download file
        try:
            await ctx.send("Downloading meowsic, ~meow")
            voice_client.play(discord.FFmpegOpusAudio("/assets/sound1.mp3"))
            with youtube_dl.YoutubeDL(ydl_prefs) as ydl:
                ydl.download([url])
        except:
            await ctx.send("Unexpected error when trying to download. Please try again, ~meow")
            voice_client.play(discord.FFmpegOpusAudio("assets\sound2.mp3"))
            return
        # Store and rename file
        try:
            os.remove("current_song.webm")
            os.remove("next_song.webm")
        except:
            pass
        for file in os.listdir("./"):
            if file.endswith(".webm"):
                os.rename(file, "current_song.webm")
        # Convert and play file
        voice_client.play(discord.FFmpegOpusAudio("current_song.webm"))
        await ctx.send("Playing meowsic, ~meow")
        play_count += 1
    else:
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice_client.is_playing():
            await ctx.send("Wait for me to finish the current meowsic, ~meow")
        else:
            try:
                await ctx.send("Downloading meowusic, ~meow")
                voice_client.play(discord.FFmpegOpusAudio("assets\sound2.mp3"))
                with youtube_dl.YoutubeDL(ydl_prefs) as ydl:
                    ydl.download([url])
            except:
                await ctx.send("Unexpected error when trying to download... maybe try again?")
                voice_client.play(discord.FFmpegOpusAudio("assets\sound3.mp3"))
                return
            try:
                os.remove("next_song.webm")
            except:
                pass
            for file in os.listdir("./"):
                if file.endswith(".webm") and not file.startswith("current_song"):
                    os.rename(file, "next_song.webm")
            await ctx.send("Playing meowsic, ~meow")
            voice_client.play(discord.FFmpegOpusAudio("next_song.webm"))
            play_count += 1


@client.command()
async def loop(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if play_count == 0:
        await ctx.send("I haven't played any meowsic, ~meow")
    if not voice_client.is_playing():
        await ctx.send("Looping current meowsic, ~meow")
        if play_count == 1:
            voice_client.play(discord.FFmpegOpusAudio("current_song.webm"))
        elif play_count >= 2:
            voice_client.play(discord.FFmpegOpusAudio("next_song.webm"))
    else:
        await ctx.send("Please wait for the meowsic to end before asking me to loop it, ~meow")


@client.command()
async def pause(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice_client.is_playing():
            await ctx.send("Meowsic is paused, ~meow")
            voice_client.pause()
    except:
        await ctx.send("I'm not playing any meowsic, ~meow")


@client.command()
async def resume(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice_client.is_paused():
            await ctx.send("Resuming meowsic playback, ~meow")
            voice_client.resume()
    except:
        await ctx.send("I'm not paused, ~meow")


@client.command()
async def stop(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice_client.is_connected():
            await ctx.send("Bye bye! ~meow")
            voice_client.stop()
            await voice_client.disconnect()
    except:
        await ctx.send("I'm not on a voice channel.")


# Read bot login token in hidden .env file
dotenv.load_dotenv(dotenv.find_dotenv())
token = os.getenv("token")
client.run(token)
