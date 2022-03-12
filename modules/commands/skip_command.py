from discord.ext import commands
import discord
from main import PREFIX, audio, getAudio, setCurrentlyPlaying
import functions
from modules.music import MusicFetcher
from modules.music.QueueMananger import QueueMananger

@commands.command(name="skip")
async def skipSong(ctx, amount=1):
    try:
        amount = int(amount)
    except:
        functions.sendSyntaxErrorMessage(ctx, PREFIX+"skip", "<amount>")
        return

    voice = ctx.guild.voice_client
    for i in range(1, amount):
        QueueMananger().removeSongFromQueue(ctx.guild.id)

    if(voice == None):
        ctx.send("You are not in a voice channel")
        return

    #global audio
    audio = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(QueueMananger().getQueue()[ctx.guild.id][0].url, executable="ffmpeg"), volume=getAudio().volume)
    voice.stop()
    voice.play(audio)
    await ctx.send('**{}** wird abgespielt. 🎶'.format(QueueMananger().getQueue()[ctx.guild.id][0].title))
    
    setCurrentlyPlaying(QueueMananger().removeSongFromQueue(ctx.guild.id))

def setup(bot):
    bot.add_command(skipSong)
