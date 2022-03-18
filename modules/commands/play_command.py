from nextcord.ext import commands
import nextcord
import youtube_dl
from modules.logger import logger
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
            await ctx.send("**{}** Song/s wurde/n gefunden. 🔍".format(len(results)))
            main.setCurrentlyPlaying(QueueMananger().removeSongFromQueue(ctx.guild.id))
            main.setAudio(nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(results[0].url, executable="ffmpeg", options='-vn', before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), volume=main.volume))
            voice.play(source=main.getAudio())
            await ctx.send('**{}** wird abgespielt. 🎶'.format(main.currently_playing.title))
            logger.log(2, "Song wird abgespielt")

    except youtube_dl.DownloadError as err:
        await ctx.send("ERROR -> "+str(err.args))


def setup(bot):
    bot.add_command(playSong)