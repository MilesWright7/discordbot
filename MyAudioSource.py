import discord


class MyAudioSource(discord.AudioSource):
	def __init__(self, song, playbackSpeed = 1, nightcore = False):
		self.song = song
		song.current_time = 0
		self.playback_speed = playbackSpeed
		if nightcore:
			self.options = "-filter_complex [0:a:0]asetrate=1.15*44.1k,aresample=resampler=soxr:precision=24:osf=s32:tsf=s32p:osr=44.1k"
		elif playbackSpeed == 1:
			self.options = None
		else:
			self.options = f'-filter:a "atempo={playbackSpeed:.1f}"'
		self.audio = discord.FFmpegPCMAudio(song.location(),options=self.options)
		

	def read(self):
		if not self.playing_sound:
			self.song.current_time += .02
			return self.audio.read()
		else:
			data = self.sound.read()
			if data:
				return data
			else:
				self.playing_sond = False
				return self.read()


	def cleanup(self):
		self.audio.cleanup()


	def seek(self, seconds):
		# delete the old audio and make it fresh again
		self.audio.cleanup()
		self.audio = discord.FFmpegPCMAudio(self.song.location(),options=self.options)

		# read that amount of time off the front of the file
		self.audio._stdout.read(discord.opus.Encoder.FRAME_SIZE * seconds * 50)
		self.song.current_time = seconds


	def play_sound(self, sound):
		self.sound = discord.FFmpegAudio(sound.location())
		self.playing_sond = True
