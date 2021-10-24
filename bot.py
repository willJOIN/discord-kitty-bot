import discord
from discord.ext import commands
import dotenv
import os
import youtube_dl

# Commands starts with "."
client = commands.Bot(command_prefix=".")
play_count = 0
queue = []


@client.command()
# Asynchronous function that requires two arguments, ctx and url, also casts url to str
async def play(ctx, url: str):
    global play_count
    global queue
    ydl_prefs = {
        # .webm
        "format": "249/250/251"
    }
   
    if play_count == 0:
        # Join author's voice channel
        voice_channel = ctx.author.voice.channel
        if not voice_client.is_connected():
            await voice_channel.connect()
        # Pick voice client
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        current_song_there = os.path.isfile("current_song.webm")
        try:
            if current_song_there:
                os.remove("current_song.webm")
        except:
            return
        # Download file
        with youtube_dl.YoutubeDL(ydl_prefs) as ydl:
            ydl.download([url])
        # Store and rename file
        for file in os.listdir("./"):
            if file.endswith(".webm"):
                os.rename(file, "current_song.webm")
        # Convert and play file
        current_song = voice_client.play(discord.FFmpegOpusAudio("current_song.webm"))
        queue.append(current_song)
        play_count += 1
    else:
         # Pick voice client
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        next_song_there = os.path.isfile("next_song.webm")
        try:
            if next_song_there:
                os.remove("next_song.webm")
        except:
            return
        with youtube_dl.YoutubeDL(ydl_prefs) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".webm"):
                if file.startswith("current_song"):
                    return
            os.rename(file, "next_song.webm")
        if not voice_client.is_playing():
            next_song = voice_client.play((discord.FFmpegOpusAudio(
                "next_song.webm")), after=queue.pop(0))
            queue.append(next_song)
            play_count += 1


@client.command()
async def loop(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await ctx.send("Looping current music.")
    if not voice_client.is_playing():
        voice_client.play(discord.FFmpegOpusAudio("current_song.webm"))


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
