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
from modules.webservice import webservice

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

def getCurrentylPlaying():
    return currently_playing

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

if __name__ == '__main__':
    if(jsonHandler.fetchDataFromJson()['use_webservice'] == "True"):
        print("Webservice wird gestartet...")
        website_thread = threading.Thread(target=webservice.runWebsite)
        website_thread.start()

    bot.run(DISCORD_TOKEN)
        
