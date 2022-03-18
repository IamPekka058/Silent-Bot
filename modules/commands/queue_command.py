from nextcord.ext import commands
from modules.music.QueueMananger import QueueMananger
import nextcord
import main

@commands.command(name="queue")
async def setQueue(ctx):
    queue = QueueMananger().getQueue()[ctx.guild.id]
    msg = ""
    for song in queue:
        msg += "\n\u200b\u200b\u200b"+song.title+"\n"
    cp = 0
    if(main.getCurrentlyPlaying() != None): cp = 1
    embed = nextcord.Embed(title="Warteschlange  ⏳  [{} Songs]".format(len(queue)+cp), description="▶ "+main.getCurrentylPlaying().title+" \n"+msg, color=0xa000a0)
    await ctx.send(embed = embed)


def setup(bot):
    bot.add_command(setQueue)