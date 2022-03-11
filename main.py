import threading
from objects.Song import Song
import functions
from modules.music.QueueMananger import QueueMananger
import modules.json.jsonHandler as jsonHandler
import discord
from discord.ext import commands
import youtube_dl
import resources.oauth as oauth
import modules

PREFIX = jsonHandler.fetchDataFromJson()['prefix']
DISCORD_TOKEN = jsonHandler.fetchDataFromJson()['token']

currently_playing = None
audio = None
volume = 0.5

intents = discord.Intents().default()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=PREFIX,intents=intents)

def setAudio(newAudio):
    global audio
    audio = newAudio
def getAudio():
    return audio

#                       #
#    Load Extensions    #
#                       # 

bot.load_extension("modules.commands.join_command")
bot.load_extension("modules.commands.skip_command")
bot.load_extension("modules.commands.leave_command")
bot.load_extension("modules.commands.volume_command")
bot.load_extension("modules.commands.play_command")

#                       #
#         INIT          #
#                       # 
def startBot():
    print("Bot startet...")
    global bot
    bot = commands.Bot(command_prefix=PREFIX,intents=intents)
    bot.run(DISCORD_TOKEN)

#                       #
#       COMMANDS        #
#                       # 

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
    await ctx.send("📅 Heutige Songempfehlung 🎶 -> **{}** <- 😀".format(result[0].getTitle()))
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
    website_thread = threading.Thread(target=modules.webservice.runWebsite)
    website_thread.start()

bot.run(DISCORD_TOKEN)
        
