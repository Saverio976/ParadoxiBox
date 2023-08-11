from threading import Thread
from typing import Any, Callable

from django.conf import settings

from .models import Song
from .ytdl import download_song_ytdl


def _download_song_helper(
    search: str, noplaylist: bool, to_execute: Callable[[Song], Any]
):
    songs = download_song_ytdl(settings.MEDIA_ROOT / "song", search, noplaylist)
    if not songs:
        return
    for song in songs:
        to_execute(song)


def download_song_helper(
    search: str,
    noplaylist: bool,
    to_execute: Callable[[Song], Any],
    threaded: bool = True,
):
    if threaded:
        Thread(
            target=_download_song_helper,
            args=(f"{search}", noplaylist, to_execute),
            daemon=True,
        ).start()
    else:
        _download_song_helper(f"{search}", noplaylist, to_execute)
