import MilesYoutube
import discordbot

yt = MilesYoutube.YT()
search = yt.find_video("goose polyphia")
link = yt.find_video("https://www.youtube.com/watch?v=lhEpE7_JZ3U")
print(f"search {search}" )
print(f"link {link}")


song = discordbot.Song(search)



def modify_song(song):
    song.current_time = 100

