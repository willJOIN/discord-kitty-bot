import discord
from discord.ext import commands
import dotenv
import youtube_dl
import os

# Commands starts with "."
client = commands.Bot(command_prefix=".")

# Decorator to register function
@client.command()
# Asynchronous function that requires two arguments, ctx and url, also casts url to str
async def play(ctx, url: str):
    music_there = os.path.isfile("music.webm")
    try:
        if music_there:
            os.remove("music.webm")
    # Stop when playing music 
    except PermissionError:
        await ctx.send("Wait for the current music to end or use the 'stop' command.")
        return

    # Join author's voice channel
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()
    # Pick voice client
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_prefs = {
        # .webm
        "format": "249/250/251"
    }

    # Download file
    with youtube_dl.YoutubeDL(ydl_prefs) as ydl:
        ydl.download([url])
    # Store and rename file
    for file in os.listdir("./"):
        if file.endswith(".webm"):
            os.rename(file, "music.webm")
    # Convert and play file
    voice_client.play(discord.FFmpegOpusAudio("music.webm"))

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
