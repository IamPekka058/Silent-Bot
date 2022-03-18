from nextcord.ext import commands
import functions
from main import PREFIX

@commands.command("clear")
async def clearChat(ctx, amount = None):
    try:
        print(amount)
        if(amount == None): raise Exception()
        num = int(amount)
    except:
        await functions.sendSyntaxErrorMessage(ctx, PREFIX+"clear", "<amount>")
        return

    await ctx.channel.purge(limit=num)  


def setup(bot):
    bot.add_command(clearChat)