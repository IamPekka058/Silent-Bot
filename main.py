from glob import glob
from click import echo
from modules.logger import logger
import multiprocessing
from tracemalloc import start
from objects.Song import Song
import functions
from modules.music.QueueMananger import QueueMananger
import modules.json.jsonHandler as jsonHandler
import discord
from discord.ext import commands
import youtube_dl
import resources.oauth as oauth
import modules
from modules.webservice import webservice

PREFIX = jsonHandler.fetchDataFromJson()['prefix']
DISCORD_TOKEN = jsonHandler.fetchDataFromJson()['token']

currently_playing = None
audio = None
volume = 0.05

intents = discord.Intents().default()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=PREFIX,intents=intents)

def setAudio(newAudio):
    global audio
    audio = newAudio

def getAudio():
    return audio

def getCurrentlyPlaying():
    return currently_playing

def setCurrentlyPlaying(playing):
    global currently_playing
    currently_playing = playing


@bot.event
async def on_message(message):
    try:
        logger.log(3, str(message.author)+" -> "+str(message.content))
        await bot.process_commands(message)
    except:
        print("Error")
#                       #
#    Load Extensions    #
#                       # 

bot.load_extension("modules.commands.join_command")
bot.load_extension("modules.commands.skip_command")
bot.load_extension("modules.commands.leave_command")
bot.load_extension("modules.commands.volume_command")
bot.load_extension("modules.commands.play_command")
bot.load_extension("modules.commands.queue_command")
bot.load_extension("modules.commands.pause_command")
bot.load_extension("modules.commands.stop_command")
bot.load_extension("modules.commands.exit_command")
bot.load_extension("modules.commands.daily_command")

def startBot():
    logger.log(2, "Bot wurde gestartet")
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    if(jsonHandler.fetchDataFromJson()['use_webservice'] == "True"):
        print("Webservice wird gestartet...")
        website_process = proc = multiprocessing.Process(target=webservice.runWebsite)
        website_process.start()

    bot_process = proc = multiprocessing.Process(target=startBot)
    bot_process.start()
    #bot.run(DISCORD_TOKEN)
    print("Bot gestartet...")
    print("Now listening to commands...")
    while(True):
        cmd = input("")
        if(cmd == "stop bot"):
            bot_process.terminate()
            print("Bot closed.")
        if(cmd == "exit"):
            print("Now exiting this process...")
            exit() 
        if(cmd == "start bot"):
            bot_process = proc = multiprocessing.Process(target=startBot)
            bot_process.start() 
            print("Bot started.")
