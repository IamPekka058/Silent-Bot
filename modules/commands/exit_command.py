from discord.ext import commands
from modules.commands.stop_command import stopMusic
from main import bot

@commands.command(name="exit")
async def stopBot(ctx):
    await ctx.send("Bot wird heruntergefahren.")
    await stopMusic(ctx)
    await bot.close()


def setup(bot):
    bot.add_command(stopBot)