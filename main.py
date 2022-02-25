from Song import Song
import variables
import functions
import jsonHandler
import discord
from discord.ext import commands
import youtube_dl
import music_fetcher

PREFIX = "!"
DISCORD_TOKEN = "OTQ1Nzg1NDMyMDk5MTM1NTc5.YhVNUg.XiCBYubgrsXt41X9-ZqJ3f7Attc"


#                       #
#         INIT          #
#                       # 

print("Bot wird initialisiert...")
intents = discord.Intents().default()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=PREFIX,intents=intents)
currently_playing = None

audio = None

async def skipMusic(ctx, skip):
    voice = ctx.guild.voice_client
    for i in range(1, skip):
        variables.queue[ctx.guild.id].pop(0)
    if(voice == None):
        await joinVoiceChannel(ctx)
    #result = await music_fetcher.YTDLSource.from_url(variables.queue[ctx.guild.id][0].url, loop=bot.loop)
    global audio
    tmp_audio = discord.FFmpegPCMAudio(variables.queue[ctx.guild.id][0].url, executable="ffmpeg.exe")
    audio = discord.PCMVolumeTransformer(tmp_audio, volume=music_fetcher.voulme)
    voice.stop()
    voice.play(audio)
    await ctx.send('**{}** wird abgespielt. 🎶'.format(variables.queue[ctx.guild.id][0].title))
    global currently_playing
    currently_playing = variables.queue[ctx.guild.id].pop(0)

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
        print("Ist in keinem Voicechat")

@bot.command(name="volume", description="Ändere die Lautstärke des Bots für alle.")
async def changeVolume(ctx, volume):
    try:
        voice = ctx.guild.voice_client
        if(float(volume) >= 1):
            volume_=float(float(volume)/100)
        music_fetcher.voulme = volume_

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
        results = await music_fetcher.YTDLSource.from_url(url)
        for result in results:
            functions.addSongToQueue(ctx.guild, Song(result.title, result.url))
        if(voice.is_playing()):
            await ctx.send("**{}** Songs wurden der Warteschlange ⏳ hinzugefügt.".format(len(results)))
        else:
            await ctx.send("**{}** Songs wurde/n gefunden. 🔍".format(len(results)))
            #results = await music_fetcher.YTDLSource.from_url(variables.queue[ctx.guild.id][0].url, loop=bot.loop)
            global audio
            tmp_audio = discord.FFmpegPCMAudio(results[0].url, executable="ffmpeg.exe")
            global currently_playing
            currently_playing = variables.queue[ctx.guild.id].pop(0)
            audio = discord.PCMVolumeTransformer(tmp_audio, volume=music_fetcher.voulme)
            voice.play(audio)
            await ctx.send('**{}** wird abgespielt. 🎶'.format(currently_playing.title))

    except youtube_dl.DownloadError as err:
        await ctx.send("ERROR -> "+str(err.args))

@bot.command(name="queue")
async def getQueue(ctx):
    queue = variables.queue[ctx.guild.id]
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
    result = await music_fetcher.YTDLSource.from_url(daily_url)
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

bot.run(DISCORD_TOKEN)

        
