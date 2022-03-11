queue = {}

class QueueMananger():
    def addSongToQueue(guild, song):
        id = guild.id
        #Check if a queue exists for guild
        try: 
            songs = queue[id]
        
            #If queue exists for guild -> Add song
            songs.append(song)

        except KeyError as err:

            #Create queue for guild
            queue[id] = [song]

        list_items = []
        for item in queue[id]:
            list_items.append(item.title)
    
    def removeSongFromQueue(self, guild_id):
        return queue[guild_id].pop(0)

    def getQueue():
        return queue