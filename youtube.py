import youtube_dl
class Youtube(object):
    ydl_opts_search = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'quiet': True,
        'skip_download': True,
        'default_search': 'auto',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            }],
    }
    
    ydl_opts_download = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'quiet': True,
        'skip_download': False,
        'default_search': 'auto',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            }],
    }

    def __init__(self):
        self.item = None

    def search(self, keywords):
        # returns data about the first song/video in search
        with youtube_dl.YoutubeDL(self.ydl_opts_search) as ydl:
            meta = ydl.extract_info(f'ytsearch:{keywords}')
            return meta['entries'][0]
   
    def download(self, url):
        # downloads song with specified url, url can be obtained by search if not already known. 
        # its held in meta['webpage_url']
        with youtube_dl.YoutubeDL(self.ydl_opts_download) as ydl:
            meta = ydl.extract_info(url)


