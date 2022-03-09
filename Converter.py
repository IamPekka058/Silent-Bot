from tkinter import E


def isPlaylist(dict):
    try:
        if(dict['_type'] == 'playlist'): return True
    except:
        return False

def getPlayListSize(dict):
    try:
        return dict['entries'].size
    except:
        return 1

def getUrl(dict):
    if(isPlaylist(dict)):
        if(getPlayListSize(dict) > 1):
            return dict['entries'].pop()
    else:    
        return dict['formats'][0]['url']