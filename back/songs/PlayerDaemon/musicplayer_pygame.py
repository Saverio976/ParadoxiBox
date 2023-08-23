from pathlib import Path
from typing import Optional
import pygame
from datetime import timedelta
from .musicplayer import MusicPlayer
from mutagen.mp3 import MP3

class MusicPlayerPygame(MusicPlayer):
    def __init__(self) -> None:
        """Suport only mp3 for now"""
        pygame.mixer.init()
        self._paused = False
        self._cur_song = ""
        super().__init__()

    def __del__(self):
        self.stop()
        pygame.mixer.quit()
        return None

    def stop(self):
        pygame.mixer.music.stop()

    def has_song(self) -> bool:
        if self._paused:
            return True
        if pygame.mixer.music.get_busy():
            return True
        return False

    def play(self, filepath: Path) -> bool:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(filepath)
        self._cur_song = filepath.as_posix()
        pygame.mixer.music.play()
        if self._paused:
            pygame.mixer.music.pause()
        return True

    def get_pos(self) -> Optional[float]:
        if not self.has_song():
            return None
        seconds = timedelta(
            milliseconds=pygame.mixer.music.get_pos()
        ).total_seconds()
        return seconds

    def get_pos_max(self) -> Optional[float]:
        if not self.has_song():
            return None
        song = MP3(self._cur_song)
        return song.info.length

    def set_pos(self, pos: float) -> bool:
        if not self.has_song():
            return False
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(pos)
        return True

    def get_pause(self) -> bool:
        return self._paused

    def set_pause(self, paused: bool):
        self._paused = paused
        if self._paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def get_vol(self) -> Optional[float]:
        if not self.has_song():
            return None
        return float(pygame.mixer.music.get_volume() * 100.0)

    def get_vol_max(self) -> Optional[float]:
        return 100

    def set_vol(self, vol: float) -> bool:
        pygame.mixer.music.set_volume(vol / 100.0)
        return True
