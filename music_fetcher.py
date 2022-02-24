import asyncio
import youtube_dl
import discord


voulme = 0.5

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'default_search': 'auto',
        'audioformat': 'mp3',
        'noplaylist': True,
}

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=voulme):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, stream=True, loop=None):
        loop = loop or asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if ("entries" in info):
            # TODO Songqueue with skip method 
            return_val = info['entries'][0]['formats'][0]['url']
            title = info['entries'][0]['title']
        else:
            return_val = info.get('formats')[0].get('url')
            title = info['title']
        return [return_val, title]

