from discord.ext import commands
import discord
import youtube_dl
from modules.commands.join_command import joinVoiceChannel
from modules.music import MusicFetcher
from modules.music.QueueMananger import QueueMananger
from objects.Song import Song
import main

@commands.command(name="play", desciption="Spiele Musik von YouTube")
async def playSong(ctx, *args):
    voice = ctx.guild.voice_client
    if(voice == None):
        await joinVoiceChannel(ctx)

    try:
        #Add parameters to search string for youtube
        url = ""
        for arg in args:
            url += arg+" "

        voice = ctx.guild.voice_client
        results = await MusicFetcher.YTDLSource.from_url(url)
        for result in results:
            QueueMananger.addSongToQueue(ctx.guild, Song(result.title, result.url))
        if(voice.is_playing()):
            await ctx.send("**{}** Song/s wurde/n der Warteschlange ⏳ hinzugefügt.".format(len(results)))
        else:
            await ctx.send("**{}** Songs wurde/n gefunden. 🔍".format(len(results)))
            #results = await music_fetcher.YTDLSource.from_url(variables.queue[ctx.guild.id][0].url, loop=bot.loop)
            #global audio
            #global currently_playing
            id = ctx.guild.id
            main.currently_playing = QueueMananger().removeSongFromQueue(id)
            main.setAudio(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(results[0].url, executable="ffmpeg", options='-vn',), volume=main.volume))
            voice.play(source=main.getAudio())
            await ctx.send('**{}** wird abgespielt. 🎶'.format(main.currently_playing.title))

    except youtube_dl.DownloadError as err:
        await ctx.send("ERROR -> "+str(err.args))


def setup(bot):
    bot.add_command(playSong)