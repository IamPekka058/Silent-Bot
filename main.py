import threading
from objects.Song import Song
import functions
from modules.music.QueueMananger import QueueMananger
import jsonHandler
import discord
from discord.ext import commands
import youtube_dl
import modules.music.MusicFetcher as MusicFetcher
import resources.oauth as oauth
from modules.webservice import webservice

PREFIX = jsonHandler.fetchDataFromJson()['prefix']
DISCORD_TOKEN = jsonHandler.fetchDataFromJson()['token']

currently_playing = None

audio = None

intents = discord.Intents().default()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=PREFIX,intents=intents)

#                       #
#         INIT          #
#                       # 
def startBot():
    print("Bot startet...")
    global bot
    bot = commands.Bot(command_prefix=PREFIX,intents=intents)
    bot.run(DISCORD_TOKEN)

async def skipMusic(ctx, skip):
    voice = ctx.guild.voice_client
    for i in range(1, skip):
        QueueMananger().removeSongFromQueue(ctx.guild.id)
    if(voice == None):
        await joinVoiceChannel(ctx)
    #result = await music_fetcher.YTDLSource.from_url(variables.queue[ctx.guild.id][0].url, loop=bot.loop)
    global audio
    tmp_audio = discord.FFmpegPCMAudio(QueueMananger().getQueue()[ctx.guild.id][0].url, executable="resources/ffmpeg.exe")
    audio = discord.PCMVolumeTransformer(tmp_audio, volume=MusicFetcher.voulme)
    voice.stop()
    voice.play(audio)
    await ctx.send('**{}** wird abgespielt. 🎶'.format(QueueMananger().getQueue()[ctx.guild.id][0].title))
    global currently_playing
    currently_playing = QueueMananger.removeSongFromQueue(ctx.guild.id)

#                       #
#       COMMANDS        #
#                       # 

@bot.command(name="join", help="Let the bot join your voicechannel")
async def joinVoiceChannel(ctx):
    if not ctx.message.author.voice:
        await ctx.send("Der Bot konnte dem Sprachkanal nicht beitreten.")
        return
    else:
        voice = ctx.guild.voice_client
        if(voice == None):
            channel = ctx.message.author.voice.channel
            await channel.connect()

@bot.command(name="leave", help="Der Bot verlässt den Sprachkanal")
async def leaveVoiceChannel(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if(voice_client != None):
        server = ctx.message.guild
        voice_channel = server.voice_client
        await voice_channel.disconnect()
    else:
        print("Der Bot ist in keinem Sprachkanal")

@bot.command(name="volume", description="Ändere die Lautstärke des Bots für alle.")
async def changeVolume(ctx, volume):
    try:
        voice = ctx.guild.voice_client
        if(float(volume) >= 1):
            volume_=float(float(volume)/100)
        MusicFetcher.voulme = volume_

        audio.volume = volume_
        if(voice.is_playing()):
            voice.pause()
            voice.play(audio)
        
    except:
        print("Error")

@bot.command(name="play", desciption="Spiele Musik von YouTube")
async def playMusic(ctx, *args):
    voice = ctx.guild.voice_client
    if(voice == None):
        await joinVoiceChannel(ctx)
    try:
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
            global audio
            tmp_audio = discord.FFmpegPCMAudio(results[0].url, executable="ffmpeg.exe", options='-vn',)# before_options='-reconnect 4 -reconnect_streamed 4 -reconnect_delay_max 5')
            global currently_playing
            currently_playing = QueueMananger().getQueue()[ctx.guild.id].pop(0)
            audio = discord.PCMVolumeTransformer(tmp_audio, volume=MusicFetcher.voulme)
            voice.play(audio)
            await ctx.send('**{}** wird abgespielt. 🎶'.format(currently_playing.title))

    except youtube_dl.DownloadError as err:
        await ctx.send("ERROR -> "+str(err.args))

@bot.command(name="queue")
async def getQueue(ctx):
    queue = QueueMananger().getQueue()[ctx.guild.id]
    msg = ""
    for song in queue:
        msg += "\n\u200b\u200b\u200b"+song.title+"\n"
    cp = 0
    if(currently_playing != None): cp = 1
    embed = discord.Embed(title="Warteschlange  ⏳  [{} Songs]".format(len(queue)+cp), description="▶ "+currently_playing.title+" \n"+msg, color=0xa000a0)
    await ctx.send(embed = embed)

@bot.command(name="skip")
async def skip(ctx, amount=1):
    try:
        amount = int(amount)
    except:
        functions.sendSyntaxErrorMessage(ctx, PREFIX+"skip", "<amount>")
        return
    await skipMusic(ctx, amount)

# TODO clear command

@bot.command(name="pause", description="Pausiert die Musikwiedergabe")
async def pauseMusic(ctx):
    voice = ctx.guild.voice_client
    if(voice.is_paused() != True):
        voice.pause()

@bot.command(name="resume", description="Lässt die Musikwiedergabe wieder abspielen")
async def resumeMusic(ctx):
    voice = ctx.guild.voice_client
    if(voice.is_paused()):
        voice.resume()

@bot.command(name="stop", description="Stoppt Musikwiedergabe")
async def stopMusic(ctx):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.stop()
        await ctx.send("Wiedergabe gestoppt.")
    except:
        await ctx.send("Es wird keine Musik gespielt.")

@bot.command(name="exit")
async def stopBot(ctx):
    await ctx.send("Bot wird heruntergefahren.")
    await stopMusic(ctx)
    await bot.close()

@bot.command("daily")
async def daily(ctx):
    daily_url = jsonHandler.fetchDataFromJson()['daily_url']
    result = await MusicFetcher.YTDLSource.from_url(daily_url)
    await ctx.send("📅 Heutige Songempfehlung 🎶 -> **{}** <- 😀".format(result[1]))
    await playMusic(ctx, daily_url)

@bot.command("clear")
async def clear(ctx, amount = None):
    try:
        print(amount)
        if(amount == None): raise Exception()
        num = int(amount)
    except:
        await functions.sendSyntaxErrorMessage(ctx, PREFIX+"clear", "<amount>")
        return

    await ctx.channel.purge(limit=num)      
    

print("Discord Bot wird gestartet...")

if(jsonHandler.fetchDataFromJson()['use_webservice'] == "True"):

    print("Webservice wird gestartet...")
    website_thread = threading.Thread(target=webservice.runWebsite)
    website_thread.start()

bot.run(DISCORD_TOKEN)
        
