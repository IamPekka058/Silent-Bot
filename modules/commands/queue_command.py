from discord.ext import commands
from modules.music.QueueMananger import QueueMananger
import discord
import main

@commands.command(name="queue")
async def setQueue(ctx):
    queue = QueueMananger().getQueue()[ctx.guild.id]
    msg = ""
    for song in queue:
        msg += "\n\u200b\u200b\u200b"+song.title+"\n"
    cp = 0
    if(main.getCurrentylPlaying() != None): cp = 1
    embed = discord.Embed(title="Warteschlange  ⏳  [{} Songs]".format(len(queue)+cp), description="▶ "+main.getCurrentylPlaying().title+" \n"+msg, color=0xa000a0)
    await ctx.send(embed = embed)


def setup(bot):
    bot.add_command(setQueue)