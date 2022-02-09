import re
import urllib.request
import os
import pytube
import string

class YT:

    def search(this, keyword:str):
        clean_keyword = this.clean_keyword(keyword)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + clean_keyword)
        videoIds = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        return("https://www.youtube.com/watch?v=" + videoIds[0]), videoIds[0]

    def download_from_url(this, url:str, video_id:str):
        try:
            yt = pytube.YouTube(url = url)
            out_file = None
            try:
                out_file = yt.streams.get_audio_only().download(output_path = 'downloads/')
            except:
                print(f"no audio only source for {yt.title}")

            if out_file == None:
                out_file = yt.streams.get_lowest_resolution.download(filename = video_id, output_path = 'downloads/')

            new_file = f"downloads/{video_id}.mp3"
            os.rename(out_file, new_file)
            print(f"Sucessfully downloaded {yt.title}")
        except BaseException as e:
           print(f"Unable to download video {url}\n {e}")

    def clean_keyword(this, keyword:str):
        return keyword.rstrip().replace(" ", "+")

    def download_from_keyword(this, keyword:str):
        link, video_id = this.search(keyword)
        yt = pytube.YouTube(link)
        if this.file_exists(video_id):
            print(f"File exists for {yt.title}")
        else:
            this.download_from_url(link, video_id)
        
        return yt.title, link, video_id

    def file_exists(this, video_id):
        return os.path.exists(f"downloads/{video_id}.mp3")



if __name__ == '__main__':
    yt = YT()
    title, url = yt.download_from_keyword("victor wooten")
    print(f"title {title} url {url}")

