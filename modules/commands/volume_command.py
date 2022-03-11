from discord.ext import commands
import main

@commands.command(name="volume", description="Ändere die Lautstärke des Bots für alle.")
async def changeVolume(ctx, volume):
    try:
        voice = ctx.guild.voice_client
        if(float(volume) >= 1):
            volume_=float(float(volume)/100)
        #global audio 
        tmp_audio = main.getAudio()
        tmp_audio.volume = volume_
        main.setAudio(tmp_audio)
        volume = volume_
        if(voice.is_playing()):
            voice.pause()
            voice.play(main.getAudio())
        
    except:
        print("Error")


def setup(bot):
    bot.add_command(changeVolume)