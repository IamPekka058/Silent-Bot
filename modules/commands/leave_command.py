from discord.ext import commands

@commands.command(name="leave", help="Der Bot verlässt den Sprachkanal")
async def leaveVoiceChannel(ctx):
    voice_client = ctx.guild.voice_client
    if(voice_client != None):
        server = ctx.message.guild
        voice_channel = server.voice_client
        await voice_channel.disconnect()
    else:
        print("Der Bot ist in keinem Sprachkanal")


def setup(bot):
    bot.add_command(leaveVoiceChannel)