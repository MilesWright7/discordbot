import re
import urllib.request
import os
import pytube
import re

class YT:

    watch_re = re.compile('watch\\?v=')
    playlist_re = re.compile('list=')
    index_re = re.compile('index=')

    def search(this, keyword:str):
        clean_keyword = this.clean_keyword(keyword)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + clean_keyword)
        videoIds = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        return "https://www.youtube.com/watch?v=" + videoIds[0]

    def download_from_url(this, url:str, ):
        try:
            yt = pytube.YouTube(url)
            out_file = None
            try:
                out_file = yt.streams.get_audio_only().download(output_path = 'downloads/')
            except:
                print(f"no audio only source for {yt.title}")

            if out_file == None:
                out_file = yt.streams.get_lowest_resolution.download(filename = url[-8:], output_path = 'downloads/')

            new_file = f"downloads/{url[-8:]}.mp3"
            os.rename(out_file, new_file)
            print(f"Sucessfully downloaded {yt.title}")
        except BaseException as e:
           print(f"Unable to download video {url}\n {e}")

    def clean_keyword(this, keyword:str):
        return keyword.rstrip().replace(" ", "+")

    def download_from_keyword(this, keyword:str):
        link = this.search(keyword)
        this.download_from_url(link)

    def file_exists(this, link):
        return os.path.exists(f"downloads/{link[-8:]}.mp3")
    
    

    def find_video(this, input:str):
        is_link = False
        is_playlist = False
        idx = 1


        playlist_search = this.playlist_re.search(input)
        if playlist_search:
            is_playlist = True
            index_search = this.index_re.search(input)
            if index_search:
                idx = int(input[index_search.span()[1]:])

        watch_search = this.watch_re.search(input)
        if watch_search:
            is_link = True

        if is_playlist:
            try:
                pl = pytube.Playlist(input)
                if pl:
                    return pl, idx

            except:
                pass
        if is_link:
            try:
                vid = pytube.YouTube(input)
                return vid, 0
            except:
                pass

        return pytube.YouTube(this.search(input)), 0

        
def download_from_pytube(yt_obj:pytube.YouTube):
        try:
            out_file = None
            try:
                out_file = yt_obj.streams.get_audio_only().download(output_path = 'downloads/')
            except:
                print(f"no audio only source for {yt_obj.title}")

            if out_file == None:
                out_file = yt_obj.streams.get_lowest_resolution.download(filename = yt_obj.video_id, output_path = 'downloads/')

            new_file = f"downloads/{yt_obj.video_id}.mp3"
            os.rename(out_file, new_file)
            print(f"Sucessfully downloaded {yt_obj.title}")
        except BaseException as e:
           print(f"Unable to download video {yt_obj.watch_url}\n {e}")

if __name__ == '__main__':
    yt = YT()
    title, url = yt.download_from_keyword("victor wooten")
    print(f"title {title} url {url}")

