import nextcord
from nextcord import Interaction
import youtube_dl
from modules.music import MusicFetcher
from modules.music.QueueMananger import QueueMananger
from modules.logger import logger
from objects import Song
from main import setAudio, getAudio, getCurrentlyPlaying, setCurrentlyPlaying, volume

async def joinVoiceChannel(voice_client, voice_channel):
    if(voice_client == None):
        await voice_channel.connect()

async def getSongs(args):
    url = ""
    try:
        for arg in args:
            url += arg
        results = await MusicFetcher.YTDLSource.from_url(url)
        return results

    except youtube_dl.DownloadError as err:
        logger.log(0, str(err.args))
        return []


async def playSong(interaction, args):
    
    voice = interaction.guild.voice_client
    guild_id = interaction.guild.id
    voice_channel = interaction.user.voice.channel
    channel = interaction.channel

    if(voice == None):
        await joinVoiceChannel(voice, voice_channel)

    try:
        results = await getSongs(args)

        for result in results:
            QueueMananger().addSongToQueue(guild_id, result)
        voice = interaction.guild.voice_client
        if(voice.is_playing()):
            if(len(results) > 1):
                await channel.send("Queued **{}** song/s. ⏳".format(len(results)))
            else:
                await channel.send("Queued **1** song. ⏳")
        else:
            if(len(results) > 1):
                await channel.send("Found **{}** songs. 🔍".format(len(results)))
            else:
                await channel.send("Found **1** song. 🔍")

            setCurrentlyPlaying(QueueMananger().removeSongFromQueue(guild_id))
            setAudio(nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(results[0].url, executable="ffmpeg", options='-vn', before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), volume=volume))
            voice.play(source=getAudio())
            await channel.send('**{}** wird abgespielt. 🎶'.format(getCurrentlyPlaying().title))
            logger.log(2, "Song wird abgespielt")

    except youtube_dl.DownloadError as err:
        print("ERROR -> "+str(err.args))