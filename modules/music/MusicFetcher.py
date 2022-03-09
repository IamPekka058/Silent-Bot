import asyncio
import youtube_dl
import discord
import json
from objects.Song import Song
import Converter


voulme = 0.5

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
        'format': 'bestaudio',
        'extractaudio': True,
        'default_search': 'auto',
        'audioformat': 'mp3',
        'noplaylist': False,
        'playlistend': 25,
        'verbose': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', }]
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)



class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=voulme):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, loop=None):
        loop = loop or asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        return_list = []
        if (Converter.isPlaylist(info)):
            for entrie in info['entries']:
                return_list.append(Song(entrie['title'], Converter.getUrl(entrie)))
            with open("temp_list.txt", "w") as file:
                file.write(json.dumps(info))
                file.flush()
                file.close()
        else:
            with open("temp.txt", "w") as file:
                file.write(json.dumps(info))
                file.flush()
                file.close()
            url_val = info['formats'][0]['url']
            title = info['title']
            return_list.append(Song(title, url_val))
            print("Song hinzugefügt")

        return return_list

