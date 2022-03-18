from nextcord.ext import commands

@commands.command(name="pause", description="Pausiert die Musikwiedergabe")
async def pauseMusic(ctx):
    voice = ctx.guild.voice_client
    if(voice.is_paused() != True):
        voice.pause()


def setup(bot):
    bot.add_command(pauseMusic)