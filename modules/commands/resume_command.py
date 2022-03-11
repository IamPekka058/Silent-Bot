from discord.ext import commands

@commands.command(name="resume", description="Lässt die Musikwiedergabe wieder abspielen")
async def resumeMusic(ctx):
    voice = ctx.guild.voice_client
    if(voice.is_paused()):
        voice.resume()


def setup(bot):
    bot.add_command(resumeMusic)