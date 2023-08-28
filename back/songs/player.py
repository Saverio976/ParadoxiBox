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
        """
        Initialize the process (player daemon)
        """
        if self._process_started is False:
            from songs.PlayerDaemon import PlayerDaemon

            logger_print("Starting process")
            self._queue_song = Queue()
            self._queue_action = Queue()
            self._queue_process_msg = Queue()
            self._queue_action.put(f"set_volume:{self._volume}")
            self._process_started = True
            player_daemon = PlayerDaemon.PlayerDaemon(
                queue_song=self._queue_song,
                queue_action=self._queue_action,
                queue_process_msg=self._queue_process_msg,
                improvise=self._improvise,
                default_number_improvise=DEFAULT_NUMBER_IMPROVISE,
            )
            self._process = Process(target=player_daemon)
            self._process.start()

    def __del__(self):
        if self._process:
            self._process.kill()

    def queue(self, song: Song) -> None:
        """
        Queue a song
        """
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
        """
        Pause the song
        """
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put("pause")
            self._paused = True

    def resume(self) -> None:
        """
        Resume the song
        """
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put("resume")
            self._paused = False

    def next(self) -> None:
        """
        Play the next song in the queue
        """
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put("next")

    def stop(self) -> None:
        """
        Stop the player daemon
        """
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
        """
        Process the message queue (interracton with the player daemon)
        """
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
                    self._volume = int(float(msg[len("volume:") :]))

    def get_list_song(self) -> List[Song]:
        """
        Get the list of song in the queue (not the current song in this list)
        """
        self._proccess_msg_queue()
        return [song for song in self._playlist]

    def get_current_song(self) -> Tuple[Optional[Song], timedelta]:
        """
        Get the current song + song time played
        """
        self._proccess_msg_queue()
        if self._current_song is None:
            return None, timedelta(milliseconds=0)
        self.get_song_time()
        if self._current_song_time is None:
            return self._current_song, timedelta(milliseconds=-1)
        return self._current_song, self._current_song_time

    def get_paused(self) -> bool:
        """
        Get if the player is paused
        """
        self._proccess_msg_queue()
        return self._paused

    def toggle_improvise(self) -> None:
        """
        Toggle improvise mode (auto improvise when end of all song in the queue)
        """
        self._improvise = not self._improvise
        if self._queue_action:
            self._queue_action.put(
                f"improvise_{'true' if self._improvise else 'false'}"
            )

    def get_improvise(self) -> bool:
        """
        Get if the player is improvise
        """
        return self._improvise

    def improvise_now(self, n: int) -> None:
        """
        Improvise the n next song based on current song
        """
        if self._current_song is None:
            return
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put(f"improvise_{n}")

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

    def set_song_time(self, time: int) -> None:
        """
        Set the current song time between 0 and 100
        """
        if self._current_song is None:
            return
        time = max(0, min(time, 100))
        self._proccess_msg_queue()
        if self._queue_action:
            self._queue_action.put(f"set_pos:{time}")

    def get_song_time(self) -> int:
        """
        Get the current song time between 0 and 100
        """
        if self._current_song is None:
            return -1
        self._proccess_msg_queue()
        self._current_song_time = None
        if self._queue_action:
            self._queue_action.put("get_pos")
        while self._current_song_time is None:
            self._proccess_msg_queue()
            time.sleep(0.01)
        percent = (
            self._current_song_time.total_seconds()
            * 100
            / self._current_song.duration.total_seconds()
        )
        return percent

    def process_events(self):
        self._proccess_msg_queue()


PLAYER = Player()


@receiver(file_changed, dispatch_uid="on_file_changed_player_stop")
def on_file_changed(sender: Any, **kwargs: Any):
    del sender, kwargs
    PLAYER.stop()
    return False
