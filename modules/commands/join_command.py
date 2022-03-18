from nextcord.ext import commands

@commands.command(name="join", help="Let the bot join your voicechannel")
async def joinVoiceChannel(ctx):
    if not ctx.message.author.voice:
        await ctx.send("Der Bot konnte dem Sprachkanal nicht beitreten.")
        return
    else:
        voice = ctx.guild.voice_client
        if(voice == None):
            channel = ctx.message.author.voice.channel
            await channel.connect()

def setup(bot):
    bot.add_command(joinVoiceChannel)
