import asyncio
import time
from datetime import timedelta
from multiprocessing import Process, Queue
from pathlib import Path
from typing import Any, Optional, Tuple, Union

import discord
from discord.ext import tasks
from django.conf import settings
from mutagen.mp3 import MP3

from songs.logger import logger_print

from .musicplayer import MusicPlayer


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
        return self._count_20ms * 0.02  # count_20ms * 20ms


class MusicPlayerDiscordPyDaemon:
    def __init__(
        self,
        queue_in: "Queue[str]",
        queue_out: "Queue[str]",
        token: str,
        voice_channel_id: int,
    ) -> None:
        """only mp3 for now"""
        super().__init__()

        self._client = discord.Client(intents=discord.Intents.default())
        self._token = token
        self._voice_channel_id = voice_channel_id
        self._cur_song = ""
        self._queue_in = queue_in
        self._queue_out = queue_out

    @staticmethod
    def send_msg(
        queue: "Queue[str]",
        title: str,
        value: Union[bool, float, None, str],
        no_value: bool = False,
    ):
        if no_value:
            queue.put(title)
            return
        value_msg = ""
        if value is None:
            value_msg = "None"
        elif isinstance(value, float):
            value_msg = str(value)
        elif value is True:
            value_msg = "True"
        elif value is False:
            value_msg = "False"
        else:
            value_msg = f"{value}"
        queue.put(f"{title}:{value_msg}")

    @staticmethod
    def get_msg(msg: str) -> Tuple[str, Union[bool, float, None, str]]:
        title, res = msg.split(":", 1)
        if res == "None" or res == "":
            return (title, None)
        if res == "True":
            return (title, True)
        if res == "False":
            return (title, False)
        try:
            return (title, float(res))
        except:
            return (title, res)

    async def _react_event(self):
        if self._queue_in.empty():
            return
        msg = self._queue_in.get()
        title, value = self.get_msg(msg)
        if title == "stop":
            await self._client.close()
        elif title == "play" and isinstance(value, str):
            res = await self._play(value)
            self.send_msg(self._queue_out, "play", res)
        elif title == "has_song":
            res = await self._has_song()
            self.send_msg(self._queue_out, "has_song", res)
        elif title == "get_pos":
            res = await self._get_pos()
            self.send_msg(self._queue_out, "get_pos", res)
        elif title == "get_pos_max":
            res = await self._get_pos_max()
            self.send_msg(self._queue_out, "get_pos_max", res)
        elif title == "set_pos" and isinstance(value, float):
            res = await self._set_pos(value)
            self.send_msg(self._queue_out, "set_pos", res)
        elif title == "get_pause":
            res = await self._get_pause()
            self.send_msg(self._queue_out, "get_pause", res)
        elif title == "set_pause" and isinstance(value, bool):
            res = await self._set_pause(value)
            self.send_msg(self._queue_out, "set_pause", res)
        elif title == "get_vol":
            res = await self._get_vol()
            self.send_msg(self._queue_out, "get_vol", res)
        elif title == "get_vol_max":
            res = await self._get_vol_max()
            self.send_msg(self._queue_out, "get_vol_max", res)
        elif title == "set_vol" and isinstance(value, float):
            res = await self._set_pos(value)
            self.send_msg(self._queue_out, "set_vol", res)

    def start(self):
        loop = asyncio.get_event_loop()

        @tasks.loop(seconds=0.1)
        async def react_event():
            await self._react_event()

        @self._client.event
        async def on_ready():
            if self._client.user is None:
                return
            logger_print(
                f"Logged in as {self._client.user} (ID: {self._client.user.id})"
            )
            react_event.start()
            await self._client.change_presence(activity=discord.Game(name="with music"))

        loop.run_until_complete(self._client.start(self._token))

    async def _ensure_connected(self) -> Optional[discord.VoiceClient]:
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
        voice_channel = await self._client.fetch_channel(self._voice_channel_id)
        if not isinstance(voice_channel, discord.VoiceChannel):
            logger_print("ERROR: MusicPlayerDiscordPy: voice channel id is bad")
            return None
        await voice_channel.connect()
        return await self._ensure_connected()

    async def _has_song(self) -> bool:
        """
        Check if a song is being played/paused

        return false if no song; true otherwise
        """
        voice_client = await self._ensure_connected()
        if voice_client is None:
            return False
        source = voice_client.source
        return not (source is None)

    async def _play(self, filepath: str) -> bool:
        """
        Play music file passed as parameter

        return false if can't play it; true otherwise
        """
        voice_client = await self._ensure_connected()
        if voice_client is None:
            return False
        source = AudioSourceTracked(discord.FFmpegPCMAudio(str(filepath)))
        voice_client.play(source, after=_on_end)
        self._cur_song = str(filepath)
        return True

    async def _get_pos(self) -> Optional[float]:
        """
        Get position of the current song (time in seconds)

        return None if no song played; the number of seconds otherwise
        """
        voice_client = await self._ensure_connected()
        if voice_client is None:
            return None
        source = voice_client.source
        if isinstance(source, AudioSourceTracked):
            return timedelta(milliseconds=source.progress).total_seconds()
        return None

    async def _get_pos_max(self) -> Optional[float]:
        """
        Get maximal position that the current song can go (time in seconds)

        return None if no song played; the number of seconds otherwise
        """
        if not await self._has_song():
            return None
        song = MP3(self._cur_song)
        return song.info.length

    async def _set_pos(self, pos: float) -> bool:
        """
        Set position of the current song (time in seconds)

        return false if no song played; true otherwise
        """
        voice_client = await self._ensure_connected()
        if voice_client is None:
            return False
        if not await self._has_song():
            return False
        source = AudioSourceTracked(discord.FFmpegPCMAudio(self._cur_song))
        for _ in range(int(pos * 1000)):
            source.read()
        voice_client.source = source
        return True

    async def _get_pause(self) -> bool:
        """
        Get status of pause

        return true if song paused; otherwise false
        """
        voice_client = await self._ensure_connected()
        if voice_client is None:
            return False
        return voice_client.is_paused()

    async def _set_pause(self, paused: bool) -> bool:
        """
        Set status of pause
        """
        voice_client = await self._ensure_connected()
        if voice_client is None:
            return False
        if paused:
            voice_client.pause()
        else:
            voice_client.resume()
        return True

    async def _get_vol(self) -> Optional[float]:
        """
        Get volume

        return None if no volume; else the number
        """
        voice_client = await self._ensure_connected()
        if voice_client is None:
            return None
        source = voice_client.source
        if isinstance(source, AudioSourceTracked):
            return source.volume * 100.0
        return None

    async def _get_vol_max(self) -> Optional[float]:
        """
        Get maximal volume

        return None if no volume; else the number
        """
        return 100.0

    async def _set_vol(self, vol: float) -> bool:
        """
        Set volume (between `0` and `self.get_pos_max()`)

        return false if volume can't be updated; true otherwise
        """
        voice_client = await self._ensure_connected()
        if voice_client is None:
            return False
        source = voice_client.source
        if isinstance(source, AudioSourceTracked):
            source.volume = vol / 100.0
            return True
        return False


class MusicPlayerDiscordPy(MusicPlayer):
    def __init__(
        self, configPath: Path = settings.BASE_DIR / "musicplayer-discordpy.json"
    ) -> None:
        """
        configPath: Path
            json file with some config for the music player backend
        """
        super().__init__(configPath)
        self._queue_in: "Queue[str]" = Queue()
        self._queue_out: "Queue[str]" = Queue()
        self._music_daemon = MusicPlayerDiscordPyDaemon(
            self._queue_in,
            self._queue_out,
            self.conf_json["token"],
            self.conf_json["voice_channel_id"],
        )
        self._process = Process(target=self._music_daemon.start, daemon=True)
        self._process.start()

    def __del__(self):
        self._process.join()

    def _empty_queue(self):
        while not self._queue_out.empty():
            self._queue_out.get()

    def has_song(self) -> bool:
        """
        Check if a song is being played/paused

        return false if no song; true otherwise
        """
        self._empty_queue()
        self._music_daemon.send_msg(self._queue_in, "has_song", None, True)
        msg = self._queue_out.get()
        val = self._music_daemon.get_msg(msg)
        if isinstance(val, bool):
            return val
        return False

    def play(self, filepath: Path) -> bool:
        """
        Play music file passed as parameter

        return false if can't play it; true otherwise
        """
        self._empty_queue()
        self._music_daemon.send_msg(self._queue_in, "play", str(filepath), False)
        msg = self._queue_out.get()
        _, val = self._music_daemon.get_msg(msg)
        if isinstance(val, bool):
            return val
        return False

    def get_pos(self) -> Optional[float]:
        """
        Get position of the current song (time in seconds)

        return None if no song played; the number of seconds otherwise
        """
        self._empty_queue()
        self._music_daemon.send_msg(self._queue_in, "get_pos", None, True)
        msg = self._queue_out.get()
        _, val = self._music_daemon.get_msg(msg)
        if isinstance(val, float):
            return val
        return None

    def get_pos_max(self) -> Optional[float]:
        """
        Get maximal position that the current song can go (time in seconds)

        return None if no song played; the number of seconds otherwise
        """
        self._empty_queue()
        self._music_daemon.send_msg(self._queue_in, "get_pos_max", None, True)
        msg = self._queue_out.get()
        _, val = self._music_daemon.get_msg(msg)
        if isinstance(val, float):
            return val
        return None

    def set_pos(self, pos: float) -> bool:
        """
        Set position of the current song (time in seconds)

        return false if no song played; true otherwise
        """
        self._empty_queue()
        self._music_daemon.send_msg(self._queue_in, "set_pos", pos, False)
        msg = self._queue_out.get()
        _, val = self._music_daemon.get_msg(msg)
        if isinstance(val, bool):
            return val
        return False

    def get_pause(self) -> bool:
        """
        Get status of pause

        return true if song paused; otherwise false
        """
        self._empty_queue()
        self._music_daemon.send_msg(self._queue_in, "get_pause", None, True)
        msg = self._queue_out.get()
        _, val = self._music_daemon.get_msg(msg)
        if isinstance(val, bool):
            return val
        return False

    def set_pause(self, paused: bool) -> bool:
        """
        Set status of pause
        """
        self._empty_queue()
        self._music_daemon.send_msg(self._queue_in, "set_pause", paused, False)
        msg = self._queue_out.get()
        _, val = self._music_daemon.get_msg(msg)
        if isinstance(val, bool):
            return val
        return False

    def get_vol(self) -> Optional[float]:
        """
        Get volume

        return None if no volume; else the number
        """
        self._empty_queue()
        self._music_daemon.send_msg(self._queue_in, "get_vol", None, True)
        msg = self._queue_out.get()
        _, val = self._music_daemon.get_msg(msg)
        if isinstance(val, float):
            return val
        return None

    def get_vol_max(self) -> Optional[float]:
        """
        Get maximal volume

        return None if no volume; else the number
        """
        self._empty_queue()
        self._music_daemon.send_msg(self._queue_in, "get_vol_max", None, True)
        msg = self._queue_out.get()
        _, val = self._music_daemon.get_msg(msg)
        if isinstance(val, float):
            return val
        return None

    def set_vol(self, vol: float) -> bool:
        """
        Set volume (between `0` and `self.get_pos_max()`)

        return false if volume can't be updated; true otherwise
        """
        self._empty_queue()
        self._music_daemon.send_msg(self._queue_in, "set_vol", vol, False)
        msg = self._queue_out.get()
        _, val = self._music_daemon.get_msg(msg)
        if isinstance(val, bool):
            return val
        return False

    def stop(self):
        """
        Stop all action (the player will shutdown maybe)
        """
        self._empty_queue()
        self._music_daemon.send_msg(self._queue_in, "stop", None, True)
