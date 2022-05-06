import MilesYoutube

yt = MilesYoutube.YT()
search = yt.find_video("goose polyphia")
playlist = yt.find_video("https://www.youtube.com/playlist?list=PL-m8lY-xpuJn5_jML8eNbCgA7pokB9CkK")
link = yt.find_video("https://www.youtube.com/watch?v=lhEpE7_JZ3U")
print(f"search {search}" )
print(f"link {link}")
print(f"playlist {playlist}")
MilesYoutube.download_from_pytube(search[0])