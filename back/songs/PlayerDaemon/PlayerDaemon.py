import time
from datetime import timedelta
from multiprocessing import Queue
from pathlib import Path
from threading import Thread
from typing import Optional

from songs.logger import logger_print
from songs.models import Song
from songs.song_download_helper import download_song_helper
from songs.ytdl import get_next_related, video_id_to_url

from .musicplayer import MusicPlayer


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
        self._last_song: Optional[Song] = None
        self._default_number_improvise = default_number_improvise
        self._improvised_auto = False
        self._music_player: MusicPlayer = MusicPlayer()
        self._pass_next = False

    def __play_next(self) -> Optional[Song]:
        song = self._queue_song.get()
        filename = str(song.path_music.path)
        try:
            self._music_player.play(Path(filename))
        except Exception as esc:
            logger_print(f"Error loading {filename} {esc}")
            return None
        self._music_player.set_pause(False)
        self._improvised_auto = False
        return song

    def get_pos(self) -> timedelta:
        pos = self._music_player.get_pos()
        if pos is None:
            return timedelta(0)
        return timedelta(seconds=pos)

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
            if self.get_pos() > duration_threshold:
                Thread(
                    target=self.improvise,
                    args=(
                        self._queue_process_msg,
                        self._last_song,
                        self._default_number_improvise,
                    ),
                ).start()
                self._improvised_auto = True

    def __react_event(self) -> None:
        if self._queue_action.empty():
            return
        action = self._queue_action.get()
        if action == "pause":
            self._music_player.set_pause(True)
        elif action == "resume":
            self._music_player.set_pause(False)
        elif action == "next":
            self._pass_next = True
        elif action == "stop":
            self._music_player.stop()
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
            self._queue_process_msg.put("pos:" + str(self.get_pos().total_seconds()))
        elif action.startswith("set_volume:"):
            volume = int(action[len("set_volume:") :])
            self._music_player.set_vol(volume)
        elif action == "get_volume":
            volume = self._music_player.get_vol()
            self._queue_process_msg.put(f"volume:{volume}")
        elif action.startswith("set_pos:") and self._last_song is not None:
            pos = int(action[len("set_pos:") :])
            self._music_player.set_pos(pos)

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
            while self._music_player.has_song():
                self.__react_event()
                if self._pass_next or self._stop:
                    break
                self.__on_play()
                time.sleep(0.1)
            if self._stop:
                break
            self.__on_next()

    def __call__(self) -> None:
        from .musicplayer_pygame import MusicPlayerPygame

        self._music_player = MusicPlayerPygame()
        self.__loop()
        del self._music_player
        self._music_player = MusicPlayer()
