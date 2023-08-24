import orjson
from pathlib import Path
from typing import Optional

from django.conf import settings
from songs.logger import logger_print

class MusicPlayer:
    def __init__(self, configPath: Path = settings.BASE_DIR / "musicplayer.json") -> None:
        """
        configPath: Path
            json file with some config for the music player backend
        """
        try:
            with open(configPath, "r") as f:
                self.conf_json = orjson.loads(f.read())
        except OSError as esc:
            self.conf_json = {}
        except Exception as esc:
            logger_print("ERROR: MusicPlayer:", esc)
            self.conf_json = {}
        super().__init__()

    def has_song(self) -> bool:
        """
        Check if a song is being played/paused

        return false if no song; true otherwise
        """
        return False

    def play(self, filepath: Path) -> bool:
        """
        Play music file passed as parameter

        return false if can't play it; true otherwise
        """
        return False

    def get_pos(self) -> Optional[float]:
        """
        Get position of the current song (time in seconds)

        return None if no song played; the number of seconds otherwise
        """
        return None

    def get_pos_max(self) -> Optional[float]:
        """
        Get maximal position that the current song can go (time in seconds)

        return None if no song played; the number of seconds otherwise
        """
        return None

    def set_pos(self, pos: float) -> bool:
        """
        Set position of the current song (time in seconds)

        return false if no song played; true otherwise
        """
        return False

    def get_pause(self) -> bool:
        """
        Get status of pause

        return true if song paused; otherwise false
        """
        return False

    def set_pause(self, paused: bool) -> bool:
        """
        Set status of pause
        """
        return False

    def get_vol(self) -> Optional[float]:
        """
        Get volume

        return None if no volume; else the number
        """
        return None

    def get_vol_max(self) -> Optional[float]:
        """
        Get maximal volume

        return None if no volume; else the number
        """
        return None

    def set_vol(self, vol: float) -> bool:
        """
        Set volume (between `0` and `self.get_pos_max()`)

        return false if volume can't be updated; true otherwise
        """
        return False

    def stop(self):
        """
        Stop all action (the player will shutdown maybe)
        """
