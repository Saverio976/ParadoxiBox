from threading import Thread

from django.conf import settings

from .ytdl import download_song_ytdl
from .player import PLAYER

def _download_song_helper(search: str, noplaylist: bool, add_to_queue: bool):
    songs = download_song_ytdl(settings.MEDIA_ROOT / 'song', search, noplaylist)
    if not songs:
        return
    if not add_to_queue:
        return
    for song in songs:
        PLAYER.queue(song)


def download_song_helper(search: str, noplaylist: bool, threaded: bool = True, add_to_queue: bool = False):
    if threaded:
        Thread(
            target=_download_song_helper,
            args=(
                f"{search}",
                noplaylist,
                add_to_queue
            ),
            daemon=True
        ).start()
    else:
        _download_song_helper(f"{search}", noplaylist, add_to_queue)
