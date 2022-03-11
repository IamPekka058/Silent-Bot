from discord.ext import commands
from modules.json import jsonHandler
from modules.commands.play_command import playSong
from modules.music import MusicFetcher

@commands.command("daily")
async def playDailySong(ctx):
    daily_url = jsonHandler.fetchDataFromJson()['daily_url']
    result = await MusicFetcher.YTDLSource.from_url(daily_url)
    await ctx.send("📅 Heutige Songempfehlung 🎶 -> **{}** <- 😀".format(result[0].getTitle()))
    await playSong(ctx, daily_url)


def setup(bot):
    bot.add_command(playDailySong)