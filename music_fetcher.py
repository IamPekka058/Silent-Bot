import asyncio
import youtube_dl
import discord

from Song import Song


voulme = 0.5

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'default_search': 'auto',
        'audioformat': 'mp3',
        'noplaylist': False,
        #'continue_dl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', }]
}

FFMPEG_OPTIONS = {'before_options': '-reconnect 4 -reconnect_streamed 4 -reconnect_delay_max 5','options': '-vn'}

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
        if ('entries' in info):
            url_val = info['entries'][0]['formats'][0]['url']
            title = info['entries'][0]['title']
            for entrie in info['entries']:
                return_list.append(Song(entrie['title'], entrie['formats'][0]['url']))
        else:
            url_val = info.get('entries')[0].get('formats')[0].get('url')
            title = info.get('entries')[0]['title']
            return_list.append(Song(title, url_val))

        return return_list

