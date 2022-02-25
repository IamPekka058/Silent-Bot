import variables

def addSongToQueue(guild, song):
    id = guild.id
    #Check if a queue exists for guild
    try: 
        songs = variables.queue[id]
        
        #If queue exists for guild -> Add song
        songs.append(song)

    except KeyError as err:

        #Create queue for guild
        variables.queue[id] = [song]

    list_items = []
    for item in variables.queue[id]:
        list_items.append(item.title)
    print("[QUEUE] " + str(id)+" -> " + str(list_items))

def hasRole(role, user):
    if(user.hasPermission()):
        return True
    else:
        return False

async def sendSyntaxErrorMessage(ctx, cmd, syntax):
    await ctx.send(cmd + " " + syntax)

