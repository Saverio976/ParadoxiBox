from pathlib import Path
import asyncio
from threading import Thread, Lock
from typing import Any, Callable, Optional
from datetime import timedelta

from mutagen.mp3 import MP3

from songs.logger import logger_print
from .musicplayer import MusicPlayer
import discord

import time

from django.conf import settings

def _on_end(e: Any):
    if e:
        logger_print("ERROR: MusicPlayerDiscordPy:", e)

class AudioSourceTracked(discord.PCMVolumeTransformer[discord.FFmpegPCMAudio]):
    def __init__(self, source: discord.FFmpegPCMAudio):
        super().__init__(source)
        self._count_20ms = 0

    def read(self) -> bytes:
        data = super().read()
        if data:
            self._count_20ms += 1
        return data

    @property
    def progress(self) -> float:
        return self._count_20ms * 0.02 # count_20ms * 20ms

class MusicPlayerDiscordPy(MusicPlayer):
    def __init__(self, configPath: Path = settings.BASE_DIR / "musicplayer-discordpy.json") -> None:
        """only mp3 for now"""
        super().__init__(configPath)

        self._client = discord.Client(intents=discord.Intents.default())
        self._token = self.conf_json["token"]
        self._voice_channel_id = self.conf_json["voice_channel_id"]
        self._cur_song = ""
        self.__voice_channel = None
        self.__lock = Lock()
        self.__lock_run = Lock()
        self._loop = None

        @self._client.event
        async def on_ready():
            if self._client.user is None:
                return
            self._loop = asyncio.get_running_loop()
            print(f'Logged in as {self._client.user} (ID: {self._client.user.id})')


        self._threaded_bot = Thread(target=self._connection)
        self._threaded_bot.start()
        self._threaded_loop = Thread(target=self._loop_)
        self._threaded_loop.start()


    def __del__(self):
        asyncio.run(self._client.close())
        self._threaded_bot.join()
        self._loop.stop()
        self._threaded_loop.join()

    def _connection(self):
        self._client.run(self._token)

    def _loop_(self):
        self._loop.run_forever()

    def _run_in_async(self, func: Callable[[], Any]):
        self.__lock_run.acquire()
        asyncio.set_event_loop(self._loop)
        res = asyncio.run(func())
        self.__lock_run.release()
        return res

    def _ensure_connected(self) -> Optional[discord.VoiceClient]:
        while not self._client.is_ready():
            time.sleep(0.01)
        def check_id(x: Any):
            if isinstance(x, discord.VoiceClient):
                return x.channel.id == self._voice_channel_id
            return False
        voices_clients = self._client.voice_clients
        for i, val in enumerate(map(check_id, voices_clients)):
            voice_client = voices_clients[i]
            if val and isinstance(voice_client, discord.VoiceClient):
                return voice_client
            return None
        self.__voice_channel = None
        async def get_voice_channel():
            voice_channel = await self._client.fetch_channel(self._voice_channel_id)
            self.__lock.acquire()
            self.__voice_channel = voice_channel
            self.__lock.release()
        self._run_in_async(get_voice_channel)
        while self.__voice_channel is None:
            time.sleep(0.01)
        if not isinstance(self.__voice_channel, discord.VoiceChannel):
            logger_print("ERROR: MusicPlayerDiscordPy: voice channel id is bad")
            return None
        self.__lock.acquire()
        asyncio.run(self.__voice_channel.connect())
        self.__lock.release()
        return self._ensure_connected()


    def has_song(self) -> bool:
        """
        Check if a song is being played/paused

        return false if no song; true otherwise
        """
        voice_client = self._ensure_connected()
        if voice_client is None:
            return False
        source = voice_client.source
        return not (source is None)

    def play(self, filepath: Path) -> bool:
        """
        Play music file passed as parameter

        return false if can't play it; true otherwise
        """
        voice_client = self._ensure_connected()
        if voice_client is None:
            return False
        source = AudioSourceTracked(discord.FFmpegPCMAudio(str(filepath)))
        voice_client.play(source, after=_on_end)
        self._cur_song = str(filepath)
        return True

    def get_pos(self) -> Optional[float]:
        """
        Get position of the current song (time in seconds)

        return None if no song played; the number of seconds otherwise
        """
        voice_client = self._ensure_connected()
        if voice_client is None:
            return None
        source = voice_client.source
        if isinstance(source, AudioSourceTracked):
            return timedelta(milliseconds=source.progress).total_seconds()
        return None

    def get_pos_max(self) -> Optional[float]:
        """
        Get maximal position that the current song can go (time in seconds)

        return None if no song played; the number of seconds otherwise
        """
        if not self.has_song():
            return None
        song = MP3(self._cur_song)
        return song.info.length

    def set_pos(self, pos: float) -> bool:
        """
        Set position of the current song (time in seconds)

        return false if no song played; true otherwise
        """
        voice_client = self._ensure_connected()
        if voice_client is None:
            return False
        if not self.has_song():
            return False
        source = AudioSourceTracked(discord.FFmpegPCMAudio(self._cur_song))
        for _ in range(int(pos * 1000)):
            source.read()
        voice_client.source = source
        return True

    def get_pause(self) -> bool:
        """
        Get status of pause

        return true if song paused; otherwise false
        """
        voice_client = self._ensure_connected()
        if voice_client is None:
            return False
        return voice_client.is_paused()

    def set_pause(self, paused: bool):
        """
        Set status of pause
        """
        voice_client = self._ensure_connected()
        if voice_client is None:
            return False
        if paused:
            voice_client.pause()
        else:
            voice_client.resume()
        return True

    def get_vol(self) -> Optional[float]:
        """
        Get volume

        return None if no volume; else the number
        """
        voice_client = self._ensure_connected()
        if voice_client is None:
            return None
        source = voice_client.source
        if isinstance(source, AudioSourceTracked):
            return source.volume * 100.0
        return None

    def get_vol_max(self) -> Optional[float]:
        """
        Get maximal volume

        return None if no volume; else the number
        """
        return 100.0

    def set_vol(self, vol: float) -> bool:
        """
        Set volume (between `0` and `self.get_pos_max()`)

        return false if volume can't be updated; true otherwise
        """
        voice_client = self._ensure_connected()
        if voice_client is None:
            return False
        source = voice_client.source
        if isinstance(source, AudioSourceTracked):
            source.volume = vol / 100.0
            return True
        return False
