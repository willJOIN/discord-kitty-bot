import discord
from discord.ext import commands
import dotenv
import os
import youtube_dl

# Commands starts with "."
client = commands.Bot(command_prefix=".")

# Decorator to register function


@client.command()
# Asynchronous function that requires two arguments, ctx and url, also casts url to str
async def play(ctx, url: str):
    current_song_there = os.path.isfile("song_1.webm")
    next_song_there = os.path.isfile("song_2.webm")
    try:
        if current_song_there:
            os.remove("song_1.webm")
        elif next_song_there:
            os.remove("song_2.webm")
    except:
        return
    ydl_prefs = {
        # .webm
        "format": "249/250/251"
    }
    play_count = 0
    if play_count == 0:
        # Join author's voice channel
        voice_channel = ctx.author.voice.channel  # bug
        await voice_channel.connect()
        # Pick voice client
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        # Download file
        with youtube_dl.YoutubeDL(ydl_prefs) as ydl:
            ydl.download([url])
        # Store and rename file
        for i, file in enumerate(os.listdir("./")):
            if file.endswith(".webm"):
                os.rename(file, "./"+'song_' + str(i - 3).zfill(1)+".webm")
        # Convert and play file
        voice_client.play(discord.FFmpegOpusAudio("song_1.webm"))
        play_count = + 1
    elif play_count == 1:
        # Download file
        with youtube_dl.YoutubeDL(ydl_prefs) as ydl:
            ydl.download([url])
        # Store and rename file
        for i, file in enumerate(os.listdir("./")):
            if file.endswith(".webm"):
                os.rename(file, "./"+'song_' + str(i - 3).zfill(1)+".webm")
        # Convert and play file
        while voice_client.is_playing():
            return
        voice_client.play(discord.FFmpegOpusAudio("song_2.webm"))


@client.command()
async def pause(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send("I'm not playing any music.")


@client.command()
async def resume(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send("I'm not paused.")


@client.command()
async def stop(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_connected():
        voice_client.stop()
        await voice_client.disconnect()
    else:
        await ctx.send("I'm not on a voice channel.")

# Read bot login token in hidden .env file
dotenv.load_dotenv(dotenv.find_dotenv())
token = os.getenv("token")
client.run(token)
