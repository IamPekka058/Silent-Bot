from discord.ext import commands

@commands.command(name="stop", description="Stoppt Musikwiedergabe")
async def stopMusic(ctx):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.stop()
        await ctx.send("Wiedergabe gestoppt.")
    except:
        await ctx.send("Es wird keine Musik gespielt.")


def setup(bot):
    bot.add_command(stopMusic)