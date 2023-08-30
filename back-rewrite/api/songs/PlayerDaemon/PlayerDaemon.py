import time
from datetime import timedelta
from multiprocessing import Queue
from pathlib import Path
from threading import Thread
from typing import Any, Dict, List, Optional
import json5

from django.conf import settings

from songs.logger import logger_print
from songs.models import Song
from songs.song_download_helper import download_song_helper
from songs.ytdl import get_next_related, video_id_to_url

from .musicplayer import MusicPlayer

CONF_PATH = settings.BASE_DIR / "config-audio.jsonc"


class PlayerDaemon:
    def __init__(
        self,
        queue_song: "Queue[Song]",
        queue_action: "Queue[str]",
        queue_process_msg: "Queue[str]",
        improvise: bool,
        default_number_improvise: int = 2,
    ) -> None:
        super().__init__()
        self._conf_path = CONF_PATH
        self._queue_song = queue_song
        self._queue_action = queue_action
        self._queue_process_msg = queue_process_msg
        self._improvise = improvise
        self._stop = False
        self._last_song: Optional[Song] = None
        self._default_number_improvise = default_number_improvise
        self._improvised_auto = False
        self._music_player: List[MusicPlayer] = [MusicPlayer()]
        self._pass_next = False

    def __play_next(self) -> Optional[Song]:
        song = self._queue_song.get()
        filename = str(song.path_music.path)
        is_error = False
        for player in self._music_player:
            try:
                player.play(Path(filename))
            except Exception as esc:
                is_error = True
                logger_print(f"Error loading {filename} {esc}")
        if is_error:
            self.__del__audio_player__()
            self.__init_audio_player__(self._conf_path)
            return None
        for player in self._music_player:
            player.set_pause(False)
        self._last_song = song
        self._improvised_auto = False
        return song

    def _get_pos(self) -> timedelta:
        pos_s: List[float] = []
        pos_not_ok: List[bool] = []
        for player in self._music_player:
            pos = player.get_pos()
            pos_not_ok.append(pos is None)
            if pos is not None:
                pos_s.append(pos)
        if False in pos_not_ok and True in pos_not_ok:
            self.__del__audio_player__()
            self.__init_audio_player__(self._conf_path)
            return timedelta(0)
        mean = sum(pos_s) / len(pos_s)
        if max(pos_s) - min(pos_s) > 2:
            is_error = False
            for player in self._music_player:
                try:
                    player.set_pos(mean)
                except Exception as esc:
                    is_error = True
                    logger_print(f"Error setting pos {mean} {esc}")
            if is_error:
                self.__del__audio_player__()
                self.__init_audio_player__(self._conf_path)
                return timedelta(0)
        return timedelta(seconds=mean)

    @staticmethod
    def improvise(
        queue_process_msg: "Queue[str]",
        last_song: Song,
        default_number_improvise: int = 2,
    ) -> bool:
        logger_print("Improvise")
        try:
            videos_id_next = get_next_related(
                query=f"{last_song.artist} {last_song.title}",
                limit=default_number_improvise,
            )
            for vid in videos_id_next:
                url_next = video_id_to_url(vid)
                download_song_helper(
                    url_next,
                    noplaylist=True,
                    to_execute=lambda song: queue_process_msg.put(f"add:{song.id}"),
                    threaded=True,
                )
            return True
        except Exception as esc:
            logger_print(esc)
            return False

    def __on_play(self) -> None:
        if (
            self._improvise
            and self._last_song
            and self._queue_song.empty()
            and self._improvised_auto is False
        ):
            duration_threshold: timedelta = self._last_song.duration - timedelta(
                seconds=4
            )
            if self._get_pos() > duration_threshold:
                Thread(
                    target=self.improvise,
                    args=(
                        self._queue_process_msg,
                        self._last_song,
                        self._default_number_improvise,
                    ),
                ).start()
                self._improvised_auto = True

    def _set_pause(self, paused: bool) -> None:
        is_error = False
        for player in self._music_player:
            try:
                player.set_pause(paused)
            except Exception as esc:
                logger_print(esc)
                is_error = True
        if is_error:
            self.__del__audio_player__()
            self.__init_audio_player__(self._conf_path)
            return None

    def _stop_fn(self) -> None:
        is_error = False
        for player in self._music_player:
            try:
                player.stop()
            except Exception as esc:
                logger_print(esc)
                is_error = True
        if is_error:
            self.__del__audio_player__()
            self.__init_audio_player__(self._conf_path)
            return None

    def _set_vol(self, volume: int) -> None:
        is_error = False
        for player in self._music_player:
            try:
                player.set_vol(volume)
            except Exception as esc:
                logger_print(esc)
                is_error = True
        if is_error:
            self.__del__audio_player__()
            self.__init_audio_player__(self._conf_path)
            return None

    def _get_vol(self) -> int:
        vol_s: List[float] = []
        is_error = False
        for player in self._music_player:
            vol = None
            try:
                vol = player.get_vol()
            except Exception as esc:
                logger_print(esc)
                vol = None
            if vol is None:
                is_error = True
            else:
                vol_s.append(vol)
        if is_error:
            self.__del__audio_player__()
            self.__init_audio_player__(self._conf_path)
            return 0
        return int(sum(vol_s) / len(vol_s))

    def _set_pos(self, pos: int) -> None:
        is_error = False
        for player in self._music_player:
            try:
                player.set_pos(pos)
            except Exception as esc:
                logger_print(esc)
                is_error = True
        if is_error:
            self.__del__audio_player__()
            self.__init_audio_player__(self._conf_path)
            return None


    def __react_event(self) -> None:
        if self._queue_action.empty():
            return
        action = self._queue_action.get()
        if action == "pause":
            self._set_pause(True)
        elif action == "resume":
            self._set_pause(False)
        elif action == "next":
            self._pass_next = True
        elif action == "stop":
            self._stop_fn()
            self._stop = True
        elif action == "improvise_true":
            self._improvise = True
        elif action == "improvise_false":
            self._improvise = False
        elif action.startswith("improvise_"):
            nb_improvise = int(action[len("improvise_") :])
            Thread(
                target=self.improvise,
                args=(
                    self._queue_process_msg,
                    self._last_song,
                    nb_improvise,
                ),
            ).start()
        elif action == "get_pos":
            self._queue_process_msg.put("pos:" + str(self._get_pos().total_seconds()))
        elif action.startswith("set_volume:"):
            volume = int(action[len("set_volume:") :])
            self._set_vol(volume)
        elif action == "get_volume":
            volume = self._get_vol()
            self._queue_process_msg.put(f"volume:{volume}")
        elif action.startswith("set_pos:") and self._last_song is not None:
            pos = int(action[len("set_pos:") :])
            self._set_pos(pos)

    def __on_next(self) -> None:
        self._queue_process_msg.put("next")

    def _has_song(self) -> bool:
        bool_has_song: List[bool] = []
        is_error = False
        for player in self._music_player:
            try:
                bool_has_song.append(player.has_song())
            except Exception as esc:
                logger_print(esc)
                is_error = True
        if is_error or (False in bool_has_song and True in bool_has_song):
            self.__del__audio_player__()
            self.__init_audio_player__(self._conf_path)
            return False
        return True in bool_has_song

    def __loop(self) -> None:
        while not self._stop:
            if self._queue_song.empty():
                self.__react_event()
                time.sleep(0.1)
                continue
            if song := self.__play_next():
                self._last_song = song
            else:
                time.sleep(0.1)
                continue
            while self._has_song():
                self.__react_event()
                if self._pass_next or self._stop:
                    break
                self.__on_play()
                time.sleep(0.1)
            if self._stop:
                break
            self.__on_next()

    def __init_audio_player__(self, confPath: Path) -> None:
        from .musicplayer_pygame import MusicPlayerPygame
        from .musicplayer_discordpy import MusicPlayerDiscordPy

        with open(confPath, "r") as f:
            conf_json = json5.loads(f.read())
            if not isinstance(conf_json, dict):
                conf_json = {}

        for backend in conf_json.get("musicplayer", []):
            if backend == "discordpy":
                self._music_player.append(MusicPlayerDiscordPy())
            elif backend == "pygame":
                self._music_player.append(MusicPlayerPygame())
            logger_print(f"Backend Audio added: {backend}")

    def __del__audio_player__(self) -> None:
        for player in self._music_player:
            player.stop()
            del player
        self._music_player = []

    def __call__(self, confPath: Path = CONF_PATH) -> None:
        self.__init_audio_player__(confPath)
        self._conf_path = confPath
        self.__loop()
        self.__del__audio_player__()
