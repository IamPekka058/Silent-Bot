import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from modules.json import jsonHandler
from modules.music import MusicFetcher
from modules.functions import Music_Functions

class Music(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="daily", description="Plays the recommended song for today.")
    async def playDailySong(self, interaction: Interaction):
        #Fetch url
        daily_url = jsonHandler.fetchDataFromJson()['daily_url']
        #Fetch audio
        result = await MusicFetcher.YTDLSource.from_url(daily_url)
        await interaction.response.send_message("📅 Todays song recommendation 🎶 -> **{}** <- 😀".format(result[0].getTitle()))
        await Music_Functions.playSong(interaction, daily_url)

def setup(bot):
    bot.add_cog(Music(bot))