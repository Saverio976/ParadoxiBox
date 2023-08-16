import time
from datetime import timedelta
from multiprocessing import Process, Queue
from threading import Lock
from typing import Any, List, Optional, Tuple

from django.dispatch import receiver
from django.utils.autoreload import file_changed

from .logger import logger_print
from .models import Song

DEFAULT_NUMBER_IMPROVISE = 2
DEFAULT_VOLUME = 50


class Player:
    def __init__(self) -> None:
        super().__init__()
        self._playlist: List[Song] = []
        self._current_song: Optional[Song] = None
        self._current_song_time: Optional[timedelta] = None
        self._queue_song: Optional["Queue[Song]"] = None
        self._queue_action: Optional["Queue[str]"] = None
        self._queue_process_msg: Optional["Queue[str]"] = None
        self._process: Optional[Process] = None
        self._process_started = False
        self._paused = False
        self._improvise = False
        self._locker = Lock()
        self._volume = DEFAULT_VOLUME

    def _init_process(self) -> None:
        if self._process_started is False:
            from songs.player_daemon import PlayerDaemon

            logger_print("Starting process")
            self._queue_song = Queue()
            self._queue_action = Queue()
            self._queue_process_msg = Queue()
            self._queue_action.put(f"set_volume:{self._volume}")
            self._process_started = True
            player_daemon = PlayerDaemon(
                queue_song=self._queue_song,
                queue_action=self._queue_action,
                queue_process_msg=self._queue_process_msg,
                improvise=self._improvise,
                default_number_improvise=DEFAULT_NUMBER_IMPROVISE,
            )
            self._process = Process(target=player_daemon, daemon=True)
            self._process.start()

    def queue(self, song: Song) -> None:
        self._init_process()
        self._proccess_msg_queue()
        if self._queue_song:
            self._locker.acquire()
            self._queue_song.put(song)
            if len(self._playlist) == 0 and self._current_song is None:
                self._current_song = song
            else:
                self._playlist.append(song)
            self._locker.release()

    def pause(self) -> None:
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put("pause")
            self._paused = True

    def resume(self) -> None:
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put("resume")
            self._paused = False

    def next(self) -> None:
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put("next")

    def stop(self) -> None:
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put("stop")
        if self._process:
            self._process.join()
        self._process = None
        self._playlist = []
        self._current_song = None
        self._current_song_time = None
        self._queue_action = None
        self._queue_process_msg = None
        self._queue_song = None
        self._process_started = False

    def _proccess_msg_queue(self) -> None:
        if self._queue_process_msg:
            while self._queue_process_msg.empty() is False:
                msg = self._queue_process_msg.get()
                if msg == "next":
                    self._locker.acquire()
                    if len(self._playlist) > 0:
                        self._current_song = self._playlist.pop(0)
                    else:
                        self._current_song = None
                    self._locker.release()
                elif msg.startswith("pos:"):
                    msg = msg[len("pos:") :]
                    self._current_song_time = timedelta(seconds=float(msg))
                elif msg.startswith("add:"):
                    msg = msg[len("add:") :]
                    try:
                        self.queue(Song.objects.get(id=msg))
                    except:
                        pass
                elif msg.startswith("volume:"):
                    self._volume = int(msg[len("volume:") :])

    def get_list_song(self) -> List[Song]:
        self._proccess_msg_queue()
        return [song for song in self._playlist]

    def get_current_song(self) -> Tuple[Optional[Song], timedelta]:
        self._proccess_msg_queue()
        if self._current_song is None:
            return None, timedelta(milliseconds=0)
        self._current_song_time = None
        if self._queue_action:
            self._queue_action.put("get_pos")
        while self._current_song_time is None:
            self._proccess_msg_queue()
            time.sleep(0.01)
        return self._current_song, self._current_song_time

    def get_paused(self) -> bool:
        self._proccess_msg_queue()
        return self._paused

    def toggle_improvise(self) -> None:
        self._improvise = not self._improvise
        if self._queue_action:
            self._queue_action.put(
                f"improvise_{'true' if self._improvise else 'false'}"
            )

    def get_improvise(self) -> bool:
        return self._improvise

    def improvise_now(self) -> None:
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put("improvise")

    def get_volume(self) -> int:
        """
        Get the current volume between 0 and 100
        """
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put("get_volume")
        time.sleep(0.15)
        self._proccess_msg_queue()
        return self._volume

    def set_volume(self, volume: int) -> None:
        """
        Set the current volume between 0 and 100
        """
        volume = max(0, min(volume, 100))
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put(f"set_volume:{volume}")


PLAYER = Player()


@receiver(file_changed, dispatch_uid="on_file_changed_player_stop")
def on_file_changed(sender: Any, **kwargs: Any):
    del sender, kwargs
    PLAYER.stop()
    return False
