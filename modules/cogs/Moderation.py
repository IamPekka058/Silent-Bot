from nextcord.ext import commands
from nextcord import Interaction
import nextcord

class Moderation(commands.Cog):
    def __init(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="clear", guild_ids=[946172925285916673])
    async def clearChat(self, interaction: Interaction, amount):
        try:
            num = int(amount)
            result = await interaction.channel.purge(limit=num)
            
        except:
            result = await interaction.channel.purge(limit=1)
        
        length = len(result)
        if(length > 1):
            await interaction.response.send_message(str(len(result))+" Nachrichten wurden gelöscht.")
        else:
            await interaction.response.send_message("1 Nachricht wurde gelöscht.")
            
def setup(bot):
    bot.add_cog(Moderation(bot))
