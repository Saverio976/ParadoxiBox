from datetime import timedelta
import time
from multiprocessing import Process, Queue
from typing import List, Optional, Tuple

from django.dispatch import receiver
from django.utils.autoreload import file_changed

from .models import Song
from .ytdl import get_next_related, video_id_to_url
from .logger import logger_print
from .song_download_helper import download_song_helper

DEFAULT_NUMBER_IMPROVISE = 2


class Player:
    def __init__(self) -> None:
        self._playlist: List[Song] = []
        self._current_song: Optional[Song] = None
        self._current_song_time: Optional[float] = None
        self._queue_song: Optional["Queue[Song]"] = None
        self._queue_action: Optional["Queue[str]"] = None
        self._queue_process_msg: Optional["Queue[str]"] = None
        self._process: Optional[Process] = None
        self._process_started = False
        self._paused = False
        self._improvise = False

    def _init_process(self) -> None:
        if self._process_started is False:
            logger_print("Starting process")
            self._queue_song = Queue()
            self._queue_action = Queue()
            self._queue_process_msg = Queue()
            self._process_started = True
            self._process = Process(
                target=self._process_loop,
                args=(self._queue_song, self._queue_action, self._queue_process_msg, self._improvise),
                daemon=True,
            )
            self._process.start()

    def _process_loop(
        self,
        queue_song: "Queue[Song]",
        queue_action: "Queue[str]",
        queue_process_msg: "Queue[str]",
        improvise: bool
    ):
        import pygame
        stop = False
        pygame.mixer.init()
        paused = False
        last_played: Optional[Song] = None
        while stop is False:
            if queue_song.empty() is False:
                song = queue_song.get()
                filename = song.path_music.path
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                last_played = song
            elif improvise is True and last_played is not None:
                logger_print("Auto next trying to guess")
                try:
                    videos_id_next = get_next_related(f"{last_played.artist} {last_played.title}", limit=DEFAULT_NUMBER_IMPROVISE)
                    for vid in videos_id_next:
                        url_next = video_id_to_url(vid)
                        download_song_helper(url_next, noplaylist=True, threaded=True, add_to_queue=True)
                    last_played = None
                    continue
                except Exception as esc:
                    logger_print(esc)
                    last_played = None
                    continue
            else:
                time.sleep(0.1)
                continue
            while pygame.mixer.music.get_busy() or paused:
                if queue_action.empty():
                    time.sleep(0.1)
                    continue
                action = queue_action.get()
                if action == "pause":
                    pygame.mixer.music.pause()
                    paused = True
                elif action == "resume":
                    pygame.mixer.music.unpause()
                    paused = False
                elif action == "next":
                    pygame.mixer.music.stop()
                    paused = False
                elif action == "stop":
                    pygame.mixer.music.stop()
                    stop = True
                    paused = False
                elif action == "improvise_true":
                    improvise = True
                elif action == "improvise_false":
                    improvise = False
                elif action == "get_pos":
                    queue_process_msg.put("pos:" + str(pygame.mixer.music.get_pos()))
            queue_process_msg.put("next")

    def _queue(self, song: Song) -> None:
        if self._queue_song:
            if len(self._playlist) == 0 and self._current_song is None:
                self._current_song = song
            else:
                self._playlist.append(song)


    def queue(self, song: Song) -> None:
        self._init_process()
        self._proccess_msg_queue()
        if self._queue_song:
            self._queue_song.put(song)
            self._queue(song)

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
                    if len(self._playlist) > 0:
                        self._current_song = self._playlist.pop(0)
                    else:
                        self._current_song = None
                elif msg.startswith("adding:"):
                    msg = msg[len("adding:"):]
                    song = Song.objects.get(id=msg)
                    self._queue(song)
                elif msg.startswith("pos:"):
                    msg = msg[len("pos:"):]
                    self._current_song_time = float(msg)

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
        return self._current_song, timedelta(milliseconds=self._current_song_time)

    def get_paused(self) -> bool:
        self._proccess_msg_queue()
        return self._paused

    def toggle_improvise(self) -> None:
        self._improvise = not self._improvise
        if self._queue_action:
            self._queue_action.put(f"improvise_{'true' if self._improvise else 'false'}")

    def get_improvise(self) -> bool:
        return self._improvise


PLAYER = Player()


@receiver(file_changed)
def on_file_changed(sender, **kwargs):
    PLAYER.stop()
    return False
