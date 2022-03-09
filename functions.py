def hasRole(role, user):
    if(user.hasPermission()):
        return True
    else:
        return False

async def sendSyntaxErrorMessage(ctx, cmd, syntax):
    await ctx.send(cmd + " " + syntax)

