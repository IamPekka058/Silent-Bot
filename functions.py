from discord import Interaction



async def sendSyntaxErrorMessage(ctx, cmd, syntax):
    await ctx.send(cmd + " " + syntax)

