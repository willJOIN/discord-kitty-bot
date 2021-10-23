import os
from tkinter import Tcl

file_list = os.listdir("./")

sort = Tcl().call('lsort', '-dict', file_list)

print(sort)

# Convert and play files in ascending order
for i, file in enumerate(os.listdir("./")):
    if file.endswith(".webm"):
        queue = Tcl().call('lsort', '-dict', os.listdir("./"))
        voice_client.play(discord.FFmpegOpusAudio("queue[i]"))
