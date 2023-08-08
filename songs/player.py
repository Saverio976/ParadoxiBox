import time
from multiprocessing import Process, Queue
from typing import List, Optional

from django.dispatch import receiver
from django.utils.autoreload import file_changed

from .models import Song


class Player:
    def __init__(self) -> None:
        self._playlist: List[Song] = []
        self._current_song: Optional[Song] = None
        self._queue_song: Optional["Queue[Song]"] = None
        self._queue_action: Optional["Queue[str]"] = None
        self._queue_process_msg: Optional["Queue[str]"] = None
        self._process: Optional[Process] = None
        self._process_started = False
        self._paused = False

    def _init_process(self) -> None:
        if self._process_started is False:
            print("Starting process")
            self._queue_song = Queue()
            self._queue_action = Queue()
            self._queue_process_msg = Queue()
            self._process_started = True
            self._process = Process(
                target=self._process_loop,
                args=(self._queue_song, self._queue_action, self._queue_process_msg),
                daemon=True,
            )
            self._process.start()

    def _process_loop(
        self,
        queue_song: "Queue[Song]",
        queue_action: "Queue[str]",
        queue_process_msg: "Queue[str]",
    ):
        import pygame
        stop = False
        pygame.mixer.init()
        paused = False
        while stop is False:
            if queue_song.empty() is False:
                song = queue_song.get()
                filename = song.path_music.path
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
            else:
                time.sleep(0.1)
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
            queue_process_msg.put("next")

    def queue(self, song: Song) -> None:
        print(1, self._playlist)
        print(1, self._current_song)
        self._init_process()
        print(1, "something here 1")
        self._proccess_msg_queue()
        print(1, "something here")
        print(1, self._queue_song)
        if self._queue_song:
            print(2, self._playlist)
            print(2, self._current_song)
            self._queue_song.put(song)
            if len(self._playlist) == 0 and self._current_song is None:
                self._current_song = song
            else:
                self._playlist.append(song)
        print(3, self._playlist)
        print(3, self._current_song)

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

    def get_list_song(self) -> List[Song]:
        self._proccess_msg_queue()
        return [song for song in self._playlist]

    def get_current_song(self) -> Optional[Song]:
        self._proccess_msg_queue()
        return self._current_song

    def get_paused(self) -> bool:
        self._proccess_msg_queue()
        return self._paused


PLAYER = Player()


@receiver(file_changed)
def on_file_changed(sender, **kwargs):
    PLAYER.stop()
    return False
