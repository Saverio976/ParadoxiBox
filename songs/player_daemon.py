import time
from datetime import timedelta
from multiprocessing import Queue
from threading import Thread
from typing import Optional

import pygame

from songs.logger import logger_print
from songs.models import Song
from songs.song_download_helper import download_song_helper
from songs.ytdl import get_next_related, video_id_to_url


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
        self._queue_song = queue_song
        self._queue_action = queue_action
        self._queue_process_msg = queue_process_msg
        self._improvise = improvise
        self._stop = False
        self._paused = False
        self._last_song: Optional[Song] = None
        self._default_number_improvise = default_number_improvise

    def __play_next(self) -> Optional[Song]:
        song = self._queue_song.get()
        filename = str(song.path_music.path)
        try:
            pygame.mixer.music.load(filename)
        except Exception as esc:
            logger_print(f"Error loading {filename} {esc}")
            return None
        pygame.mixer.music.play()
        return song

    def get_pos(self) -> timedelta:
        return timedelta(milliseconds=pygame.mixer.music.get_pos())

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
        if self._improvise and self._last_song:
            duration_threshold: timedelta = self._last_song.duration - timedelta(
                seconds=4
            )
            if self.get_pos() > duration_threshold:
                Thread(
                    target=self.improvise,
                    args=(
                        self._queue_process_msg,
                        self._last_song,
                        self._default_number_improvise,
                    ),
                ).start()
                self._last_song = None

    def __react_event(self) -> None:
        if self._queue_action.empty():
            return
        action = self._queue_action.get()
        if action == "pause":
            pygame.mixer.music.pause()
            self._paused = True
        elif action == "resume":
            pygame.mixer.music.unpause()
            self._paused = False
        elif action == "next":
            pygame.mixer.music.stop()
            self._paused = False
        elif action == "stop":
            pygame.mixer.music.stop()
            self._stop = True
            self._paused = False
        elif action == "improvise_true":
            self._improvise = True
        elif action == "improvise_false":
            self._improvise = False
        elif action == "improvise":
            Thread(
                target=self.improvise,
                args=(
                    self._queue_process_msg,
                    self._last_song,
                    self._default_number_improvise,
                ),
            ).start()
        elif action == "get_pos":
            self._queue_process_msg.put("pos:" + str(self.get_pos().total_seconds()))

    def __on_next(self) -> None:
        self._queue_process_msg.put("next")

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
            while pygame.mixer.music.get_busy() or self._paused:
                self.__react_event()
                self.__on_play()
                time.sleep(0.1)
            self.__on_next()

    def __call__(self) -> None:
        pygame.mixer.init()
        self.__loop()
