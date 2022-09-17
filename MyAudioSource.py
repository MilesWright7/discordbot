
from ssl import Options
import discord

class MyAudioSource(discord.AudioSource):

    def __init__(self, song, playbackSpeed = 1):
        self.song = song
        self.playback_speed = playbackSpeed
        if playbackSpeed == 1:
            options = None
        else:
            options = f'-filter:a "atempo={playbackSpeed:.1f}"'
        self.audio = discord.FFmpegPCMAudio(song.location(),options=options)

    def read(self):
        self.song.current_time += .02
        return self.audio.read()

    def cleanup(self):
        self.audio.cleanup()

    def seek(self, seconds):
        # delete the old audio and make it fresh again
        self.audio.cleanup()
        self.audio = discord.FFmpegPCMAudio(self.song.location())

        # read that amount of time off the front of the file
        self.audio._stdout.read(OpusEncoder.FRAME_SIZE * seconds * 50)
        self.song.current_time = seconds
