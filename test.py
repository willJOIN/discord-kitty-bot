import discord
from discord.ext import commands

loop = False
queue = []

async def loop(ctx):
    global loop
    if loop == True:
        await ctx.send("Loop OFF.")
        loop = False
    else:
        await ctx.send("Loop ON.")
        loop = True





current_song = 1
next_song = 2

# When play_count == 0
queue.append(current_song)
# When play_count > 1
queue.append(next_song)

# When current_song finishes, pop first one
voice_client.play(discord.FFmpegOpusAudio("current_song.webm"), after = queue.pop(0)) 
voice_client.play(discord.FFmpegOpusAudio("next_song.webm"), after = queue.pop(0)) 
